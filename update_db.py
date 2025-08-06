from app import create_app, db
from app.models import Aluno
import random

app = create_app()

def gerar_matricula():
    """Gera uma matrícula numérica única de 10 dígitos"""
    while True:
        # Gerar número aleatório de 10 dígitos
        matricula = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        # Verificar se já existe
        if not Aluno.query.filter_by(matricula=matricula).first():
            return matricula

with app.app_context():
    print("🔄 Atualizando banco de dados...")
    
    # Verificar se a coluna matricula existe
    inspector = db.inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('aluno')]
    
    if 'matricula' not in columns:
        print("➕ Adicionando coluna 'matricula' à tabela 'aluno'...")
        # Usar a conexão direta do SQLAlchemy
        with db.engine.connect() as connection:
            connection.execute(db.text("ALTER TABLE aluno ADD COLUMN matricula VARCHAR(10)"))
            connection.commit()
        print("✅ Coluna 'matricula' adicionada com sucesso!")
        
        # Adicionar constraint UNIQUE
        with db.engine.connect() as connection:
            connection.execute(db.text("CREATE UNIQUE INDEX idx_aluno_matricula ON aluno (matricula)"))
            connection.commit()
        print("✅ Constraint UNIQUE adicionada à coluna 'matricula'!")
        
        # Gerar matrículas para alunos existentes
        alunos = Aluno.query.all()
        for aluno in alunos:
            matricula = gerar_matricula()
            aluno.matricula = matricula
            print(f"📝 Atribuindo matrícula {matricula} ao aluno {aluno.nome}")
        
        db.session.commit()
        print("✅ Matrículas geradas para todos os alunos existentes!")
    else:
        print("ℹ️ A coluna 'matricula' já existe na tabela 'aluno'")
        
        # Verificar se as matrículas existentes são numéricas
        alunos = Aluno.query.all()
        for aluno in alunos:
            if not aluno.matricula or not aluno.matricula.isdigit():
                nova_matricula = gerar_matricula()
                aluno.matricula = nova_matricula
                print(f"🔄 Atualizando matrícula do aluno {aluno.nome} para {nova_matricula}")
        
        db.session.commit()
        print("✅ Matrículas atualizadas para formato numérico!")
    
    print("🎉 Atualização do banco de dados concluída!")