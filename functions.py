from telegram import ReplyKeyboardMarkup
from telegram import constants

from datetime import date, timedelta
import logging

from keyboards import *
from all_cinemas_and_users_dicts import all_cinemas, users_cinema, all_cinemas_schedules


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def load_all_schedules(*args):
    '''
    Функция обновляет словарь с распианием всех кинотеатров
    :return:
    '''
    for el in all_cinemas_schedules:
        logger.info(f'Start loading {el} schedule')

        cinema = all_cinemas[el](date.today())
        all_cinemas_schedules[el]['today'] = cinema.get_events()
        cinema.close_page()

        cinema = all_cinemas[el](date.today())
        all_cinemas_schedules[el]['tomorrow'] = all_cinemas[el](date.today() + timedelta(days=1)).get_events()
        cinema.close_page()

        cinema = all_cinemas[el](date.today())
        all_cinemas_schedules[el]['after_tomorrow'] = all_cinemas[el](date.today() + timedelta(days=2)).get_events()
        cinema.close_page()

        logger.info(f'Finish loading {el} schedule')
    logger.info('Finish load all schedules')


def format_schedule(schedule):
    '''
    Функция форматирует расписание кино
    :param schedule: список словарей со структурой, описанной в Parser.get_events()
    :return: строка
    '''
    res = [f"{schedule['name']}\n{schedule['date']}"]
    events = schedule['events']
    if not events:
        return f'{schedule["name"]}\n{schedule["date"]}\n\nЗдесь пока пусто'

    for el in events:
        cinema = f'<b>{el["name"]}</b>\n' \
                 f'<i>{el["tags"]}\n' \
                 f'{el["age"]}</i>\n'
        for i in range(len(el['price'])):
            cinema += f'~ {el["price"][i]}    {el["time"][i]}\n'
        res.append(cinema)

    return '\n\n'.join(res)


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
            format_schedule(all_cinemas_schedules[users_cinema[update.message.chat_id]]['today']),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def tomorrow(update, context):
    '''Функция обрабатывает команду /tomorrow'''
    if update.message.chat_id in users_cinema:
        await update.message.reply_text(
            format_schedule(all_cinemas_schedules[users_cinema[update.message.chat_id]]['tomorrow']),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def after_tomorrow(update, context):
    '''Функция обрабатывает команду /after_tomorrow'''
    if update.message.chat_id in users_cinema:
        await update.message.reply_text(
            format_schedule(all_cinemas_schedules[users_cinema[update.message.chat_id]]['after_tomorrow']),
            parse_mode=constants.ParseMode.HTML)
    else:
        await update.message.reply_text("Вы не выбрали кинотеатр")


async def back(update, context):
    '''Функция обрабатывает команду /go_back'''
    markup = ReplyKeyboardMarkup(keyboard_cinemas, one_time_keyboard=False)
    await update.message.reply_text("Какую информацию вы хотите получить?", reply_markup=markup)