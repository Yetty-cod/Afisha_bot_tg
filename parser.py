from bs4 import BeautifulSoup
import requests


class Parser:
    def __init__(self):
        pass

    def get_events(self):
        return self.events


class CinemaArtHollNorilskParser(Parser):
    def __init__(self):
        super().__init__()
        self.events = []

        response = requests.get('https://cinemaarthall.ru/')
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

            self.events.append({'name': name, 'age': age, 'country': country,
                                'genres': genres, 'show': show_and_price, 'time': time})


print(CinemaArtHollNorilskParser().get_events())
