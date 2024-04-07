import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from functions import *
import schedule


# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token('6764108898:AAFjiDWFaVNmxtnGhz6_AwcEl-zxPAHXDZU').build()

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

    application.run_polling()

    schedule.every().day.at("00:01").do(load_all_schedules)

    while True:
        schedule.run_pending()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    load_all_schedules()
    main()