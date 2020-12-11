import time
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import random
import sys
import os
from werkzeug.datastructures import ImmutableMultiDict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from general_service.service import Service
from data_processing.osm_data_processor import OSMDataProcessor
from graph_constructor.osm_graph_constructor import OsmGraphConstructor


osm_data_processor = OSMDataProcessor()
constructor = OsmGraphConstructor.create(osm_data_processor, "./cache/", cache=False)
service = Service(constructor)

def print_performance(time_results):
    """
    Вывод результатов рабты теста в консоль.

    Params:
        time_results(dict) - словарь, в котором хранится количество времени для построения маршрута разной длительности.

    """

    for time_for_route, ans_for_time in time_results.items():
        print("Statistics for creating {} minutes route:\nmean time {}s\nstd time {}s"
              .format(time_for_route, np.mean(ans_for_time), np.std(ans_for_time))
              )


def draw_performance(time_results):
    """
    Изображение полученных статистик с помощью boxplota.

    Params:
        time_results(dict) - словарь, в котором хранится количество времени для построения маршрута разной длительности.

    """

    plt.title('Performance results')
    plt.xlabel('Route time, min')
    plt.ylabel('Algorithm time, sec')
    data = time_results.values()
    labels = [str(key) for key in time_results.keys()]
    plt.boxplot(data)
    plt.xticks(list(range(1, len(time_results) + 1)), labels)
    plt.show()
    plt.savefig('performance_results.png')


def write_performance_to_file(time_results, file_name='performance.json'):
    """
    Запись результатов работы тестирования в файл.

    Params:
        time_results(dict) - словарь, в котором хранится количество времени для построения маршрута разной длительности.
        file_name(str) - имя файла для записию

    """

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(time_results, f, ensure_ascii=False, indent=4)


def read_performance_from_file(file_name='performance.json'):
    """
    Чтение результатов работы алгоритма из файла.

    Params:
        file_name(str) - имя файла для чтения.

    """

    with open(file_name, 'r', encoding='utf-8') as f:
        time_performance = json.load(f)
    return time_performance


def get_parser():
    """
    Извлечение значений переданных в консоль аргументов.
    Ключи соответствуют следующим функциям:
        -r: чтение предыдущих результатов работы теста из файла, заново тест не выполняется.
        -w: запись полученных результатов в файл.
        -d: построение графика с результатом работы алгоритма и сохранение графика в файл.
        -p: печать статистки в консоль.

    Returns:
        dict - словарь, в котором хранятся значения переданных ключей с соответствующими им значениями.

    """
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('-r', help='Read previous performance result from file', action='store_true')
    parser.add_argument('-w', help='Write result to file', action='store_true')
    parser.add_argument('-d', help='Draw statistics', action='store_true')
    parser.add_argument('-p', help='Print statistics', action='store_true')
    args = vars(parser.parse_args())
    return args


def get_request(start_lat, start_lng, duration, trip_type, need_return, tags, constraints):
    """
    Создание запроса для тестирования работы алгоритма.

    Params:
        start_lat(double) - широта стартовой точки.
        start_lng(double) - долгота стартовой точки.
        duration(int) - время маршрута.
        trip_type(str) - тип маршрута.
        need_return(str) - нужно ли возвращаться в стартовую точку('true' если нужно и 'false' в противном случае)
        tags(array-like of str) - теги маршрута.
        constraints(array-like of str) - ограничения.

    Return:
        ImmutableMultiDict - словарь с запросом.

    """

    return ImmutableMultiDict([
        ('start_lat', str(start_lat)),
        ('start_lng', str(start_lng)),
        ('duration', str(duration)),
        ('trip_type', trip_type),
        ('need_return', str(need_return)),
        ('tags', ','.join(tags)),
        ('constraints', ','.join(constraints))
    ])


def performance_test():
    """
    Тест на скорость работы алгоритма построения маршрута.
    Для заданных ограничений по времени и по категории мест для посещений алгоритм запускается несколько раз.
    Для статистической значимости лучше запускать 30 и более раз.

    Return:
        time_results(dict) - словарь, в котором хранится количество времени для построения маршрута разной длительности.

    """

    time_for_routes = [60, 120, 180]
    n_tries = 5
    time_results = {
        time_for_route: []
        for time_for_route in time_for_routes
    }

    min_lat = 52.50
    max_lat = 52.55
    min_lng = 13.34
    max_lng = 13.44

    # min_lat = 52.54
    # max_lat = 52.54
    # min_lng = 13.5
    # max_lng = 13.5

    trip_type = 'historic'
    need_return = 'false'
    tags = ['historic_historic', 'historic_archaeological', 'historic_tomb',
            'historic_military', 'historic_transport', 'historic_memorial', 'historic_city']
    constraints = [
        'food_restaurant', 'pharmacy'
    ]

    for time_for_route in time_for_routes:

        for _ in range(n_tries):
            start_lat = round(random.uniform(min_lat, max_lat), 4)
            start_lng = round(random.uniform(min_lng, max_lng), 4)

            request = get_request(
                start_lat=start_lat,
                start_lng=start_lng,
                duration=time_for_route,
                trip_type=trip_type,
                need_return=need_return,
                tags=tags,
                constraints=constraints,
            )
            print(request)
            start_time = time.time()
            routes = service.get_optimal_route(request)
            end_time = time.time()
            time_delta = end_time - start_time
            time_results[time_for_route].append(time_delta)

    return time_results


def main():
    args = get_parser()
    if args['r']:
        time_results = read_performance_from_file()
    else:
        time_results = performance_test()

    if args['p']:
        print_performance(time_results)

    if args['d']:
        draw_performance(time_results)

    if args['w']:
        write_performance_to_file(time_results)


if __name__ == '__main__':
    print('start performance test')
    main()
    print('end performance test')