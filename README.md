# Telegram Voice Message Processor

Module for processing voice messages and utilizing Sber's speech recognition API.
## Overview

This module contains functions to handle voice messages received by a Telegram bot. It performs various operations, including converting audio formats, acquiring authentication tokens, and using Sber's speech recognition API to convert audio to text.
### Functions

    - process_voice_message(update: telegram.Update, context: telegram.ext.CallbackContext) -> 
None: Process a voice message from a Telegram update.  
    - convert_ogg_to_mp3() -> None: Convert an OGG audio file to MP3 format.  
    - get_token() -> dict: Obtain an authentication token for API access.  
    - convert_audio_to_text() -> str: Convert audio to text using Sber's speech recognition API.  
    - main() -> None: Main function to run the Telegram bot application.  

### Files
    bot.py
    constants.py
    utils.py

## Setup
### Requirements
    Python version 3.10.13
    Docker version 24.0.7

### Installation
1. Clone the repository.
2. Set up environment variables.   
        - BOT_TOKEN: telegram bot token  
        - CLIENT_SECRET: client secret obtained at developers.sber.ru  
3. Build the Docker image:
```bash
docker build -t project-name .
```
4. Run the Docker container:
```bash
docker run -e BOT_TOKEN=$BOT_TOKEN -e CLIENT_SECRET:$CLIENT_SECRET project-name
```
## Usage
Once the application is running, interact with your Telegram bot by sending voice messages. The bot will process these messages and reply with converted text.

## Configuration
Ensure the following configurations are set up:  
Environment Variables:  
    BOT_TOKEN: Telegram Bot token.  
    CLIENT_SECRET: Sber's client secret for authentication.  

## Contributing
Contributions to this project are welcome. To contribute:
1.    Fork the repository to your GitHub account.
2.    Create a new branch for your feature or bug fix.
3.    Make changes and test thoroughly.
4.    Commit your changes with descriptive commit messages.
5.    Push your changes to your fork.
6.    Open a pull request to the main repository's branch.
 
## License
This project is licensed under Apache License Version 2.0, January 2004

## Acknowledgements
This project uses the following resources:

    python-telegram-bot: Library for interacting with Telegram API.
    pydub: Library for audio manipulation.
    requests: Library for making HTTP requests.
    (Add any other libraries or resources used in your project.)

