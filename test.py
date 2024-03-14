import requests
from bs4 import BeautifulSoup
from parser import CinemaArtHollNorilskParser


# response = requests.get('https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query=Аватар',
#                         headers={'X-API-KEY': 'VHS9Z8S-8ZJMVC0-M529YWV-WKRWP3R'})
# print(response.json())

print(CinemaArtHollNorilskParser().get_events())