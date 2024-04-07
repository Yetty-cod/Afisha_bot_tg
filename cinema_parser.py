from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import datetime


op = webdriver.ChromeOptions()
op.add_argument('--headless')

driver = webdriver.Chrome(options=op)


class Parser:
    '''
    Родительский класс парсера расписания кино
    '''
    def __init__(self):
        self.events = []
        self.date = ''
        self.name = 'Без имени'

    def get_events(self):
        '''
        Метод возвращает список словарей с информацией о расписании.
        В словарях присутствуют поля:
            name: название фильма
            age: возрастное ограничение
            tags: теги фильма
            price: цена. каждый сеанс это элемент списка
            time: время показа. каждый сеанс это элемент списка

            price и time должны быть равной длины.
            сеанс price[i] должен соответствовать сеансу time[i]
        :return: список словарей с расписанием
        '''
        return self.events

    def get_format_events(self):
        res = [f"{self.name}\n{self.date}"]
        events = self.get_events()
        if not events:
            return f'{self.name}\n{self.date}\n\nЗдесь пока пусто'

        for el in events:
            cinema = f'<b>{el["name"]}</b>\n' \
                     f'<i>{el["tags"]}\n' \
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

        self.name = 'Синема Арт Холл, Норильск'
        self.date = date.strftime('%Y/%m/%d')
        params = {'date': self.date}
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

            self.events.append({'name': name, 'age': age, 'tags': f'{country} {genres}',
                                'price': price, 'time': time})


class RodinaNorilskParser(Parser):
    def __init__(self, date=datetime.date.today()):
        super().__init__()

        self.name = 'Родина, Норильск'
        self.date = date.strftime('%Y/%m/%d')

        driver.get('http://кино-родина.рф/raspisanie')

        soup = BeautifulSoup(driver.page_source, 'lxml')
        info = soup.find_all('div', {'class': 'activity'})

        for el in info:
            soup_ = BeautifulSoup(str(el), 'lxml')

            name = soup_.find('div', {'class': 'title'}).text
            age = soup_.find('div', {'class': 'age'})['data-age']

            tags = [el.text for el in soup_.find_all('div', {'class': 'tag'})]

            price = soup_.find_all('span', {'class': 'df744'})
            price = [el.text.replace(' ', ' ') for el in price]
            time = soup_.find_all('div', {'class': 'time'})
            time = [el.text for el in time]

            self.events.append({'name': name, 'age': age, 'tags': tags,
                                'price': price, 'time': time})


class KDCVisotskogoTalnahParser(Parser):
    def __init__(self, date=datetime.date.today()):
        super().__init__()

        self.name = 'КДЦ Высотского, Талнах'
        self.date = date.strftime('%Y/%m/%d')

        driver.get('https://кдц-высоцкого.рф/repertuar/')

        soup = BeautifulSoup(driver.page_source, 'lxml')
        info = soup.find_all('div', {'class': 'activity'})

        for el in info:
            soup_ = BeautifulSoup(str(el), 'lxml')

            name = soup_.find('div', {'class': 'title'}).text
            age = soup_.find('div', {'class': 'age'})['data-age']

            tags = [el.text for el in soup_.find_all('div', {'class': 'tag'})]

            price = soup_.find_all('span', {'class': 'df744'})
            price = [el.text.replace(' ', ' ') for el in price]
            time = soup_.find_all('div', {'class': 'time'})
            time = [el.text for el in time]

            self.events.append({'name': name, 'age': age, 'tags': tags,
                                'price': price, 'time': time})