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
        Метод возвращает список словарей с информацией о расписании. Формат в записке
        '''
        events = self.events[:]
        res = {'name': self.name, 'date': self.date, 'events': events}
        return res

    def close_page(self):
        '''
        Метод закрывает страницу браузера для парсеров динамических страниц. Для статических страниц остаётся pass
        :return:
        '''
        pass
