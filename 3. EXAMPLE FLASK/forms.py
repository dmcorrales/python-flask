from flask_wtf import FlaskForm
from wtforms.validators import ( DataRequired, ValidationError, Email, Regexp, Length, EqualTo )
import User

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Ya existe un usuario con ese nombre')

def email_exists(form, field)
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Ya existe un usuario con ese correo')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$'
            ),
            name_exists
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8,max=233),
            EqualTo('password2', message = 'Los passwords debe coincidir')
        ]
    )

    password2 = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
        ]
    )