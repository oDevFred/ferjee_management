from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import sys

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Configuração do banco de dados com caminho absoluto
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'instance')
    db_file = os.path.join(db_path, 'ferjee.db')
    
    # Garantir que a pasta instance exista
    try:
        os.makedirs(db_path)
        print(f"Pasta instance criada em: {db_path}")
    except OSError:
        print(f"Pasta instance já existe ou não foi possível criar: {db_path}")
    
    # Configurar URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"Usando banco de dados em: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar o Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Aluno
        return Aluno.query.get(int(user_id))
    
    # Criar as tabelas do banco de dados
    with app.app_context():
        try:
            db.create_all()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
    
    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app