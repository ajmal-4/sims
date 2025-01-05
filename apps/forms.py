from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, FieldList, FormField, validators

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[validators.DataRequired()])
    quantity = IntegerField('Quantity', validators=[validators.DataRequired()])
    price = FloatField('Price', validators=[validators.DataRequired()])

class InvoiceForm(FlaskForm):
    products = FieldList(FormField(ProductForm), min_entries=1)
    submit = SubmitField('Create Invoice')