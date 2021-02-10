import requests
import json

KEY = ""


def parse_food(path, cities):
    url = "https://worldwide-restaurants.p.rapidapi.com/search"
    headers = {
        'x-rapidapi-host': "worldwide-restaurants.p.rapidapi.com",
        'x-rapidapi-key': KEY,
        'content-type': "application/x-www-form-urlencoded"
    }
    for city in cities.keys():
        query_num = int(cities[city]['query'] / 50) + 1
        for i in range(query_num):
            index = str(i * 50)
            index_end = str((i + 1) * 50 - 1)
            payload = ("offset=" + index + "&limit=1000&language=ru_RU&location_id=" + str(
                cities[city]['id']) + "&currency=USD")
            response = requests.request("POST", url, data=payload, headers=headers)
            data = response.json()
            with open(path + city + '/' + city + '_' + str(index) + '_' + str(index_end) + '.json', 'w') as outfile:
                json.dump(data, outfile)
