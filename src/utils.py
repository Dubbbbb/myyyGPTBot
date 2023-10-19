import os
import pickle

import speech_recognition as sr

from pathlib import Path


def get_voice_file_name(user_id, main_path):
    counter = 0
    file_name = f'{user_id}_audio_{counter}.ogg'

    file_path = f"{main_path}{os.path.sep}{file_name}"
    while os.path.exists(file_path):
        counter += 1
        file_name = f'{user_id}_audio_{counter}.ogg'
        file_path = f"{main_path}{os.path.sep}{file_name}"
    return file_name[:-4]


def get_text_from_audio_message(user_id, new_file):
    try:
        # main_path = "/home/dubbuddub/bot"
        main_path = os.getcwd()
        file_name = get_voice_file_name(user_id, main_path)

        # Сохраняем аудиофайл на диск
        tg_file = f'{file_name}.ogg'
        new_file.download(tg_file)

        # Конвертируем аудиофайл в нужный формат
        converted_file = f'{file_name}.wav'
        os.system(f'ffmpeg -i {tg_file} -c:a pcm_s16le -ar 16000 {converted_file}')

        # Создаем объект распознавания речи
        r = sr.Recognizer()

        # Открываем аудиофайл
        with sr.AudioFile(converted_file) as source:
            audio_data = r.record(source)
            # Распознаем речь
            text = r.recognize_google(audio_data, language="ru")

        os.remove(converted_file)
        os.remove(tg_file)
        return text

    except:
        os.remove(converted_file)
        os.remove(tg_file)
        return None


def save_data(data, name, path='data/'):
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(path + str(name), 'wb') as f:
        pickle.dump(data, f)


def load_data(name, path='data/'):
    with open(path + str(name), 'rb') as f:
        return pickle.load(f)

