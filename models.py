from flask_wtf import FlaskForm
from wtforms import validators, StringField
from wtforms.fields.html5 import TelField, EmailField


# Form data pasien, menggunakan plugin WTForm
class formPatient(FlaskForm):
    name = StringField('Name:', [validators.required()])
    address = StringField('Address:', [validators.optional()])
    phone = TelField('Phone:', [validators.required()])
    email = EmailField('Email address:', [validators.DataRequired(), validators.Email()])
    complaint = StringField('Complaint:', [validators.required()])
