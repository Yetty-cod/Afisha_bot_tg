import logging

from telegram import constants
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from cinema_parser import CinemaArtHallNorilskParser
from telegram import ReplyKeyboardMarkup

from datetime import date, timedelta

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
all_cinemas = {'CinemaArtHall': CinemaArtHallNorilskParser}
cinema = ''


async def start(update, context):
    reply_keyboard = [["/CinemaArtHall"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Я афиша-бот. Какую информацию вы хотите получить?", reply_markup=markup)


async def write_cinema(update, context):
    global cinema
    cinema = update.message.text.strip('/')
    day = [["/today", "/tomorrow", "/after_tomorrow"]]
    day_markup = ReplyKeyboardMarkup(day, one_time_keyboard=True)

    await update.message.reply_text("На какой день вы хотите получить расписание?", reply_markup=day_markup)


async def today(update, context):
    global cinema
    await update.message.reply_text(all_cinemas[cinema]().get_format_events(), parse_mode=constants.ParseMode.HTML)


async def tomorrow(update, context):
    global cinema
    date_ = date.today() + timedelta(days=1)
    await update.message.reply_text(all_cinemas[cinema](date=date_).get_format_events(),
                                    parse_mode=constants.ParseMode.HTML)


async def after_tomorrow(update, context):
    global cinema
    date_ = date.today() + timedelta(days=2)
    await update.message.reply_text(all_cinemas[cinema](date=date_).get_format_events(),
                                    parse_mode=constants.ParseMode.HTML)


def main():
    application = Application.builder().token('6764108898:AAFjiDWFaVNmxtnGhz6_AwcEl-zxPAHXDZU').build()

    command_start = CommandHandler("start", start)
    application.add_handler(command_start)
    command_cinema_art_holle = CommandHandler("CinemaArtHall", write_cinema)
    application.add_handler(command_cinema_art_holle)
    command_today = CommandHandler("today", today)
    application.add_handler(command_today)
    command_tomorrow = CommandHandler("tomorrow", tomorrow)
    application.add_handler(command_tomorrow)
    command_after_tomorrow = CommandHandler("after_tomorrow", after_tomorrow)
    application.add_handler(command_after_tomorrow)

    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()