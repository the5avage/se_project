from app.routes.auth import auth_bp
from app.routes.reviews import reviews_bp
from app.routes.map import map_bp


from app.entities.db import init_db

# Initialize the database before starting the app
init_db()