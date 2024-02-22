from app import create_app, db

def create_tables():
    db.create_all()

if __name__ == "__main__":
    with create_app().app_context():
        create_tables()
    create_app().run(port=5000, debug=True)