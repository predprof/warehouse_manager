# Модули python.
# operator - для упорядочивания по определенному параметру, зная его имя
import operator

# Наши модули
import db
import manipulator


# Общая инициализация + инициализация БД
def init():
    # Получение JSON-схемы
    scheme = manipulator.get_scheme()
    # Если получить схему у манипулятора удалось, то:
    if len(scheme) > 0:
        # Инициализируем схемы склада в БД
        init_storage_scheme(scheme)
        print("Схема склада обновлена!")
    # Очистка БД
    db.clean_items()
    # Инициализируем БД: тестовая накладная
    init_demo_items()
    print("Тестовые товары занесены")


# Инициализация схемы склада в БД из схемы, которую прислал манипулятор
def init_storage_scheme(scheme):
    print("Инициализирую схему склада")
    # Создаем буферный массив с ячейками базового размера (единичные) и гененируем им правильные имена
    alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
    numbers = "1234567890"
    basic_size = 1000
    buf = []
    x = 0
    while x < scheme['size']['size_x']:
        y = 0
        while y < scheme['size']['size_y']:
            buf.append(alphabet[x] + numbers[y])
            y += 1
        x += 1

    # Предварительная очистка таблицы ячеек
    db.clean_stowages()

    # Добавление в БД объединенных ячеек с фактическими размерами (двойными и четверными)
    for merged in scheme['merged']:
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

        # Удаление обьединенных ячеек из буферного массива (останутся только необъединенные, единичного размера)
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
    # (добавлена для того, чтобы не выносить признак удаленного склада в отдельный столбец)
    new_stowage = db.Stowage(id=999999,
                             row="Remote",
                             level=1,
                             size_x=basic_size*10,
                             size_y=basic_size*10,
                             size_z=basic_size*10,
                             volume=basic_size * basic_size * basic_size * 1000,
                             json="no",
                             empty=False
                             )
    db.add_stowage(new_stowage)
    print("Схема склада готова!")


# Добавляем в накладную новый товар из полученной от front-end формы
def add_item(form):
    print("Добавляю новый товар в наколадную")
    new_item = db.Item(name=form.name.data,
                       size_x=form.size_x.data,
                       size_y=form.size_y.data,
                       size_z=form.size_z.data,
                       weight=form.weight.data
                       )

    # Добавление в БД новой записи о товаре
    db.add_item(new_item)
    print("Товар добавлен")


# Распределяем и загружаем товары
def load_items():
    # Получаем нераспределенные товары и сортируем их по убыванию веса
    all_items = db.get_all_items()
    items = [i for i in all_items if i.stowage_id is None]
    items_sorted_weight = sorted(items, key=operator.attrgetter('weight'), reverse=True)

    # Перебираем товары и определяем набор подходящих ячеек для каждого товара
    for i in items_sorted_weight:
        print("Загрузка нераспределенных товаров")
        # Получаем пустые ячейки и сортируем их по возрастанию объема
        all_stowages = db.get_all_stowages()
        stowages = [s for s in all_stowages if s.empty is True]
        stowages_sorted = sorted(stowages, key=operator.attrgetter('volume'))

        # Перебираем все ячейки
        stowages_suitable = []
        for s in stowages_sorted:
            # Если ячейка всё еще пуста и подходит по размерам, то добавляем её в дополнительный массив
            if s.empty:
                if ((i.size_x <= s.size_x) and (i.size_y <= s.size_y) and (i.size_z <= s.size_z)) \
                        or ((i.size_x <= s.size_y) and (i.size_y <= s.size_x) and (i.size_z <= s.size_z)):
                    # or ((i.size_x <= s.size_x) and (i.size_y <= s.size_z) and (i.size_z <= s.size_y)):
                    stowages_suitable.append(s)

        # Если подходящих ячеек не нашлось, то размещаем на удаленный склад
        if len(stowages_suitable) == 0:
            i.stowage_id = 999999
            break
            # TODO: Большие тяжелые товары уходят на удаленный склад и прерывают поиск места для остальных. ИСправить

        # Сохраняем объем самой маленькой подходящей ячейки
        smallest_volume = stowages_suitable[0].volume

        # Отбираем ячейки этого объема и сортируем этот набор по возрастанию высоты
        stowages_lowest = sorted((s for s in stowages_suitable if s.volume <= smallest_volume),
                                 key=operator.attrgetter('level'))
        # Размещаем тем самым тяжелый товар прежде всего
        i.stowage_id = stowages_lowest[0].id
        stowages_lowest[0].empty = False
        # Замершаем работу с БД
        db.load_item_in_stowage(i, stowages_lowest[0])
        # Сообщить манипулятору



def unload_item(uid):
    db.unload_item_from_stowage(uid)
    print("Unloading ", uid)


# Добавление в БД демонстрационной накладной
def init_demo_items():
    db.clean_items()
    new_item = db.Item(name="Компьютер 1", size_x=900, size_y=900, size_z=300, weight=15)
    db.add_item(new_item)
    new_item = db.Item(name="Монитор", size_x=900, size_y=1500, size_z=50, weight=7)
    db.add_item(new_item)
    new_item = db.Item(name="Доска маркерная", size_x=1900, size_y=1100, size_z=900, weight=5)
    db.add_item(new_item)
