import sys
import os
import requests
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Для удобства эти переменные сделаны глобальными
server_name = 'http://127.0.0.1:9090/api/submit'
request_data = {
    'duration': None,
    'tags': 'historic',
    'constraints': '',
    'start_lat': '52.5',
    'start_lng': '13.3',
}
successful_requests = []


def request_to_server():
    """
    Post апрос к серверу.

    Return:
        response - ответ от сервера.
    """
    session = requests.Session()
    response = session.post(server_name, data=request_data)
    is_successful_request = (response.status_code == 200)
    successful_requests.append(is_successful_request)
    return response


async def do_requests_async(num_requests):
    """
    Асинхронное выполнение запросов.

    Params:
        num_requests(int) - количество запросов.

    """

    with ThreadPoolExecutor(max_workers=100) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request_to_server,
                )
                for _ in range(num_requests)
            ]
            for _ in await asyncio.gather(*tasks):
                pass


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
    parser.add_argument('-d', help='Duration')
    parser.add_argument('-n', help='Number of request')
    parser.add_argument('-async', help='Run requests in async way', action='store_true')
    parser.add_argument('-p', help='Print results in console', action='store_true')
    args = vars(parser.parse_args())
    return args


def test_async(num_requests):
    """
    Асинхронное тестирование кода.

    Params:
        num_requests(int) - количество запросов.

    """

    start_time = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(do_requests_async(num_requests))
    loop.run_until_complete(future)
    end_time = time.time()
    return end_time - start_time


def test_seq(num_requests):
    """
    Последовательное тестирование кода.

    Params:
        num_requests(int) - количество запросов.

    """

    start_time = time.time()
    for _ in range(num_requests):
       _ = request_to_server()
    end_time = time.time()
    return end_time - start_time


def main():
    args = get_parser()
    num_requests = int(args['n'])
    duration = args['d']
    request_data['duration'] = duration

    if args['async']:
        time_results = test_async(num_requests)
    else:
        time_results = test_seq(num_requests)

    print('{} from {} were successful'.format(sum(successful_requests), num_requests))
    print('Time elapsed: {:.2f} seconds'.format(time_results))


if __name__ == '__main__':
    main()

