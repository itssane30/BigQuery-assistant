from flask import Flask

from app.config import Config
from app.routes.chat import chat_bp
from app.routes.health import health_bp
from app.utils.logger import get_logger
from flask_cors import CORS
from flask import render_template

logger = get_logger(__name__)

def create_app() -> Flask:
    """Flask application factory."""
    Config.validate()
    
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    
    CORS(app)
    app.config.from_object(Config)

    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    logger.info("Flask app created")
    return app
