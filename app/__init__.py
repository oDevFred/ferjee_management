from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar o Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Por enquanto, vamos retornar None, pois ainda não temos um modelo de usuário completo
        # Vamos implementar isso corretamente quando criarmos o modelo de usuário
        return None
    
    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app