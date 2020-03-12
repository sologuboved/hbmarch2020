from telegram import Bot, ParseMode, error
from helpers import report_exception
from poem_obtainer import get_poems
from poem_processor import process_poem
from tkn import TOKEN, GROUP_ID


# http://поэтика.рф/поэты/державин/стихи/2049/водопад


@report_exception
def send_poems():
    bot = Bot(token=TOKEN)
    for poem in get_poems():
        try:
            bot.send_message(chat_id=GROUP_ID,
                             text=process_poem(*poem),
                             parse_mode=ParseMode.HTML)
        except error.BadRequest:
            print(poem)


if __name__ == '__main__':
    send_poems()
