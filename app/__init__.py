from flask import Flask
from flask_caching import Cache

# Initialize Cache
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    # Initialize cache
    cache.init_app(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.reviews import reviews_bp
    from .routes.map import map_bp
    from .routes.root import root_bp
    from app.routes.search import search_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(root_bp, url_prefix='/')
    app.register_blueprint(map_bp, url_prefix='/map')
    app.register_blueprint(search_bp, url_prefix='/search')

    return app
