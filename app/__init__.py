from flask import Flask
from app.utils.config import config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # Configure Flask from JSON config
    app.config['SECRET_KEY'] = config.get('flask.secret_key')
    app.config['DEBUG'] = config.get('flask.debug', False)

    logger.info("Starting Flask application")

    # Register blueprints
    from app.views.main import main_bp
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 error: {error}")
        return "Page not found", 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        return "Internal server error", 500

    logger.info("Flask application initialized successfully")
    return app