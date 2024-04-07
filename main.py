import logging

from telegram import constants
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from cinema_parser import CinemaArtHallNorilskParser, RodinaNorilskParser, KDCVisotskogoTalnahParser
from telegram import ReplyKeyboardMarkup

from datetime import date, timedelta

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
all_cinemas = {'CinemaArtHall': CinemaArtHallNorilskParser, 'Rodina': RodinaNorilskParser,
               'KDCVisotskogo': KDCVisotskogoTalnahParser}
cinema = dict()
keyboard_cinemas = [["CinemaArtHall", "Rodina", "KDCVisotskogo"]]


async def start(update, context):
    global keyboard_cinemas
    markup = ReplyKeyboardMarkup(keyboard_cinemas, one_time_keyboard=False)
    await update.message.reply_text("Я афиша-бот. Какую информацию вы хотите получить?", reply_markup=markup)


async def write_cinema(update, context):
    global cinema
    if update.message.text in all_cinemas:
        logger.info(update.message.chat_id)
        cinema[update.message.chat_id] = update.message.text
        day = [["/today", "/tomorrow", "/after_tomorrow"],
               ["/go_back"]]
        day_markup = ReplyKeyboardMarkup(day, one_time_keyboard=False)

        await update.message.reply_text("На какой день вы хотите получить расписание?", reply_markup=day_markup)
    else:
        await update.message.reply_text("Такого кинотеатра ещё нет:(")


async def today(update, context):
    global cinema
    if update.message.chat_id in cinema:
        await update.message.reply_text(
            all_cinemas[cinema[update.message.chat_id]]().get_format_events(), parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def tomorrow(update, context):
    global cinema
    if update.message.chat_id in cinema:
        date_ = date.today() + timedelta(days=1)
        await update.message.reply_text(all_cinemas[cinema[update.message.chat_id]](date=date_).get_format_events(),
                                        parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def after_tomorrow(update, context):
    global cinema
    if update.message.chat_id in cinema:
        date_ = date.today() + timedelta(days=2)
        await update.message.reply_text(all_cinemas[cinema[update.message.chat_id]](date=date_).get_format_events(),
                                        parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def back(update, context):
    global keyboard_cinemas
    markup = ReplyKeyboardMarkup(keyboard_cinemas, one_time_keyboard=False)
    await update.message.reply_text("Какую информацию вы хотите получить?", reply_markup=markup)


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


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()