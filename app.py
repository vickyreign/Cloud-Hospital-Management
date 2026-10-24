import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import config_by_name
from models import db, login_manager

csrf = CSRFProtect()


def create_app(config_name=None):
    """Application factory for MediCloud Hospital Management System."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.patients import patients_bp
    from routes.doctors import doctors_bp
    from routes.appointments import appointments_bp
    from routes.medical_records import medical_records_bp
    from routes.billing import billing_bp
    from routes.api import api_bp

    # Exempt REST API blueprint from CSRF for seamless API usage and tests
    csrf.exempt(api_bp)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(medical_records_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(api_bp)

    # Context processors
    @app.context_processor
    def inject_global_data():
        return {
            'app_name': 'MediCloud HMS',
            'hospital_name': 'MediCloud Multi-Specialty Hospital',
            'current_year': 2026
        }

    # Custom error handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # CLI command to initialize database
    @app.cli.command("init-db")
    def init_db_command():
        """Creates database tables."""
        with app.app_context():
            db.create_all()
            print("Database initialized successfully.")

    # CLI command to seed demo data
    @app.cli.command("seed-db")
    def seed_db_command():
        """Seeds realistic demo data."""
        from seed import seed_all_data
        with app.app_context():
            seed_all_data()
            print("Demo data seeded successfully.")

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
