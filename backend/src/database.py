from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
_app_instance = None

def init_app(app):
    global _app_instance
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    _app_instance = app

def create_db():
    if _app_instance is None:
        raise RuntimeError("Application not initialized. Call init_app(app) first.")
    with _app_instance.app_context():
        db.create_all()