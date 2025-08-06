from flask import Flask
from app import create_app, db
from app.models import Aluno
import os

print("🚀 Iniciando script de inicialização do banco de dados...")
app = create_app()

with app.app_context():
    # Verificar se o arquivo do banco de dados existe
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_uri.replace('sqlite:///', '')
    
    print(f"📂 Caminho do banco de dados: {db_path}")
    print(f"🔍 O arquivo do banco de dados existe? {os.path.exists(db_path)}")
    
    # Criar as tabelas
    print("🛠️ Criando tabelas no banco de dados...")
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar se a tabela aluno foi criada
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tabelas no banco de dados: {tables}")
    
    if 'aluno' in tables:
        print("👤 Tabela 'aluno' encontrada no banco de dados!")
    else:
        print("❌ ERRO: Tabela 'aluno' não foi encontrada no banco de dados!")
    
    print("🎉 Script de inicialização concluído com sucesso!")