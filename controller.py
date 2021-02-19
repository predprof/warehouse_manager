import json
import db
import forms


def init_schema():
    # Получение JSON-схемы
    json_schema = '{"size":{"size_x": 3,"size_y": 3,"size_z": 1},"merged":[["A1", "A2", "B1", "B2"],["B3", "C3"]]}'
    schema = json.loads(json_schema)

    # Буферный массив с ячейками базового размера
    alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
    numbers = "1234567890"
    basic_size = 1000
    buf = []
    x = 0
    while x < schema['size']['size_x']:
        y = 0
        while y < schema['size']['size_y']:
            buf.append(alphabet[x] + numbers[y])
            y += 1
        x += 1

    # Предварительная очистка таблицы ячеек
    db.clean_stowages()

    # Добавление в БД объединенных ячеек с фактическими размерами
    for merged in schema['merged']:
        stowage_size_x = basic_size
        stowage_size_y = basic_size
        stowage_size_z = basic_size
        if len(merged) >= 2:
            stowage_size_x = basic_size * 2

        if len(merged) == 4:
            stowage_size_y = basic_size * 2

        print(merged)

        new_stowage = db.Stowage(name=merged[0],
                                 size_x=stowage_size_x,
                                 size_y=stowage_size_y,
                                 size_z=stowage_size_z,
                                 # _json="\"merged\":" + merged
                                 json=merged
                                 )
        db.add_stowage(new_stowage)

        # Удаление обьединенных ячеек из буферного массива (останутся только необъединенные)
        res = [i for i in buf if i not in merged]
        buf = res
    # Добавление в БД оставшихся ячеек базового размера
    for entry in buf:
        new_stowage = db.Stowage(name=entry,
                                 size_x=basic_size,
                                 size_y=basic_size,
                                 size_z=basic_size,
                                 json=entry.replace("\"", "")
                                 )
        db.add_stowage(new_stowage)


def load_items(new_item):

    print("Loading!", new_item)
    db.add_items(new_item)


def unload_item(uid):
    print("Unloading ", uid)
