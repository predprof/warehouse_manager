from flask import Flask, render_template
import db
import parse_schema_to_db

# Создаем экземпляр веб-приложения
app = Flask(__name__)
# Инициализируем БД схемы склада
parse_schema_to_db.init_schema()


@app.route('/')
def main():
    # return 'Hello World!'

    items_data = db.get_items()
    items = [(item.name, item.size_x, item.size_y, item.size_z, item.weight) for item in items_data]

    return render_template('main.html', items=items)


if __name__ == '__main__':
    # Запускаем веб-приложение
    app.run()
