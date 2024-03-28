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
            price: цена. каждый сеанс это элемент списка
            time: время показа. каждый сеанс это элемент списка

            price и time должны быть равной длины.
            сеанс price[i] должен соответствовать сеансу time[i]
        :return: список словарей с расписанием
        '''
        return self.events

    def get_format_events(self):
        res = []
        if not self.events:
            return 'Здесь пока пусто'

        for el in self.events:
            cinema = f'<b>{el["name"]}</b>\n' \
                     f'<i>{el["year_and_country"]}\n' \
                     f'{el["genres"]}\n' \
                     f'{el["age"]}</i>\n'
            for i in range(len(el['price'])):
                cinema += f'~ {el["price"][i]}    {el["time"][i]}\n'
            res.append(cinema)

        return '\n\n'.join(res)


class CinemaArtHallNorilskParser(Parser):
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
            price = soup_.find_all('div', {'class': 'price'})
            price = [el.text.replace(' ', ' ') for el in price]
            time = soup_.find_all('div', {'class': 'show-time'})
            time = [el.text for el in time]

            self.events.append({'name': name, 'age': age, 'year_and_country': country,
                                'genres': genres, 'price': price, 'time': time})
