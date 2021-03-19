import os

import requests
import json

# Для локального запуска
# manipulator_url_get_scheme = 'https://run.mocky.io/v3/ae75fa43-17cd-49a1-bd10-bf76fd3c40dd'
# manipulator_url_post_load = 'https://run.mocky.io/v3/0e1bf89d-e50a-4347-a713-ea8c8389c9bd'
# manipulator_url_get_unload = 'https://run.mocky.io/v3/0e1bf89d-e50a-4347-a713-ea8c8389c9bd'
# Для запуска через heroku
manipulator_url_get_scheme = os.getenv("URL_TO_GET_SCHEME")
manipulator_url_post_load = os.getenv("URL_TO_GET_STATUS_OK")
manipulator_url_get_unload = os.getenv("URL_TO_GET_STATUS_OK")


# Получить JSON-схему от манипулятора
def get_scheme():
    # Запрашиваем у манипулятора схему. Результат в формате JSON возвращаем
    res = requests.get(manipulator_url_get_scheme)
    return res.json()


# Загрузить товар на склад
def load(item_id, destination):
    data = {"uuid": str(item_id),
            "destination": destination}
    data_json = json.dumps(data)
    payload = {"json_payload": data_json}
    res = requests.post(manipulator_url_post_load, payload)
    return res.json()


# Выгрузить товар со склада
def unload(destination):
    print("Unloading from stowage with destination json ", destination)
    data = {"destination": destination}
    data_json = json.dumps(data)
    payload = {"json_payload": data_json}
    res = requests.get(manipulator_url_get_unload, payload)
    return res
