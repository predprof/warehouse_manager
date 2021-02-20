from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired


class InvoiceForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    size_z = IntegerField('size_x', validators=[DataRequired()])
    size_x = IntegerField('size_y', validators=[DataRequired()])
    size_y = IntegerField('size_z', validators=[DataRequired()])
    weight = IntegerField('weight', validators=[DataRequired()])
    submit = SubmitField('Save')