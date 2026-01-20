from app import app, db

def init_database():
    """Inicializar a base de dados"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("Base de dados inicializada com sucesso!")
        print("Tabelas criadas: users, contents")

if __name__ == '__main__':
    init_database()
