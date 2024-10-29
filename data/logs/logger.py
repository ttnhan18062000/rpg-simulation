import logging


logging.basicConfig(
    level=logging.DEBUG,  # Set the log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Log to console
    ],
)


logger = logging.getLogger(__name__)
