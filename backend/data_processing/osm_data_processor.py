from pymongo import MongoClient

from backend.data_processing.data_processor import DataProcessor
from backend.utils.configuration import *


class OSMDataProcessor(DataProcessor):
    """
    Класс для работы с данными, полученными из OpenStreetMap, которые хранятся в MongoDB.

    Attributes:
        client(pymongo.MongoClient) - клиент для подключения к MongoDB.
        db(pymongo.database.Database) - база данных.
    """

    client = None
    db = None

    def __init__(self):
        """
        Инициализация подключения к БД.
        """
        self._create_connection()

    def _create_connection(self):
        """
        Подключение к базе данных.
        """

        self.client = MongoClient(osm_data_processor[SITE_NAME])
        self.db = self.client.get_database(osm_data_processor[DATABASE_NAME])
        # Пока непонятно, нужно ли это делать каждый раз при подключении к базе
        self.db.nodes.create_index([('location', "2dsphere")])

    def get_nearest_points(self, lat, lon, max_distance, tags=None):
        """
        Поиск всех точек на карте в заданной окружности.

        Params:
            lat(double) - широта.
            lon(double) - долгота.
            max_distance(double) - максимальный радиус поиска в метрах.
            tags(list(str)) - список тегов для ближайших точек. 

        Returns:
            list - список подходящих объектов.

        """
        params = {
            "location": {
                "$near": {
                    "$geometry": {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    },
                    "$maxDistance": max_distance,
                }
            }
        }

        if tags is not None:
            params['important'] = True
            params['global_tags'] = {
                '$in': tags
            }

        return self.select_query(
            collection_name='nodes',
            params=params,
        )

    def get_nodes_by_tags(self, tags):
        """
        Запрос для получения точек интереса по тегам.

        Params: 
            tags(list(str)) - список тегов.

        Returns:
            list - список подходящих объектов.

        """

        params = {
            'important': True,
            'global_tags': {
                '$in': tags
            }
        }

        return self.select_query(
            collection_name='nodes',
            params=params
        )

    def select_query(self, collection_name, params):
        """
        Запрос типа SELECT в базу данных.

        Params:
            collection_name(str) - имя коллекции.
            params(dict(str->str)) - словарь с параметрами для фильтрации.

        Returns:
            list - список объектов в коллекции, соответствующих запросу.
            Если коллекция отсутствует в базе данных, то возращается пустой список.
        """
        if collection_name in self.db.collection_names():
            collection = self.db.get_collection(collection_name)
            return list(collection.find(params))
        return []

    def close_connection(self):
        """
        Закрытие подключения к базе данных.
        """
        self.client.close()
