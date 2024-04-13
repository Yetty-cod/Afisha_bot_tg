from base_parser import Parser
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date


class KDCVisotskogoTalnahParser(Parser):
    '''
    Парсер для кинотеатра КДЦ Высотского в Талнахе
    '''
    def __init__(self, date=date.today()):
        super().__init__()

        self.name = 'КДЦ Высотского, Талнах'
        self.date = date.strftime('%Y/%m/%d')

        op = webdriver.ChromeOptions()
        op.add_argument('--headless')

        self.driver = webdriver.Chrome(options=op)

        self.driver.get('https://кдц-высоцкого.рф/repertuar/')

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        info = soup.find_all('div', {'class': 'activity'})

        for el in info:
            soup_ = BeautifulSoup(str(el), 'lxml')

            name = soup_.find('div', {'class': 'title'}).text
            age = soup_.find('div', {'class': 'age'})['data-age']

            tags = ', '.join([el.text for el in soup_.find_all('div', {'class': 'tag'})])

            price = soup_.find_all('span', {'class': 'df744'})
            price = [el.text.replace(' ', ' ') for el in price]
            time = soup_.find_all('div', {'class': 'time'})
            time = [el.text for el in time]

            self.events.append({'name': name, 'age': age, 'tags': tags,
                                'price': price, 'time': time})

    def close_page(self):
        self.driver.close()
