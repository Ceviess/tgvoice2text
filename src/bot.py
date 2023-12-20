import os
import uuid
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


async def process_voice_message(update, context):
    file = await update.message.voice.get_file()
    await file.download_to_drive(FILE_PATH_OGG)
    convert_ogg_to_mp3()
    text = convert_audio_to_text()
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

    response = requests.post(url, headers=headers, data=data, verify=False)
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

    response = requests.post(url, headers=headers, data=audio_data, verify=False)

    if response.status_code == 200:
        result = response.json()['result'][0]
        return result



if __name__ == "__main__":
    application = (
        Application.builder().token(TOKEN).build()
    )
    application.add_handler(MessageHandler(filters.VOICE, process_voice_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
