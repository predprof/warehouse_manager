from flask import Flask, render_template, redirect
import db
import controller
from config import Config
from forms import InvoiceForm

# Создаем экземпляр веб-приложения Flask
app = Flask(__name__, template_folder="template")
app.config.from_object(Config)

# Инициализация
controller.init()
print("Приложение готово к работе")

# Запуск веб-приложения
if __name__ == '__main__':
    app.run()


# Функция отрисовки главного экрана
@app.route('/', methods=['GET', 'POST'])
def main():
    print("Загружаю главную страницу")
    form1 = InvoiceForm()
    if form1.validate_on_submit():
        print("Обнаружены данные из формы")
        controller.add_item(form1)

    items_data = db.get_all_items()
    items = [(item.id, item.name, item.size_x, item.size_y, item.size_z, item.weight, item.stowage_id) for item in items_data]

    stowages_data = db.get_all_stowages()
    stowages = [(stowage.id, stowage.row, stowage.level, stowage.size_x, stowage.size_y, stowage.size_z, stowage.json, stowage.empty) for stowage in stowages_data]

    print("Загрузка главной страницы")
    return render_template('main.html', items=items, stowages=stowages, form1=form1)


# Функция размещения товаров на складе
@app.route('/load', methods=['POST'])
def load():
    print("Обнаружен запрос на загрузку нераспределенных товаров")
    controller.load_items()
    return redirect("/", code=302, Response=None)


# Функция выгрузки товара со склада
@app.route('/unload/<uuid:item_id>', methods=['POST'])
def unload(item_id):
    controller.unload_item(item_id)
    print("Обнаружен запрос на выгрузку товара с id ", item_id)
    return redirect("/", code=302, Response=None)
