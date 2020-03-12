import traceback
import logging
from telegram import Bot, ParseMode
from functools import wraps, partial
from tkn import TOKEN, GROUP_ID, TRACEBACKS_ID


def notify_of_alert(notification, chat_id=GROUP_ID):
    notifier = Bot(token=TOKEN)
    notifier.send_message(chat_id=chat_id,
                          text=notification,
                          parse_mode=ParseMode.HTML)


def report_exception(func=None, raise_exception=True):
    if func is None:
        return partial(report_exception, raise_exception=raise_exception)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            notify_of_alert(
                "<b>hbmarch2020</b>\n\n({}, called with {}, {}) {}: {}".format(func.__name__, args, kwargs,
                                                                             type(e).__name__, str(e)),
                TRACEBACKS_ID
            )
            if raise_exception:
                raise e
            else:
                traceback_msg = traceback.format_exc()
                logging.error(traceback_msg)

    return wrapper
