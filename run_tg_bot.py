import os
import openai

from dotenv import load_dotenv
from src import service_dialog, utils
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext.defaults import Defaults

import logging


def log_errors(func):
    def wrapper(*args, **kwargs):
        # Создание объекта логгера
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.ERROR)

        # Создание объекта обработчика, например, запись в файл
        file_handler = logging.FileHandler('errors.log')
        file_handler.setLevel(logging.ERROR)

        # Создание объекта форматирования
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Добавление обработчика в логгер
        logger.addHandler(file_handler)

        try:
            # Выполнение функции
            result = func(*args, **kwargs)
        except Exception as e:
            # Логирование ошибки
            logger.error(f'Ошибка в функции {func.__name__}: {str(e)}')
            result = error_message(*args, **kwargs)

        return result
    return wrapper


dotenv_path = f"{os.getcwd()}{os.path.sep}.env"
# dotenv_path = "/home/dubbuddub/bot/.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

openai.api_key = os.environ.get('OPENAI_API_KEY')
TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')


@log_errors
def start(update, context):
    chat_id = update.effective_chat.id
    text = "<b>Это Chat GPT в Telegram\n\n" \
             "Новый диалог - /new\n" \
             "История диалогов - /history\n" \
             "Активный диалог - /active\n\n" \
             "Начинай новый диалог и задавай вопросы</b>\n\n" \
             "<u>5 последних диалогов будут хранится в истории, ты всегда сможешь к ним вернуться</u>"
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())


@log_errors
def active_dialog(update, context):
    chat_id = update.effective_chat.id
    active_dialog_id = context.user_data.get('active_dialog_id')
    if active_dialog_id:
        text = f"Твой активный диалог под номером- {active_dialog_id}"
    else:
        text = f"У тебя нет активного диалога\n\n" \
               f"Для использования бота:\n" \
               f"<b>Активируйте диалог в истории или создайте новый</b>"
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


@log_errors
def new_dialog(update, context):
    user_from = update.message.from_user
    chat_id = update.effective_chat.id
    is_create = service_dialog.create_new(user_from['id'], context)
    if is_create:
        context.bot.send_message(chat_id=chat_id, text=f'Диалог создан, пиши в чат свои вопросы')
    else:
        context.bot.send_message(chat_id=chat_id, text=f'Возникли проблемы при создании диалога')


@log_errors
def history_dialog(update, context):
    user_from = update.message.from_user
    inline_keyboard = service_dialog.get_keyboard_with_history(user_from['id'], InlineKeyboardButton)
    if inline_keyboard:
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        update.message.reply_text('Выбери диалог:', reply_markup=reply_markup)
    else:
        update.message.reply_text('У тебя нет истории диалогов')


@log_errors
def answer_any_text(update, context):
    user_from = update.message.from_user
    chat_id = update.message.chat_id
    active_dialog_id = context.user_data.get('active_dialog_id')
    if not active_dialog_id:
        text = f"Для использования бота:\n" \
               f"<b>Активируйте диалог в истории или создайте новый</b>"
    else:
        if update.message.voice:
            file_id = update.message.voice.file_id
            new_file = context.bot.getFile(file_id)
            user_message = utils.get_text_from_audio_message(user_from.id, new_file)
            if user_message:
                context.bot.send_message(chat_id=chat_id, text=f"Ваш голосовой запрос:\n\n{user_message}",
                                         parse_mode='HTML')
        else:
            user_message = update.message.text
        msg = context.bot.send_message(chat_id=chat_id, text="⏳ Ждем-с..", parse_mode='HTML')
        text = service_dialog.get_gpt_answer(user_message, user_from['id'], int(active_dialog_id))
        context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')


@log_errors
def callback_handler(update, context):
    dialog_number = update.callback_query.data
    context.user_data['active_dialog_id'] = int(dialog_number)
    update.callback_query.message.reply_text(f"Вы переключились на диалог под номером - {dialog_number} ")


@log_errors
def error_message(update, context):
    try:
        update.message.reply_text("ОШИБКА 🤬")
    except:
        update.callback_query.message.reply_text("ОШИБКА 🤬")


@log_errors
def send_log_file(update, context):
    chat_id = update.effective_chat.id
    file_path = f"{os.getcwd()}{os.path.sep}errors.log"
    try:
        context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
    except Exception as e:
        update.message.reply_text(f"{e}")


@log_errors
def send_update_message(update, context):
    folder_data_path = f"{os.getcwd()}{os.path.sep}data"
    update_message = os.environ.get('UPDATE_MESSAGE')
    for filename in os.listdir(folder_data_path):
        user_id = filename.replace('_dialog', '')
        context.bot.send_message(chat_id=user_id, text=update_message, parse_mode='HTML')


updater = Updater(TELEGRAM_API_KEY, defaults=Defaults(run_async=True))
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('active', active_dialog))
dp.add_handler(CommandHandler('new', new_dialog))
dp.add_handler(CommandHandler('history', history_dialog))
dp.add_handler(CommandHandler('sendlog', send_log_file))
dp.add_handler(CommandHandler('sendupdatemessage', send_update_message))

dp.add_handler(MessageHandler(Filters.text, answer_any_text))
dp.add_handler(MessageHandler(Filters.voice, answer_any_text))

dp.add_handler(CallbackQueryHandler(callback_handler))

updater.start_polling()
updater.idle()
