from base_parser import Parser
from requests import get
from bs4 import BeautifulSoup
from datetime import date


class CinemaArtHallNorilskParser(Parser):
    '''
    Парсер для Синема Арт Холла в Норильске
    '''
    def __init__(self, date=date.today()):
        '''
        :param date: дата. Объект datetime.date
        '''
        super().__init__()

        self.name = 'Синема Арт Холл, Норильск'
        self.date = date.strftime('%Y/%m/%d')
        params = {'date': self.date}
        response = get('https://cinemaarthall.ru/', params=params)
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
