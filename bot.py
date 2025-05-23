from utils.coins import get_coin_usd
from utils.translate import translate_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from utils.chatai import LangChainModel
from datetime import datetime
import threading
from dotenv import load_dotenv
import os
from flask import Flask
import asyncio
import logging

logger = logging.getLogger(__name__)

load_dotenv()

TIME, MESSAGE, COIN, TRANSLATE, TRANSLATE_LANGUAGE, ASKAI = range(6)

app = Flask(__name__)


@app.route('/')
def hello():
    return "Bot is running!"


def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)


async def set_alert(user_time, user_string, update: Update):
    target_time = datetime.strptime(user_time, "%H:%M:%S").time()
    now = datetime.now()
    delta_seconds = (datetime.combine(
        now.date(), target_time) - now).total_seconds()
    if delta_seconds < 0:
        delta_seconds += 86400

    await asyncio.sleep(delta_seconds)
    await update.message.reply_text(f"Alert: {user_string}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != int(os.getenv('USER_ID') or '0'):
        await update.message.reply_text('Sorry this bot is private')
    else:
        keyboard = [
            [InlineKeyboardButton("Set Alert", callback_data='1')],
            [InlineKeyboardButton("Get price of BTC", callback_data='2')],
            [InlineKeyboardButton("Get price of ETH", callback_data='3')],
            [InlineKeyboardButton(
                "Get price of any currency", callback_data='4')],
            [InlineKeyboardButton(
                "Translate Text", callback_data='5')],
            [InlineKeyboardButton(
                "Ask question to AI", callback_data='6')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Choose an option:', reply_markup=reply_markup)


async def alert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the time (HH:MM:SS):')
    return TIME


async def price_BTC(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value_BTC = get_coin_usd('BTC')
        value_currency = '${:,.2f}'.format(value_BTC)
        await update.message.reply_text(f'Price of BTC: {value_currency}')
    except Exception as e:
        logger.exception("Failed to get the price of BTC")
        await update.message.reply_text(f'Error: {e}')


async def price_ETH(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value_ETH = get_coin_usd('ETH')
        value_currency = '${:,.2f}'.format(value_ETH)
        await update.message.reply_text(f'Price of ETH: {value_currency}')
    except Exception as e:
        logger.exception("Failed to get the price of ETH")
        await update.message.reply_text(f'Error: {e}')


async def price_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the coin: ')
    return COIN


async def askai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the prompt: ')
    return ASKAI


async def translate_text_opt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the text to be translated: ')
    return TRANSLATE


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    match query.data:
        case '1':
            await query.message.reply_text('Please enter the time (HH:MM:SS):')
            return TIME
        case '2':
            await price_BTC(query, context)
        case '3':
            await price_ETH(query, context)
        case '4':
            await query.message.reply_text('Please enter the coin: ')
            return COIN
        case '5':
            await query.message.reply_text('Please enter the text to be translated: ')
            return TRANSLATE
        case '6':
            await query.message.reply_text('Please enter the prompt: ')
            return ASKAI


async def handle_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text
    await update.message.reply_text('Now enter the message:')
    return MESSAGE


async def handle_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_time = context.user_data['time']
    user_string = update.message.text
    asyncio.create_task(set_alert(user_time, user_string, update))

    await update.message.reply_text(f"Alert set. Time: {user_time}. Message: {user_string}")
    return ConversationHandler.END


async def handle_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coin = update.message.text.upper()
        value_coin = get_coin_usd(coin)
        value_currency = '${:,.2f}'.format(value_coin)

        await update.message.reply_text(f'Price of {coin}: {value_currency}')
        return ConversationHandler.END
    except Exception as e:
        logger.exception(f"Failed to get the price of {coin.upper()}")
        await update.message.reply_text(f'Error: {e}')


async def handle_translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['text_translate'] = update.message.text

        await update.message.reply_text(f'Enter the target language (e.g: en):')
        return TRANSLATE_LANGUAGE
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')
        return ConversationHandler.END


async def handle_translate_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_language = update.message.text

        if len(target_language) != 2:
            raise Exception("Invalid source and target languages format")

        text_translate = context.user_data.get('text_translate')
        translated_text = translate_text(
            text_translate, "auto", target_language)

        await update.message.reply_text(f'Text translated: \n{translated_text}')
    except Exception as e:
        logger.exception(f"Failed to translate text")
        await update.message.reply_text(f'Error: {e}')

    return ConversationHandler.END


async def handle_ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_prompt = update.message.text
        langchain_model = LangChainModel()
        response = langchain_model.get_response(user_prompt)

        await update.message.reply_text(f'AI response: \n{response}', parse_mode='Markdown')
    except Exception as e:
        logger.exception(f"Failed to get AI response")
        await update.message.reply_text(f'Error: {e}')

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END


def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    application = Application.builder().token(os.getenv('BOT_ID', '')).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('alert', alert_handler), CommandHandler(
            'coin', price_coin), CommandHandler('askai', askai), CommandHandler('translate', translate_text_opt), CallbackQueryHandler(button)],
        states={
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_time)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_string)],
            COIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coin)],
            TRANSLATE: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_translate_text)],
            TRANSLATE_LANGUAGE: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_translate_language)],
            ASKAI: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_ask_ai)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('btc', price_BTC))
    application.add_handler(CommandHandler('eth', price_ETH))
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
