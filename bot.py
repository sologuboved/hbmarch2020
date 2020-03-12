from telegram import Bot, ParseMode
from helpers import report_exception
from poem_obtainer import get_poems
from poem_processor import process_poem
from tkn import TOKEN, GROUP_ID


@report_exception
def send_poems():
    bot = Bot(token=TOKEN)
    for poem in get_poems():
        bot.send_message(chat_id=GROUP_ID,
                         text=process_poem(*poem),
                         parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    send_poems()
