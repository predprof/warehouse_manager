from flask import Flask, render_template, request
import db
import controller

# Создаем экземпляр веб-приложения
from config import Config
from forms import InvoiceForm

app = Flask(__name__)
app.config.from_object(Config)

# Инициализируем БД схемы склада
controller.init_schema()


# Модуль front-end: просмотр сведений
@app.route('/', methods=['GET', 'POST'])
def main():
    form1 = InvoiceForm()
    if form1.validate_on_submit():
        controller.load_items(form1)

    items_data = db.get_items()
    items = [(item.id, item.name, item.size_x, item.size_y, item.size_z, item.weight, item.stowage_id) for item in items_data]

    stowages_data = db.get_stowages()
    stowages = [(stowage.id, stowage.row, stowage.level, stowage.size_x, stowage.size_y, stowage.size_z, stowage.json, stowage.empty) for stowage in stowages_data]

    return render_template('main.html', items=items, stowages=stowages, form1=form1)


# Модуль размещение товаров на складе
@app.route('/put', methods=['POST'])
def load():
    projectpath = request.form['projectFilepath']
    return "/"


# Модуль выгрузки товара со склада
@app.route('/get', methods=['POST'])
def unload():
    projectpath = request.form['projectFilepath']
    return "/"


if __name__ == '__main__':
    # Запускаем веб-приложение
    app.run()
