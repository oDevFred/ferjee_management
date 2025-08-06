from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao')
    
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
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar o Flask-Login
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Usuario
        user = Usuario.query.get(int(user_id))
        if user:
            print(f"🔐 Carregando usuário: {user.username}")
        return user
    
    # Não criar as tabelas automaticamente aqui
    # Elas serão criadas pelo script init_db.py
    
    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app