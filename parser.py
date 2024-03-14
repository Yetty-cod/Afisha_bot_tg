from bs4 import BeautifulSoup
import requests
import datetime


class Parser:
    '''
    Родительский класс парсера расписания кино
    '''
    def __init__(self):
        self.events = []

    def get_events(self):
        '''
        Метод возвращает список словарей с информацией о расписании.
        В словарях присутствуют поля:
            name: название фильма
            age: возрастное ограничение
            year_and_country: год производства страны-создатели через пробел
            genres: жанры через пробел
            show_and_price: зал и цена через табуляцию. каждый сеанс это элемент списка
            time: время показа. каждый сеанс это элемент списка

            show_and_price и time должны быть равной длины.
            сеанс show_and_price[i] должен соответствовать сеансу time[i]
        :return: список словарей с расписанием
        '''
        return self.events


class CinemaArtHollNorilskParser(Parser):
    '''
    Парсер для Синема Арт Холла в Норильске
    '''
    def __init__(self, date=datetime.date.today()):
        '''
        :param date: дата. Объект datetime.date
        '''
        super().__init__()

        params = {'date': date.strftime('%Y/%m/%d')}
        response = requests.get('https://cinemaarthall.ru/', params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        info = soup.find_all('div', {'class': 'event-info'})

        for el in info:
            soup_ = BeautifulSoup(str(el), 'lxml')

            name = soup_.find('h2', {'class': 'title'}).text
            age = soup_.find('div', {'class': 'age'}).text
            country = soup_.find('div', {'class': 'country'}).text
            genres = soup_.find('div', {'class': 'genres'}).text
            show_and_price = soup_.find_all('div', {'class': 'show'})
            show_and_price = [el['title'].replace('\n\n', '\t').replace('\u2009', '') for el in show_and_price]
            time = soup_.find_all('div', {'class': 'show-time'})
            time = [el.text for el in time]

            self.events.append({'name': name, 'age': age, 'year_and_country': country,
                                'genres': genres, 'show_and_price': show_and_price, 'time': time})
