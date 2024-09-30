from utils.coins import get_coin_usd
from utils.translate import translate_es_ru
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater,  CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import time
from datetime import datetime
import threading
from dotenv import load_dotenv
import os
from flask import Flask

load_dotenv()

TIME, MESSAGE, COIN, TRANSLATE_RU = range(4)

app = Flask(__name__)

# Define a route (not required but useful for testing)
@app.route('/')
def hello():
    return "Bot is running!"     

def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)   


def set_alert(user_time, user_string, update):
    # Parse the target time
    target_time = datetime.strptime(user_time, "%H:%M:%S").time()
    now = datetime.now()

    # Calculate the number of seconds until the target time
    delta_seconds = (datetime.combine(now.date(), target_time) - now).total_seconds()
    if delta_seconds < 0:
        delta_seconds += 86400  # Add 24 hours if the target time is tomorrow

    # Sleep until the target time
    time.sleep(delta_seconds)

    # Alert the user
    update.message.reply_text(f"Alert: {user_string}")

def start(update, context):
    # Define the inline buttons
    user_id = update.message.from_user.id
    if user_id != int(os.getenv('USER_ID')):
       update.message.reply_text('Sorry this bot is private') 
    else:
        keyboard = [
            [InlineKeyboardButton("Set Alert", callback_data='1')],
            [InlineKeyboardButton("Get price of BTC", callback_data='2')],
            [InlineKeyboardButton("Get price of ETH", callback_data='3')],
            [InlineKeyboardButton("Get price of any coin", callback_data='4')],
            [InlineKeyboardButton("Translate Spanish into Russian", callback_data='5')]                  
        ]
    
        # Create the inline keyboard
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        # Send the message with the inline keyboard
        update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def alert_handler(update, context):
    update.message.reply_text('Please enter the time (HH:MM:SS):')
    return TIME  # Move to the next state to capture time input

def price_BTC(update, context):    
    try:
        value_BTC = get_coin_usd('BTC')
        value_currency = '${:,.2f}'.format(value_BTC)
        update.message.reply_text(f'Price of BTC: {value_currency}')
    except Exception as e:
        update.message.reply_text(f'Error: {e}')    

def price_ETH(update, context):
    try:
        value_ETH = get_coin_usd('ETH')
        value_currency = '${:,.2f}'.format(value_ETH)
        update.message.reply_text(f'Price of ETH: {value_currency}') 
    except Exception as e:
        update.message.reply_text(f'Error: {e}')

def price_coin(update, context):
    update.message.reply_text('Please enter the coin: ') 
    return COIN

def translate_into_russian(update, context):
    update.message.reply_text('Please enter the text to be translated: ') 
    return TRANSLATE_RU    

def button(update, context):
    query = update.callback_query
    query.answer()

    # Handle the button press
    match query.data:
        case '1':
            query.message.reply_text('Please enter the time (HH:MM:SS):')
            return TIME  # Move to the next state to capture time input
        case '2':       
            price_BTC(query, context)     
        case '3':
            price_ETH(query, context)        
        case '4':
            query.message.reply_text('Please enter the coin: ')  
            return COIN   
        case '5':
            query.message.reply_text('Please enter the text to be translated: ')
            return TRANSLATE_RU     
         

# Handle time input
def handle_time(update: Update, context):
    context.user_data['time'] = update.message.text
    update.message.reply_text('Now enter the message:')
    return MESSAGE  # Move to the next state to capture string input

# Handle string input
def handle_string(update: Update, context):
    user_time = context.user_data['time']
    user_string = update.message.text
    # Now you can set an alert or do something with the inputs

    thread = threading.Thread(target=set_alert, args=(user_time, user_string, update))
    thread.start()
   
    update.message.reply_text(f"Alert set. Time: {user_time}. Message: {user_string}")

    return ConversationHandler.END  # End the conversation

# Handle coin input
def handle_coin(update: Update, context):
    try:
        coin = update.message.text.upper()
        value_coin = get_coin_usd(coin)
        value_currency = '${:,.2f}'.format(value_coin)

        update.message.reply_text(f'Price of {coin}: {value_currency}')
        return ConversationHandler.END
    except Exception as e:
        update.message.reply_text(f'Error: {e}')

# Handle input of text for translation
def handle_translate_ru(update: Update, context):
    try:
        text = update.message.text
        text_translated = translate_es_ru(text)

        update.message.reply_text(f'Text translated into Russian: \n{text_translated}')
    except Exception as e:
        update.message.reply_text(f'Error: {e}')
    
    return ConversationHandler.END

# Cancel handler
def cancel(update: Update, context):
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main():
    #Run flask in parallel
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Set up the Updater and Dispatcher
    updater = Updater(os.getenv('BOT_ID'), use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button),CommandHandler('alert', alert_handler),CommandHandler('coin', price_coin),CommandHandler('translate', translate_into_russian)],
        states={
            TIME: [MessageHandler(Filters.text & ~Filters.command, handle_time)],
            MESSAGE: [MessageHandler(Filters.text & ~Filters.command, handle_string)],
            COIN:[MessageHandler(Filters.text & ~Filters.command, handle_coin)],
            TRANSLATE_RU: [MessageHandler(Filters.text & ~Filters.command, handle_translate_ru)] 
        },
        fallbacks=[CommandHandler('cancel', cancel)]                
    )

    # Define handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('btc', price_BTC))
    dp.add_handler(CommandHandler('eth', price_ETH))

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()
  

if __name__ == '__main__':
    main()
