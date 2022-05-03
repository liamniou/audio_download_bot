import logging as log
import os
import subprocess
import telebot


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


token = os.getenv("AUDIO_DL_BOT_TOKEN")
AUTHORIZED_USERS = [294967926, 191151492]
MUSIC_DIR = "/Music"
MUSIC_DL_DIR = "/Music_dl"
bot = telebot.TeleBot(token, threaded=False)


def instantiate_message(message, reply_msg):
    return Bunch(chat=Bunch(id=message.chat.id), text=message.text, reply=reply_msg)


def log_and_send_message_decorator(fn):
    def wrapper(message):
        log.warning(f"[FROM {message.chat.id}] [{message.text}]")
        if message.chat.id in AUTHORIZED_USERS:
            reply = fn(message)
        else:
            reply = "Sorry, this is a private bot"
        log.warning(f"[TO {message.chat.id}] [{reply}]")
        try:
            bot.send_message(message.chat.id, reply)
        except:
            log.error(f"Can't send message to {message.chat.id}")

    return wrapper


@log_and_send_message_decorator
def send_message(message):
    return message.reply


@bot.message_handler(commands=["start", "help"])
@log_and_send_message_decorator
def greet_new_user(message):
    welcome_msg = "\nWelcome to Audio Download bot! Send link to Spotify.\n"
    if message.chat.first_name is not None:
        if message.chat.last_name is not None:
            reply = f"Hello, {message.chat.first_name} {message.chat.last_name} {welcome_msg}"
        else:
            reply = f"Hello, {message.chat.first_name} {welcome_msg}"
    else:
        reply = "Hello, {message.chat.title} {welcome_msg}"

    return reply


@bot.message_handler(
    func=lambda m: m.text is not None
    and "spotify.com/" in m.text
    and m.text.startswith(("https://"))
)
def download(message):
    link = message.text
    send_message(instantiate_message(message, f"Link detected: {link}"))
    try:
        os.chdir(MUSIC_DL_DIR)
        dl_result = subprocess.run(
            ["spotdl", link],
            capture_output=True,
            text=True,
        )
        log.warning(dl_result)
        import_result = subprocess.run(
            ["beet", "import", "-A", MUSIC_DL_DIR],
            capture_output=True,
            text=True,
        )
        log.warning(import_result)
        send_message(instantiate_message(message, f"Download completed"))
    except:
        send_message(instantiate_message(message, f"Download failed"))


if __name__ == "__main__":
    subprocess.run(["beet", "import", "-A", MUSIC_DIR])
    bot.polling()
