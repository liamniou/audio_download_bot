This Telegram bot downloads audio files from Spotify and sorts them into folders using the Beets tool.

## Prerequisites
- create bot user via [BotFather and get API token](https://core.telegram.org/bots#3-how-do-i-create-a-bot);
- install Docker.

## Usage
# Build Docker image
![build_and_publish_docker_image](https://github.com/liamniou/audio_download_bot/actions/workflows/docker-publish.yml/badge.svg)
> docker build -f Dockerfile -t audio_download_bot .
# Start Docker container
> docker run -dit \
  --name=audio_download_bot \
  --env=AUDIO_DL_BOT_TOKEN=PUT_TOKEN_HERE \
  -v PUT_LOCAL_PATH_TO_MUSIC_FOLDER_HERE:/Music \
  -v PUT_LOCAL_PATH_TO_MUSIC_DL_FOLDER_HERE:/Music_dl \
  audio_download_bot
