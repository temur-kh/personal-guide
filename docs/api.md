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
            "lng": <долгота точки интереса (float)>
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
            "category": "start_point"
            "lat": 52.5147543
            "lng": 13.3890427
        },
        {
            "category": "historic"
            "lat": 52.5136361
            "lng": 13.3926475
        },
        {
            "category": "pharmacy"
            "lat": 52.5197017
            "lng": 13.3875011
        },
        {
            "category": "food"
            "lat": 52.5229855
            "lng": 13.3828675
        }
    ],
    "paths": [
        {
            "lat": 52.5147543,
            "lng": 13.3890427
        },
        {
            "lat": 52.5146793
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
