from flask import Blueprint, render_template, request, jsonify
from app.utils.logger import get_logger
from app.utils.config import config

main_bp = Blueprint('main', __name__)
logger = get_logger(__name__)


@main_bp.route('/')
def index():
    logger.info("Index page accessed")
    return render_template('index.html')


