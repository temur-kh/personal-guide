# API Общения между Frontend и Backend

Файл можно редактировать напрямую или через сервис HackMD. Ссылка на ноутбук в HackMD можно найти в Trello карточке [здесь](https://trello.com/c/NVt5fMRh).

## Запрос маршрутов

Данные запроса пользователя отправляются на сервер.

**URL** : `/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```
{
    "start_lat": "<широта стартовой точки (float)>",
    "start_lng": "<долгота стартовой точки (float)>",
    "duration": "<максимальная длительность прогулки (int)>",
    "trip_type": "<тип маршрута (str)>",
    "need_return": "<нужно ли вернуться в начальную точку(bool)>",
    "tags": "<список тегов для точек интереса(array(str))>",
    "constaints": <список тегов для дополнительных точек в маршруте(array(str))>"
}
```

**Data example**

```
{
    "start_lat": "52.51489690989536",
    "start_lng": "13.389158248901369",
    "duration": "60",
    "trip_type": "history",
    "need_return": "false",
    "tags": ["tourism_monument", "tourism_viewpoint", "tourism_fountain"],
    "constraints": ["pharmacy", "shop", "food_restaurant"]
}
```

## Success Response

**Code** : `200 OK`

**Content constraints**

```
{
    "points": [
        {
            "category": "<категория точки интереса (str)>",
            "lat": <широта точки интереса (float)>,
            "lng": <долгота точки интереса (float)>,
            "attributes": {
                "category_title": "<название категории точки на русском (str)>",
                "title": "<название точки интереса (str)>",
                "description": "<описание точки интереса (str, optional)>",
                "images": {   // optional
                    "thumbnail": {
                        "width": "<ширина картинки (int)>",
                        "height": "<высота картинки (int)>",
                        "url": "URL ссылка на картинку (str)"
                    },
                    "small": {
                        "width": "<ширина картинки (int)>",
                        "height": "<высота картинки (int)>",
                        "url": "URL ссылка на картинку (str)"
                    },
                    "medium": {
                        "width": "<ширина картинки (int)>",
                        "height": "<высота картинки (int)>",
                        "url": "URL ссылка на картинку (str)"
                    },
                    "large": {
                        "width": "<ширина картинки (int)>",
                        "height": "<высота картинки (int)>",
                        "url": "URL ссылка на картинку (str)"
                    },
                    "original": {
                        "width": "<ширина картинки (int)>",
                        "height": "<высота картинки (int)>",
                        "url": "URL ссылка на картинку (str)"
                    }
                },
                "food_rating": "<рейтинг ресторана (float[0.0, 5.0], optional)>",
                "poi_rate": <рейтинг достопримечательности (int[0, 3], optional)>
            }
        },
        ...
    ],
    "paths": [
        {
            "lat": <широта точки дорог (float)>,
            "lng": <долгота точки дорог (float)>
        },
        ...
    ]
}
```

**Content example**

```
{
    "points": [
        {
            "category": "start_point",
            "lat": 52.5147543,
            "lng": 13.3890427,
            "attributes": {
                "category_title": "Стартовая точка",
                "title": "Стартовая точка",
                "description": "Максимальная продолжительность машрута: 60 минут.\nОриентировочная скорость пешехода: 66 метров в минуту."
            }
        },
        {
            "category": "historic",
            "lat": 52.5136361,
            "lng": 13.3926475,
            "attributes": {
                "category_title": "Туристическое место",
                "title": "Метеорит",
                "description": "Мамоновский метеорит — глыба железистой руды неизвестного происхождения, найденная в песчаном карьере близ г. Мамоново Калининградской области весной 2002 года.О находке и дальнейших её злоключениях неоднократно писала местная и российская пресса: сразу после появления в печати первых сведений о «Мамоновском метеорите» к нему началось паломничество любопытствующих. Осенью 2002 года находку перевёз в Калининград владелец гостиницы «Анна» и установил в сквере по улице Тенистая аллея, напротив здания гостиницы.Сегодня доступ к «Мамоновскому метеориту» свободный; он является районной достопримечательностью.",
                "poi_rate": 2
            }
        },
        {
            "category": "pharmacy",
            "lat": 52.5197017,
            "lng": 13.3875011,
            "attributes": {
                "category_title": "Аптека",
                "title": "Аптека"
            }
        },
        {
            "category": "food",
            "lat": 52.5229855,
            "lng": 13.3828675,
            "attributes": {
                "category_title": "Ресторан",
                "title": "Кошерная Столовая",
                "images": {
                    "thumbnail": {
                        "width": "50",
                        "height": "50",
                        "url": "https://media-cdn.tripadvisor.com/media/photo-t/1c/1d/95/c0/photo0jpg.jpg"
                    },
                    "small": {
                        "width": "150",
                        "height": "150",
                        "url": "https://media-cdn.tripadvisor.com/media/photo-l/1c/1d/95/c0/photo0jpg.jpg"
                    },
                    "medium": {
                        "width": "450",
                        "height": "450",
                        "url": "https://media-cdn.tripadvisor.com/media/photo-s/1c/1d/95/c0/photo0jpg.jpg"
                    },
                    "large": {
                        "width": "550",
                        "height": "550",
                        "url": "https://media-cdn.tripadvisor.com/media/photo-p/1c/1d/95/c0/photo0jpg.jpg"
                    },
                    "original": {
                        "width": "1280",
                        "height": "1280",
                        "url": "https://media-cdn.tripadvisor.com/media/photo-m/1280/1c/1d/95/c0/photo0jpg.jpg"
                    }
                },
                "food_rating": "4.0"
            }
        }
    ],
    "paths": [
        {
            "lat": 52.5147543,
            "lng": 13.3890427
        },
        {
            "lat": 52.5146793,
            "lng": 13.3890534
        }
    ]
}
```

## Error Response

**Condition** : Если произошла ошибка на стороне сервера или не получилось построить маршруты.

**Code** : `500 INTERNAL SERVER`

**Content** :

```
{}
```
