"""
Artisan Dashboard — Main application entry point.

A Flask web application that helps artisans discover modern
market-relevant design trends and generate new product design
concepts while preserving traditional craft identity.

Run with:
    python app.py
"""

import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_app():
    """Application factory — creates and configures the Flask app."""

    app = Flask(__name__)

    # --- Configuration ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["DATABASE_URI"] = os.getenv("DATABASE_URI", "database/app.db")

    # --- Initialize database ---
    from models.concept_model import init_db
    with app.app_context():
        init_db()

    # --- Register blueprints ---
    from routes.main_routes import main_bp
    from routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # --- Ensure static directories exist ---
    os.makedirs(os.path.join(app.static_folder, "images", "generated"), exist_ok=True)

    return app


# --- Entry Point ---
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"

    print(f"\n  ✦ Artisan Dashboard running at http://localhost:{port}")
    print(f"  ✦ Debug mode: {'ON' if debug else 'OFF'}\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
