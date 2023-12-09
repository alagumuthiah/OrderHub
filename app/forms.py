from flask_wtf import FlaskForm
from wtforms.fields import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    employee_number	= StringField('Employee Number',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')
