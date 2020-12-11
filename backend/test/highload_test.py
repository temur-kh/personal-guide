import sys
import os
import requests
from flask import Flask, Blueprint, request, jsonify

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


if __name__ == '__main__':
    session = requests.Session()
    data = {
        'duration': '30',
        'tags': 'historic',
        'constraints': '',
        'start_lat': '52.5',
        'start_lng': '13.3',
    }
    response = session.post('http://127.0.0.1:9090/app/submit', data=data)
    print(response.text)
