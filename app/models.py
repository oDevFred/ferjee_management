from . import db
from flask_login import UserMixin
from datetime import datetime

class Aluno(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
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
        print(f"🆕 Criando novo objeto aluno: {kwargs.get('nome', 'Sem nome')}")
        super().__init__(**kwargs)