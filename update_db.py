from app import create_app, db
from app.models import Aluno
import random
import string

app = create_app()

def gerar_matricula():
    # Gera uma matrícula no formato AAAA9999 (4 letras + 4 números)
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"{letras}{numeros}"

with app.app_context():
    print("🔄 Atualizando banco de dados...")
    
    # Verificar se a coluna matricula existe
    inspector = db.inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('aluno')]
    
    if 'matricula' not in columns:
        print("➕ Adicionando coluna 'matricula' à tabela 'aluno'...")
        # Usar a conexão direta do SQLAlchemy
        with db.engine.connect() as connection:
            connection.execute(db.text("ALTER TABLE aluno ADD COLUMN matricula VARCHAR(20)"))
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
            # Garantir que a matrícula seja única
            while Aluno.query.filter_by(matricula=matricula).first():
                matricula = gerar_matricula()
            aluno.matricula = matricula
            print(f"📝 Atribuindo matrícula {matricula} ao aluno {aluno.nome}")
        
        db.session.commit()
        print("✅ Matrículas geradas para todos os alunos existentes!")
    else:
        print("ℹ️ A coluna 'matricula' já existe na tabela 'aluno'")
    
    print("🎉 Atualização do banco de dados concluída!")