import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from functions import *
import datetime


# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '6900333723:AAHtoADh6ZOmdBfG3bkhl5NpyBqIjr31aXU'


def main():
    application = Application.builder().token(TOKEN).build()

    command_start = CommandHandler("start", start)
    application.add_handler(command_start)
    cinema_name = MessageHandler(filters.TEXT & ~filters.COMMAND, write_cinema)
    application.add_handler(cinema_name)
    command_back = CommandHandler("go_back", back)
    application.add_handler(command_back)
    command_today = CommandHandler("today", today)
    application.add_handler(command_today)
    command_tomorrow = CommandHandler("tomorrow", tomorrow)
    application.add_handler(command_tomorrow)
    command_after_tomorrow = CommandHandler("after_tomorrow", after_tomorrow)
    application.add_handler(command_after_tomorrow)

    load_all_schedules()  # грузим расписание в первый раз

    jq = application.job_queue
    job_minute = jq.run_repeating(load_all_schedules, interval=datetime.timedelta(days=1), first=datetime.time(0, 1))

    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()