FROM python:3.10

# Update package lists and install necessary tools
RUN apt update && \
    apt install -y ffmpeg

WORKDIR /app

RUN pip install urllib3==2.1.0 pydub python-telegram-bot requests --break-system-packages

COPY src/bot.py ./

CMD ["python3", "./bot.py"]

# COPY test.sh ./
#
# # Set permissions for the script
# RUN chmod +x ./test.sh
#
# # Start the endless script when the container starts
# CMD ["./test.sh"]
