from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField
from wtforms.fields.html5 import TelField, EmailField


class formMember(FlaskForm):
    name = StringField('Name:', [validators.required()])
    address = StringField('Address:', [validators.optional()])
    phone = TelField('Phone:', [validators.required()])
    email = EmailField('Email address:', [validators.DataRequired(), validators.Email()])
