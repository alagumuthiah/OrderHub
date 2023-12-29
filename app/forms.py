from flask_wtf import FlaskForm
from wtforms.fields import StringField,PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    employee_number	= StringField('Employee Number',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")

class MenuItemAssignmentForm(FlaskForm):
    menu_items = SelectMultipleField("Menu items", coerce=int)
