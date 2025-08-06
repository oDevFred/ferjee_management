from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import Usuario

class FormLogin(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=80)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class FormRegistro(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=100)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(), EqualTo('senha', message='As senhas devem coincidir')
    ])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este e-mail já está em uso.')