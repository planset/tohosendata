import os

srcdirpath = os.path.abspath('./tohosen_pdf')
destdirpath = os.path.abspath('./tohosen_text')

BASE_URL = 'http://www.city.sapporo.jp/st/subway/route_time/documents/{filename}'


def read_station():
    import json
    with open('station.json') as f:
        return json.load(f)

stations = read_station()

