import os
import logging
from app import create_app
from app.models.db import init_db  # Import your database initialization function

# Initialize the Flask app
app = create_app()


def setup_logging():
    """
    Configure logging for the application.
    Logs to a file in production mode.
    """
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        handler = logging.FileHandler("app.log")  # Log to a file
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)

if __name__ == "__main__":
    # Set environment
    env = os.getenv("FLASK_ENV", "development")
    debug = env == "development"

    # Setup logging
    setup_logging()

    # Initialize the database
    if debug:
        print("Initializing the database...")
    init_db()

    # Run the Flask application
    app.run(debug=debug, host="0.0.0.0", port=5000)
