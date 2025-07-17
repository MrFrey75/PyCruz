from app import create_app
from app.utils.config import config
from app.utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == '__main__':
    app = create_app()

    host = config.get('flask.host', '127.0.0.1')
    port = config.get('flask.port', 5000)
    debug = config.get('flask.debug', False)

    logger.info(f"Starting server on {host}:{port} (debug={debug})")

    try:
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.critical(f"Failed to start server: {e}")
        raise