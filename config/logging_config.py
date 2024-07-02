from loguru import logger


def configure_logger():
    """
    Configures the logger to save logs to a file with rotation.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger.add(
        "debug.log", rotation="1 MB"
    )  # Save all the logs in an archive. Rotation happens when it gets at 1 MB.
    return logger
