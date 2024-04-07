from telegram import ReplyKeyboardMarkup
from telegram import constants

from datetime import date, timedelta
import logging

from keyboards import *
from all_cinemas_and_users_dicts import all_cinemas, users_cinema


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update, context):
    '''Функция для старта, выводит подсказку и клавиатуру'''
    markup = ReplyKeyboardMarkup(keyboard_cinemas, one_time_keyboard=False)
    await update.message.reply_text("Я афиша-бот. Какую информацию вы хотите получить?", reply_markup=markup)


async def write_cinema(update, context):
    '''Функция запускается когда пользователь выбирает кинотеатр.
    Нужна для записи выбранного кинотеатра и вывода клавиатуры с выбором дня'''
    if update.message.text in all_cinemas:
        logger.info(update.message.chat_id)
        users_cinema[update.message.chat_id] = update.message.text

        day_markup = ReplyKeyboardMarkup(keyboard_day, one_time_keyboard=False)

        await update.message.reply_text("На какой день вы хотите получить расписание?", reply_markup=day_markup)
    else:
        await update.message.reply_text("Такого кинотеатра ещё нет:(")


async def today(update, context):
    '''Функция обрабатывает команду /today'''
    if update.message.chat_id in users_cinema:
        await update.message.reply_text(
            all_cinemas[users_cinema[update.message.chat_id]]().get_format_events(),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def tomorrow(update, context):
    '''Функция обрабатывает команду /tomorrow'''
    if update.message.chat_id in users_cinema:
        date_ = date.today() + timedelta(days=1)
        await update.message.reply_text(
            all_cinemas[users_cinema[update.message.chat_id]](date=date_).get_format_events(),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def after_tomorrow(update, context):
    '''Функция обрабатывает команду /after_tomorrow'''
    if update.message.chat_id in users_cinema:
        date_ = date.today() + timedelta(days=2)
        await update.message.reply_text(
            all_cinemas[users_cinema[update.message.chat_id]](date=date_).get_format_events(),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def back(update, context):
    '''Функция обрабатывает команду /go_back'''
    markup = ReplyKeyboardMarkup(keyboard_cinemas, one_time_keyboard=False)
    await update.message.reply_text("Какую информацию вы хотите получить?", reply_markup=markup)