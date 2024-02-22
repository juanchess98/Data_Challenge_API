from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

# Function to upload data to the specified database table
def upload_to_db(data, table_name, schema):
        # Here, you may want to validate the schema and perform other checks
        # For simplicity, assuming the schema is valid and contains column mappings
        column_mapping = schema.get('column_mapping')

        # Insert data into the specified table
        table = db.Table(table_name, db.metadata, autoload=True, autoload_with=db.engine)
        columns = table.columns.keys()
        if len(columns) != len(column_mapping):
            raise ValueError('Schema does not match the table columns')
        
        mapped_data = [{column: row[index] for column, index in column_mapping.items()} for row in data]
        db.session.execute(table.insert(), mapped_data)
        db.session.commit()

# Function to create the app
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app