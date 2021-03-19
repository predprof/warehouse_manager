import os

import requests
import json

# Если запускаемся с Heroku, то срабатывают перменные среды, иначе - задаем сами

if os.getenv("URL_TO_GET_SCHEME") is None:
    manipulator_url_get_scheme = 'https://run.mocky.io/v3/ae75fa43-17cd-49a1-bd10-bf76fd3c40dd'
else:
    manipulator_url_get_scheme = os.getenv("URL_TO_GET_SCHEME")

if os.getenv("URL_TO_LOAD") is None:
    manipulator_url_post_load = 'https://run.mocky.io/v3/0e1bf89d-e50a-4347-a713-ea8c8389c9bd'
else:
    manipulator_url_post_load = os.getenv("URL_TO_LOAD")

if os.getenv("URL_TO_UNLOAD") is None:
    manipulator_url_get_unload = 'https://run.mocky.io/v3/0e1bf89d-e50a-4347-a713-ea8c8389c9bd'
else:
    manipulator_url_get_unload = os.getenv("URL_TO_UNLOAD")


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
    print("JSON payload:", payload)
    res = requests.post(manipulator_url_post_load, payload)
    return res.json()


# Выгрузить товар со склада
def unload(destination):
    print("Unloading from stowage with destination json ", destination)
    data = {"destination": destination}
    data_json = json.dumps(data)
    payload = {"json_payload": data_json}
    print("JSON payload:", payload)
    res = requests.get(manipulator_url_get_unload, payload)
    return res.json()
