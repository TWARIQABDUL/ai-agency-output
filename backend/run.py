from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        if app.config['DEBUG']:
            app.config['SECRET_KEY'] = 'super-secret-dev-key-ONLY-FOR-DEV'
            print("WARNING: SECRET_KEY not set. Using a default for development ONLY.", file=sys.stderr)
        else:
            print("ERROR: SECRET_KEY environment variable not set. This is critical for production security.", file=sys.stderr)
            sys.exit(1)
    else:
        app.config['SECRET_KEY'] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    print(f"Database configured for URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    cors_origins_env = os.environ.get('CORS_ORIGINS')

    if app.config['DEBUG']:
        if not cors_origins_env:
            allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
            print(f"WARNING: CORS_ORIGINS not set in debug mode. Defaulting to {allowed_origins}", file=sys.stderr)
        else:
            allowed_origins = [origin.strip() for origin in cors_origins_env.split(',')]
            print(f"DEBUG: CORS_ORIGINS set to {allowed_origins}")
        CORS(app, supports_credentials=True, origins=allowed_origins)
    else:
        if not cors_origins_env:
            print("ERROR: CORS_ORIGINS environment variable not set. This is critical for production security.", file=sys.stderr)
            sys.exit(1)
        allowed_origins = [origin.strip() for origin in cors_origins_env.split(',')]
        CORS(app, supports_credentials=True, origins=allowed_origins)
        print(f"CORS initialized with restricted origins: {allowed_origins}")

    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route('/status')
    def status():
        return jsonify({"message": "API is running!", "status": "ok"})
    
    app.register_blueprint(api_bp)
    print("API blueprints registered.")

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the backend service!", "version": "1.0"})

    return app

if __name__ == '__main__':
    app = create_app()
    # For initial development setup, create tables if running directly in debug mode.
    # In production, use a dedicated migration tool (e.g., Flask-Migrate or Alembic).
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()
            print("DEBUG: Database tables created (development mode).")

    app.run(host='0.0.0.0', port=5000)