from utils.cryptos import get_BTCUSD_rate, get_ETHUSD_rate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater,  CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import time
from datetime import datetime
import threading
from dotenv import load_dotenv
import os

load_dotenv()

TIME, STRING = range(2)

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
    keyboard = [
        [InlineKeyboardButton("Set Alert", callback_data='1')],
        [InlineKeyboardButton("Get value of BTC", callback_data='2')],
        [InlineKeyboardButton("Get value of ETH", callback_data='3')]           
    ]
    
    # Create the inline keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the message with the inline keyboard
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()

    # Handle the button press
    if query.data == '1':
        query.message.reply_text('Please enter the time (HH:MM:SS):')
        return TIME  # Move to the next state to capture time input
    if query.data == '2':
        value_BTC = get_BTCUSD_rate()
        value_currency = '${:,.2f}'.format(value_BTC)
        query.message.reply_text(f'Value of BTC: {value_currency}')   
    if query.data == '3':
        value_BTC = get_ETHUSD_rate()
        value_currency = '${:,.2f}'.format(value_BTC)
        query.message.reply_text(f'Value of ETH: {value_currency}')   


# Handle time input
def handle_time(update: Update, context):
    context.user_data['time'] = update.message.text
    update.message.reply_text('Now enter the message:')
    return STRING  # Move to the next state to capture string input

# Handle string input
def handle_string(update: Update, context):
    user_time = context.user_data['time']
    user_string = update.message.text
    # Now you can set an alert or do something with the inputs

    thread = threading.Thread(target=set_alert, args=(user_time, user_string, update))
    thread.start()
   
    update.message.reply_text(f"Alert set. Time: {user_time}. Message: {user_string}")

    return ConversationHandler.END  # End the conversation


# Cancel handler
def cancel(update: Update, context):
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main():
    # Set up the Updater and Dispatcher
    updater = Updater(os.getenv('BOT_ID'), use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            TIME: [MessageHandler(Filters.text & ~Filters.command, handle_time)],
            STRING: [MessageHandler(Filters.text & ~Filters.command, handle_string)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]        
    )

    # Define handlers
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
