from app import create_app, db
from app.models import Aluno

app = create_app()

with app.app_context():
    print("🔍 Verificando o banco de dados...")
    
    # Verificar se a tabela aluno existe
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tabelas no banco de dados: {tables}")
    
    if 'aluno' in tables:
        print("✅ Tabela 'aluno' encontrada!")
        
        # Contar alunos
        count = Aluno.query.count()
        print(f"🔢 Total de alunos no banco: {count}")
        
        # Listar alunos
        alunos = Aluno.query.all()
        for aluno in alunos:
            print(f"👤 Aluno: {aluno.nome} (ID: {aluno.id})")
    else:
        print("❌ Tabela 'aluno' não encontrada!")