from flask import Blueprint, render_template
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/health')
def health_check():
    return {'status': 'ok', 'message': 'Sistema operacional'}

@bp.route('/alunos')
def listar_alunos():
    from .models import Aluno
    alunos = Aluno.query.all()
    return render_template('alunos/listar.html', alunos=alunos)