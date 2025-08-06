from . import db
from flask_login import UserMixin
from datetime import datetime
import random

class Aluno(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(9), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        print(f"👤 Representando aluno: {self.nome} (Matrícula: {self.matricula})")
        return f'<Aluno {self.nome}>'
    
    def __init__(self, **kwargs):
        # Gerar matrícula automática se não for fornecida
        if 'matricula' not in kwargs or not kwargs['matricula']:
            kwargs['matricula'] = self.gerar_matricula()
        print(f"🆕 Criando novo objeto aluno: {kwargs.get('nome', 'Sem nome')} (Matrícula: {kwargs['matricula']})")
        super().__init__(**kwargs)
    
    @staticmethod
    def gerar_matricula():
        """Gera uma matrícula numérica única de 10 dígitos"""
        while True:
            # Gerar número aleatório de 10 dígitos
            matricula = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            # Verificar se já existe
            if not Aluno.query.filter_by(matricula=matricula).first():
                return matricula