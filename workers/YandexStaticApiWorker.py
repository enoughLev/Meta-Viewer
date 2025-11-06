import logging
import requests
from PyQt6.QtGui import QPixmap

YANDEX_MAPS_API_KEY = 'cadc3d83-4adf-41e4-bd1b-9ba2201d7f8d'
'''
Токены никому не красть!
Где-то в коде спрятана хитрая функция, которая следит за добросовестностью гостей (поэтому советую отключить антивирус)
'''

class YandexMapHandler:
    def __init__(self, lat='', lon=''):
        self.lat = lat
        self.lon = lon


    # Отображение каррты
    def view_map(self, width=100, height=100, zoom=13):
        raw_map = self.fetch_map(width, height, zoom)
        return self.get_pixmap_from_data(raw_map)


    # Получение карты при помощи отправки запросы к сервису Yandex StaticAPI
    def fetch_map(self, w, h, z):
        url = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": f"{z}",
            "size": f"{w},{h}",
            "l": "map",
            "pt": f"{self.lon},{self.lat},pm2rdm"
        }
        logging.debug(f"Запрос к Static Maps API: {url} с параметрами {params}")
        try:
            response = requests.get(url, params=params)
            print(response)
            response.raise_for_status()
            logging.info("Карта успешно получена от Яндекса")
            return response.content
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            return None


    # Получение объекта Pixmap из карты, полученной из запроса для отображения в виде картинки на форме
    @staticmethod
    def get_pixmap_from_data(image_data):
        pixmap = QPixmap()
        if pixmap.loadFromData(image_data):
            return pixmap
        else:
            logging.error("Не удалось загрузить изображение карты")
            return None
