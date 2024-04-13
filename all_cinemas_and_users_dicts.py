from parsers.base_parser import Parser
from parsers.cinema_art_hall_parser import CinemaArtHallNorilskParser
from parsers.rodina_parser import RodinaNorilskParser
from parsers.KDC_Visotskogo_parser import KDCVisotskogoTalnahParser


all_cinemas = {'CinemaArtHall': CinemaArtHallNorilskParser, 'Rodina': RodinaNorilskParser,
               'KDCVisotskogo': KDCVisotskogoTalnahParser}

all_cinemas_schedules = {'CinemaArtHall': {'today': Parser().get_events(),
                                           'tomorrow': Parser().get_events(),
                                           'after_tomorrow': Parser().get_events()},
                         'Rodina': {'today': Parser().get_events(),
                                    'tomorrow': Parser().get_events(),
                                    'after_tomorrow': Parser().get_events()},
                         'KDCVisotskogo': {'today': Parser().get_events(),
                                           'tomorrow': Parser().get_events(),
                                           'after_tomorrow': Parser().get_events()}}

users_cinema = dict()