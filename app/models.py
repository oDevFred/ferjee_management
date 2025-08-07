from . import db
from flask_login import UserMixin
from datetime import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash

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

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)

    def set_senha(self, senha):
        print(f"🔐 Gerando hash da senha para o usuário: {self.username}")
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        resultado = check_password_hash(self.senha_hash, senha)
        print(f"🔍 Verificando senha para o usuário: {self.username} - {'✅ Válida' if resultado else '❌ Inválida'}")
        return resultado

    def __repr__(self):
        print(f"👤 Representando usuário: {self.username} ({self.nome_completo})")
        return f'<Usuario {self.username}>'

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    duracao_meses = db.Column(db.Integer, nullable=False)
    valor_mensalidade = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    matriculas = db.relationship('Matricula', backref='curso', lazy=True)
    
    def __repr__(self):
        print(f"📚 Representando curso: {self.nome}")
        return f'<Curso {self.nome}>'

class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    data_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='ativo')  # ativo, concluido, cancelado, trancado
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamentos
    aluno = db.relationship('Aluno', backref='matriculas')
    
    def __repr__(self):
        print(f"📝 Representando matrícula: Aluno {self.aluno_id} no Curso {self.curso_id}")
        return f'<Matricula {self.id}>'