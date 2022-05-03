FROM python:3

# Install spotify-downloader
RUN apt-get update && apt install ffmpeg -y && pip install spotdl beets

COPY ["app/beets_config.yaml", "/root/.config/beets/config.yaml"]

WORKDIR /app
COPY app/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./app/audio_download_bot.py ./
CMD ["python", "audio_download_bot.py"]
