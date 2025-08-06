from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    print("🚀 Inicializando aplicação Flask...")
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao')
    print("🔑 Configurando chave secreta da aplicação")
    
    # Configuração do banco de dados com caminho absoluto
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'instance')
    db_file = os.path.join(db_path, 'ferjee.db')
    
    # Garantir que a pasta instance exista
    try:
        os.makedirs(db_path)
        print(f"📁 Pasta instance criada em: {db_path}")
    except OSError:
        print(f"📁 Pasta instance já existe ou não foi possível criar: {db_path}")
    
    # Configurar URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(f"💾 Usando banco de dados em: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Inicializar extensões
    print("🔧 Inicializando extensões Flask...")
    db.init_app(app)
    login_manager.init_app(app)
    print("✅ Extensões inicializadas com sucesso!")
    
    # Configurar o Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        print(f"🔐 Carregando usuário com ID: {user_id}")
        from .models import Aluno
        return Aluno.query.get(int(user_id))
    
    # Não criar as tabelas automaticamente aqui
    # Elas serão criadas pelo script init_db.py
    
    # Registrar blueprints
    print("📋 Registrando blueprints...")
    from . import routes
    app.register_blueprint(routes.bp)
    print("✅ Blueprint registrado com sucesso!")
    
    print("🎉 Aplicação configurada com sucesso!")
    return app