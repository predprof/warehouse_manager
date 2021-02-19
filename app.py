from flask import Flask, render_template, request
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
@app.route('/', methods=['GET', 'POST'])
def main():
    items_data = db.get_items()
    items = [(item.id, item.name, item.size_x, item.size_y, item.size_z, item.weight) for item in items_data]

    stowages_data = db.get_stowages()
    stowages = [(stowage.name, stowage.size_x, stowage.size_y, stowage.size_z, stowage.json) for stowage in stowages_data]

    form1 = InvoiceForm()
    # form2 = InvoiceForm()
    # form3 = InvoiceForm()
    # forms = ListForms()
    if form1.validate_on_submit():
        controller.load_items(form1)
        print(form1.name)
        print("YYYY")

    return render_template('main.html', items=items, stowages=stowages, form1=form1)

#
# # ������ front-end: ���������� ������� �� ������
# @app.route('/put', methods=['POST'])
# def handle_data():
#     projectpath = request.form['projectFilepath']
#     return render_template()
#
#
# # ������ front-end: �������� ������� �� ������
# @app.route('/get', methods=['POST'])
# def handle_data():
#     projectpath = request.form['projectFilepath']
#     # your code
#     # return a response


if __name__ == '__main__':
    # ��������� ���-����������
    app.run()
