import logging

from telegram import constants
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from cinema_parser import CinemaArtHollNorilskParser

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def afisha_today(update, context):
    await update.message.reply_text(CinemaArtHollNorilskParser().get_format_events(),
                                    parse_mode=constants.ParseMode.HTML)


def main():
    application = Application.builder().token('6764108898:AAFjiDWFaVNmxtnGhz6_AwcEl-zxPAHXDZU').build()

    command_handler = CommandHandler("shedule", afisha_today)
    application.add_handler(command_handler)

    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()