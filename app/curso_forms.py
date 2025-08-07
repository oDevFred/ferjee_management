from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class FormCurso(FlaskForm):
    nome = StringField('Nome do Curso', validators=[DataRequired(), Length(min=3, max=100)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    duracao_meses = IntegerField('Duração (meses)', validators=[DataRequired(), NumberRange(min=1, max=60)])
    valor_mensalidade = FloatField('Valor da Mensalidade (R$)', validators=[DataRequired(), NumberRange(min=0)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar Curso')

class FormMatricula(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int, validators=[DataRequired()])
    curso_id = SelectField('Curso', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('ativo', 'Ativo'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('trancado', 'Trancado')
    ], validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Matricular Aluno')