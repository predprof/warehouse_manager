from flask import Flask, render_template
import storage_manager_olypm

app = Flask(__name__)


@app.route('/')
def hello_world():
    # return 'Hello World!'

    items_data = storage_manager_olypm.get_items()

    items = [(item.name, item.size_x, item.size_y, item.size_z, item.weight) for item in items_data]

    return render_template('main.html', items=items)


if __name__ == '__main__':
    app.run()
