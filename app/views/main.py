from flask import Blueprint, render_template, request, jsonify
from app.utils.logger import get_logger
from app.utils.config import config

main_bp = Blueprint('main', __name__)
logger = get_logger(__name__)


@main_bp.route('/')
def index():
    logger.info("Index page accessed")
    return render_template('index.html')


@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return jsonify({
        'status': 'healthy',
        'config_loaded': bool(config.config),
        'debug_mode': config.get('flask.debug', False)
    })


@main_bp.route('/config')
def show_config():
    """Display current configuration (for debugging)"""
    if not config.get('flask.debug', False):
        logger.warning("Config endpoint accessed in production mode")
        return jsonify({'error': 'Not available in production'}), 403

    logger.debug("Configuration requested")
    return jsonify({
        'flask': config.get_section('flask'),
        'logging': config.get_section('logging'),
        'features': config.get_section('features')
    })