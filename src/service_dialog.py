import openai
import os

from db import db_dialog_data
from src.const import Result
# from run_tg_bot import log_errors


def create_new(tg_id, context):
    try:
        old_data = db_dialog_data.get_api_lobject(tg_id, "dialog")
        if not old_data:
            old_data = {}
            number_new = 1
        else:
            number_new = max(old_data) + 1
            if number_new > 100:
                number_new = 1
            if len(old_data) == 5:
                number_del = min(old_data)
                old_data.pop(number_del)

        context.user_data['active_dialog_id'] = number_new
        new_data = {number_new: [{"role": "system", "content": "Ты хороший ассистент"}]}
        old_data.update(new_data)
        db_dialog_data.update_data(tg_id, 'dialog', old_data,)
        return Result.OK
    except Exception as e:
        return Result.ERROR


def get_keyboard_with_history(tg_id, inline_button):
    dialog_messages = db_dialog_data.get_api_lobject(tg_id, "dialog")
    inline_keyboard = []
    if dialog_messages:
        for key, value in dialog_messages.items():
            if len(value) > 1:
                button_name = f"{key} | {value[1]['content'][:10]}..."
            else:
                button_name = f"{key}| NEW"
            button = [inline_button(button_name, callback_data=key)]
            inline_keyboard.append(button)
    return inline_keyboard


def get_gpt_answer(user_message, tg_id, d_id):
    try:
        dialog_messages = db_dialog_data.get_api_lobject(tg_id, "dialog")
        active_dialog = dialog_messages[d_id]
        user_answer = {"role": "user", "content": user_message}
        active_dialog.append(user_answer)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=active_dialog
        )
        gpt_answer = response['choices'][0]['message']['content']
        save_gpt_answer(gpt_answer, active_dialog, dialog_messages, d_id, tg_id)
        return gpt_answer
    except Exception as e:
        return 'Произошла ошибка'
        raise


def save_gpt_answer(text, active_dialog, dialog_messages, d_id, tg_id):
    gpt_answer = {"role": "assistant", "content": text}
    active_dialog.append(gpt_answer)
    dialog_messages[d_id] = active_dialog
    db_dialog_data.update_data(tg_id, 'dialog', dialog_messages)
