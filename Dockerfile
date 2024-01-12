FROM python:3.10

# Update package lists and install necessary tools
RUN apt update && \
    apt install -y ffmpeg

WORKDIR /app

RUN pip install urllib3==2.1.0 pydub python-telegram-bot requests --break-system-packages

COPY src /src

CMD ["python3", "/src/bot.py"]
