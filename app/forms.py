from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, ValidationError
import re

class FormAluno(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired(), Length(min=3, max=20)])
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=100)])
    rg = StringField('RG', validators=[Optional(), Length(max=20)])
    cpf = StringField('CPF', validators=[Optional(), Length(min=11, max=14)])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[Optional()])
    email = StringField('E-mail', validators=[Optional(), Email()])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    endereco = StringField('Endereço', validators=[Optional(), Length(max=200)])
    bairro = StringField('Bairro', validators=[Optional(), Length(max=100)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado', choices=[
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], validators=[Optional()])
    cep = StringField('CEP', validators=[Optional(), Length(min=8, max=9)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Cadastrar Aluno')
    
    def validate_cpf(self, cpf):
        if cpf.data:
            # Remover caracteres não numéricos
            cpf_clean = re.sub(r'[^0-9]', '', cpf.data)
            
            if len(cpf_clean) != 11:
                raise ValidationError('CPF deve ter 11 dígitos')
            
            # Verificar se todos os dígitos são iguais
            if cpf_clean == cpf_clean[0] * 11:
                raise ValidationError('CPF inválido')
            
            # Cálculo do primeiro dígito verificador
            soma = 0
            for i in range(9):
                soma += int(cpf_clean[i]) * (10 - i)
            resto = 11 - (soma % 11)
            if resto == 10 or resto == 11:
                digito1 = 0
            else:
                digito1 = resto
            
            # Cálculo do segundo dígito verificador
            soma = 0
            for i in range(10):
                soma += int(cpf_clean[i]) * (11 - i)
            resto = 11 - (soma % 11)
            if resto == 10 or resto == 11:
                digito2 = 0
            else:
                digito2 = resto
            
            # Verificar se os dígitos verificadores estão corretos
            if int(cpf_clean[9]) != digito1 or int(cpf_clean[10]) != digito2:
                raise ValidationError('CPF inválido')
    
    def validate_telefone(self, telefone):
        if telefone.data:
            # Remover caracteres não numéricos
            tel_clean = re.sub(r'[^0-9]', '', telefone.data)
            
            if len(tel_clean) < 10 or len(tel_clean) > 11:
                raise ValidationError('Telefone inválido')