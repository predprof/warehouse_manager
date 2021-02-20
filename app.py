from flask import Flask, render_template, request, redirect, url_for
import db
import controller

# ������� ��������� ���-����������
from config import Config
from forms import InvoiceForm

app = Flask(__name__)
app.config.from_object(Config)

# �������������� �� ����� ������
controller.init_schema()


# ������ front-end: �������� ��������
@app.route('/', methods=['GET'])
def main():
    form1 = InvoiceForm()
    if form1.validate_on_submit():
        controller.add_item(form1)

    items_data = db.get_items()
    items = [(item.id, item.name, item.size_x, item.size_y, item.size_z, item.weight, item.stowage_id) for item in items_data]

    stowages_data = db.get_stowages()
    stowages = [(stowage.id, stowage.row, stowage.level, stowage.size_x, stowage.size_y, stowage.size_z, stowage.json, stowage.empty) for stowage in stowages_data]

    return render_template('main.html', items=items, stowages=stowages, form1=form1)


# ������ ���������� ������� �� ������
@app.route('/put', methods=['POST'])
def load():
    print("Loading!!!")
    controller.load_items()
    return redirect("/", code=302, Response=None)


# ������ �������� ������ �� ������
@app.route('/get', methods=['POST'])
def unload():
    print("Unloading!!!")

    return redirect("/", code=302, Response=None)


if __name__ == '__main__':
    # ��������� ���-����������
    app.run()
