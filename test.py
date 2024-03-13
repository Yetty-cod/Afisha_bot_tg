import requests
from bs4 import BeautifulSoup


# response = requests.get('https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query=Аватар',
#                         headers={'X-API-KEY': 'VHS9Z8S-8ZJMVC0-M529YWV-WKRWP3R'})
# print(response.json())


response = requests.get('https://cinemaarthall.ru/')
soup = BeautifulSoup(response.text, 'lxml')

# titles = soup.find_all('h2', {'class': 'title'})
# age = soup.find_all('div', {'class': 'age'})
# country = soup.find_all('div', {'class': 'country'})
# genres = soup.find_all('div', {'class': 'genres'})

