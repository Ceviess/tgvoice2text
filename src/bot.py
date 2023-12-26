import os
import uuid
import logging
import requests
from telegram.ext import (
    Application,
    MessageHandler,
    filters
)
from pydub import AudioSegment
from telegram import Update

TOKEN = os.environ['BOT_TOKEN']
FILE_PATH_OGG = "voice.ogg"
FILE_PATH_MP3 = "voice.mp3"
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('my_log_file.log')
file_handler.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)  # Set the level as needed

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


async def process_voice_message(update, context):
    logger.info("Start processing file")
    file = await update.message.voice.get_file()
    await file.download_to_drive(FILE_PATH_OGG)
    logger.info("File downloaded")
    convert_ogg_to_mp3()
    logger.info("File converted to mp3")
    text = convert_audio_to_text()
    logger.info("File converted to text")
    await update.message.reply_text(text)


def convert_ogg_to_mp3():
    ogg_audio = AudioSegment.from_file(FILE_PATH_OGG, format="ogg")
    ogg_audio.export(FILE_PATH_MP3, format="mp3")


def get_token():
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    authorization_data = os.environ['CLIENT_SECRET']
    rq_uid = str(uuid.uuid4())
    api_version = 'SALUTE_SPEECH_PERS'

    headers = {
        'Authorization': f'Basic {authorization_data}',
        'RqUID': rq_uid,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'scope': api_version
    }
    logger.info("Starting getting token")
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code != 200:
        logger.info(response.status_code)
        logger.info(response.json())
        raise Exception
    logger.info("Successfully get token")
    return response.json()


def convert_audio_to_text():
    url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"
    token = get_token()['access_token']

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/mpeg"
    }

    file_path = "voice.mp3"

    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    logger.info("Starting converting audio to text")
    response = requests.post(url, headers=headers, data=audio_data, verify=False)

    if response.status_code != 200:
        logger.error(response.status_code)
        logger.error(response.json())
        raise Exception
    result = response.json()['result'][0]
    return result


def main():
    application = (
        Application.builder().token(TOKEN).build()
    )
    application.add_handler(MessageHandler(filters.VOICE, process_voice_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
