import json
import db
import operator


def init():
    # Очистка
    db.clean_items()
    # Инициализируем БД: схема склада
    init_storage_schema()
    # Инициализируем БД: тестовая накладная
    init_demo_items()


def init_storage_schema():
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
                                 volume=stowage_size_x * stowage_size_y * stowage_size_z,
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
                                 volume=basic_size * basic_size * basic_size,
                                 json=entry.replace("\"", ""),
                                 empty=True
                                 )
        db.add_stowage(new_stowage)

    # Добавление в БД ячейки, которая уловно обозначает удаленный склад
    new_stowage = db.Stowage(id=999999,
                             row="Remote",
                             level=1,
                             size_x=basic_size,
                             size_y=basic_size,
                             size_z=basic_size,
                             volume=basic_size * basic_size * basic_size,
                             json="no",
                             empty=False
                             )
    db.add_stowage(new_stowage)


def add_item(form):
    new_item = db.Item(name=form.name.data,
                       size_x=form.size_x.data,
                       size_y=form.size_y.data,
                       size_z=form.size_z.data,
                       weight=form.weight.data
                       )

    # Добавление в БД новой записи о товаре
    db.add_items(new_item)


# Распределяем товары
def load_items():
    # Получаем места
    stowages = db.get_stowages()
    # Получаем нераспределенные товары
    all_items = db.get_items()
    items = [i for i in all_items if i.stowage_id is None]
    # Сортировка ячеек по возрастанию объема
    stowages_sorted = sorted(stowages, key=operator.attrgetter('volume'))
    # Сортировка товаров по убыванию веса (на размещение прежде всего пойдут наиболее тяжелые товары)
    items_sorted_weight = sorted(items, key=operator.attrgetter('weight'), reverse=True)

    # Алгоритм выбора подходящей ячейки
    # По всем товарам
    for i in items_sorted_weight:
        stowages_suitable = []
        # По всем ячейкам
        for s in stowages_sorted:
            # Если ячейка пуста и подходит по размерам, то добавляем её в дополнительный массив
            if s.empty and \
                    ((i.size_x <= s.size_x) and (i.size_y <= s.size_y) and (i.size_z <= s.size_z)) \
                    or ((i.size_x <= s.size_y) and (i.size_y <= s.size_x) and (i.size_z <= s.size_z)):\
                    # or ((i.size_x <= s.size_x) and (i.size_y <= s.size_z) and (i.size_z <= s.size_y)):
                stowages_suitable.append(s)

        # Если подходящих ячеек 0, то размещаем на удаленный склад
        if len(stowages_suitable) == 0:
            i.stowage_id = 999999
            break

        # Сохраняем объем самой маленькой подходящей ячейки
        smallest_volume = stowages_suitable[0].volume
        print("smallest = ", smallest_volume)
        # Отбираем ячейки этого объема и сортируем этот набор по возрастанию высоты
        stowages_lowest = sorted((s for s in stowages_suitable if s.volume <= smallest_volume),
                                 key=operator.attrgetter('level'))
        # Размещаем тяжелые товары прежде всего
        i.stowage_id = stowages_lowest[0].id
        stowages_lowest[0].empty = False
        # Замершаем работу с БД
        db.put_item_in_stowage(i, stowages_lowest[0])
        # Сообщить манипулятору

    print("Loading complete!")


def unload_item(uid):
    print("Unloading ", uid)


# Добавление в БД демонстрационной накладной
def init_demo_items():
    db.clean_items()
    new_item = db.Item(name="Компьютер 1",size_x=900,size_y=900,size_z=300,weight=15)
    db.add_items(new_item)
    new_item = db.Item(name="Монитор",size_x=900,size_y=1500,size_z=50,weight=7)
    db.add_items(new_item)
    new_item = db.Item(name="Доска маркерная",size_x=1900,size_y=1100,size_z=900,weight=5)
    db.add_items(new_item)
