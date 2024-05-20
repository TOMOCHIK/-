from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from datetime import datetime
from api_keys import TOKEN
from summarize import summarize
from get_text import get_text  

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Мои команды здесь: /help')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/summarize [текст] - Суммаризирует Ваш текст\n'
                                    '/link [ссылка] - Суммаризация новостей по вашей ссылке\n')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = 'Такой команды нет...'
    await update.message.reply_text(response)

async def on_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'(!) Update {update} caused {context.error}')
    if update and update.effective_message:
        chat_id = update.effective_message.chat_id
        await context.bot.send_message(chat_id=chat_id, text=f"Error! {context.error}")

async def summ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message = ' '.join(context.args)
        response = summarize(message)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text('Неправильный ввод!')

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        url = context.args[0]
        status, text = get_text(url)
        if status:
            response = summarize(text, mode='link')
            await update.message.reply_text(response)
        else:
            await update.message.reply_text('Неправильная ссылка!')
    else:
        await update.message.reply_text('Введите ссылку... /link ссылка')

if __name__ == '__main__':
    logging.info('Bot starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('summarize', summ))
    app.add_handler(CommandHandler('link', link))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(on_error)

    app.run_polling(poll_interval=3)
