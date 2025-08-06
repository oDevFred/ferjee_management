from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/health')
def health_check():
    return {'status': 'ok', 'message': 'Sistema operacional'}