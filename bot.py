from telegram import Bot, ParseMode, error
from time import sleep
from helpers import report_exception
from poem_obtainer import get_poems
from poem_processor import process_poem
from tkn import TOKEN, GROUP_ID


# http://поэтика.рф/поэты/державин/стихи/2049/водопад


@report_exception
def send_poems():
    bot = Bot(token=TOKEN)
    for raw_poem in get_poems():
        try:
            for chunk in process_poem(*raw_poem):
                bot.send_message(chat_id=GROUP_ID,
                                 text=chunk,
                                 parse_mode=ParseMode.HTML)
                sleep(1)
        except error.BadRequest as e:
            print(e)


if __name__ == '__main__':
    send_poems()
