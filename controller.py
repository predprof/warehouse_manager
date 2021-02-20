import json
import db


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

        new_stowage = db.Stowage(row=merged[0][0],
                                 level=int(merged[0][1]),
                                 size_x=stowage_size_x,
                                 size_y=stowage_size_y,
                                 size_z=stowage_size_z,
                                 volume=stowage_size_x*stowage_size_y*stowage_size_x,
                                 json=merged,
                                 empty=True
                                 )
        db.add_stowage(new_stowage)

        # Удаление обьединенных ячеек из буферного массива (останутся только необъединенные)
        res = [i for i in buf if i not in merged]
        buf = res

    # Добавление в БД оставшихся ячеек базового размера
    for entry in buf:
        new_stowage = db.Stowage(row=entry[0],
                                 level=int(entry[1]),
                                 size_x=basic_size,
                                 size_y=basic_size,
                                 size_z=basic_size,
                                 volume=basic_size*basic_size*basic_size,
                                 json=entry.replace("\"", ""),
                                 empty=True
                                 )
        db.add_stowage(new_stowage)


def load_items(form):
    print("Loading new item!")
    new_item = db.Item(name=form.name.data,
                       size_x=form.size_x.data,
                       size_y=form.size_y.data,
                       size_z=form.size_z.data,
                       weight=form.weight.data
                       )

    # Логика выбора места
    stowages = db.get_stowages()
    # stowages.sort
    # for stowage in stowages:
    # if stowage.empty == True:


    # Добавление в БД новой записи о товаре
    db.add_items(new_item)


def unload_item(uid):
    print("Unloading ", uid)
