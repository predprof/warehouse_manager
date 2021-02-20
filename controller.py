import json
import db
import operator


def init_schema():
    # ��������� JSON-�����
    json_schema = '{"size":{"size_x": 3,"size_y": 3,"size_z": 1},"merged":[["A1", "A2", "B1", "B2"],["B3", "C3"]]}'
    schema = json.loads(json_schema)

    # �������� ������ � �������� �������� �������
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

    # ��������������� ������� ������� �����
    db.clean_stowages()

    # ���������� � �� ������������ ����� � ������������ ���������
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
                                 volume=stowage_size_x*stowage_size_y*stowage_size_z,
                                 json=merged,
                                 empty=True
                                 )
        db.add_stowage(new_stowage)

        # �������� ������������ ����� �� ��������� ������� (��������� ������ ��������������)
        res = [i for i in buf if i not in merged]
        buf = res

    # ���������� � �� ���������� ����� �������� �������
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


def add_item(form):
    new_item = db.Item(name=form.name.data,
                       size_x=form.size_x.data,
                       size_y=form.size_y.data,
                       size_z=form.size_z.data,
                       weight=form.weight.data
                       )

    # ���������� � �� ����� ������ � ������
    db.add_items(new_item)


# ������������ ������
def load_items():
    # �������� ��������� �����
    stowages = db.get_stowages()

    # �������� ���������������� ������
    all_items = db.get_items()
    items = [i for i in all_items if i.stowage_id is None]

    # ������ ������ 30�� ��������� ������ �����, ��� ����� ����
    heavy = [i for i in all_items if i.weight >= 30]
    light = [i for i in all_items if i.weight < 30]

    stowages_sorted = sorted(stowages, key=operator.attrgetter('volume'))
    items_sorted_weight = sorted(items, key=operator.attrgetter('weight'), reverse=True)

    for s in stowages_sorted:
        print(s.volume)

    for i in items_sorted_weight:
        print(i.weight)

    for i in items_sorted_weight:
        for s in stowages_sorted:
            if s.empty & (i.size_x <= s.size_x) & (i.size_y <= s.size_y) & (i.size_z <= s.size_z):
                i.stowage_id = s.id
                s.empty = False
                # �������� ������������
                break

    print("Loading ")


def unload_item(uid):
    print("Unloading ", uid)
