"""
bot.py - Module containing functions for processing voice messages and interacting
with Sber's speech recognition API.

This module provides functions to process voice messages received by a Telegram bot
and perform operations like converting audio formats, obtaining authentication tokens,
and converting audio to text using Sber's speech recognition API.

Functions:
- process_voice_message(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    Process a voice message from a Telegram update.
- convert_ogg_to_mp3() -> None: Convert an OGG audio file to MP3 format.
- get_token() -> dict: Obtain an authentication token for API access.
- convert_audio_to_text() -> str: Convert audio to text using Sber's speech recognition API.
- main(): Main function to run the Telegram bot application.
"""

import os
import uuid
import requests
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram import Update
from pydub import AudioSegment
from src.constants import (
    FILE_PATH_OGG,
    FILE_PATH_MP3,
    TOKEN_URL,
    API_VERSION,
    SPEECH_URL,
    TIMEOUT,
)
from src.utils import get_logger

TOKEN = os.environ["BOT_TOKEN"]
logger = get_logger("main")


async def process_voice_message(update: Update, context: CallbackContext) -> None:
    """
    Process a voice message from an update.

    :param update: The incoming update containing the voice message.
    :type update: telegram.Update
    :param context: The context for the current update.
    :type context: telegram.ext.CallbackContext
    :return: None
    """
    logger.info("Start processing file")
    file = await update.message.voice.get_file()
    await file.download_to_drive(FILE_PATH_OGG)
    logger.info("File downloaded")
    convert_ogg_to_mp3()
    logger.info("File converted to mp3")
    text = convert_audio_to_text()
    logger.info("File converted to text")
    await update.message.reply_text(text)


def convert_ogg_to_mp3() -> None:
    """
    Convert an OGG audio file to MP3 format.

    :return: None
    """
    ogg_audio = AudioSegment.from_file(FILE_PATH_OGG, format="ogg")
    ogg_audio.export(FILE_PATH_MP3, format="mp3")


def get_token() -> dict:
    """
    Obtain a token for authentication.

    :return: JSON response containing the access token.
    """
    authorization_data = os.environ["CLIENT_SECRET"]
    rq_uid = str(uuid.uuid4())

    headers = {
        "Authorization": f"Basic {authorization_data}",
        "RqUID": rq_uid,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"scope": API_VERSION}
    logger.info("Starting getting token")
    response = requests.post(
        TOKEN_URL, headers=headers, data=data, verify=False, timeout=TIMEOUT
    )
    if response.status_code != 200:
        logger.info(response.status_code)
        logger.info(response.json())
        raise Exception
    logger.info("Successfully get token")
    return response.json()["access_token"]


def convert_audio_to_text() -> str:
    """
    Convert audio to text using Sber's speech recognition API.

    :return: Text converted from the audio.
    """
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "audio/mpeg"}

    with open(FILE_PATH_MP3, "rb") as audio_file:
        audio_data = audio_file.read()

    logger.info("Starting converting audio to text")
    response = requests.post(
        SPEECH_URL, headers=headers, data=audio_data, verify=False, timeout=TIMEOUT
    )

    if response.status_code != 200:
        logger.error(response.status_code)
        logger.error(response.json())
        raise Exception
    result = response.json()["result"][0]
    return result


def main() -> None:
    """
    Entry point

    :return: None
    """
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.VOICE, process_voice_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
