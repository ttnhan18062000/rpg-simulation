import logging
import sys

# Set up logging with UTF-8 encoding for the StreamHandler
logging.basicConfig(
    level=logging.DEBUG,  # Set the log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    handlers=[
        logging.FileHandler(
            "app.log", encoding="utf-8"
        ),  # Log to a file with UTF-8 encoding
        logging.StreamHandler(sys.stdout),  # Log to console with default UTF-8 encoding
    ],
)

logger = logging.getLogger(__name__)

# Example log with special characters
logger.info("This is a test log with special characters: ñ, é, ü")
