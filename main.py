from config.config import load_config
from config.logging_config import configure_logger
from scraper.scraper import NewsScraper
from robocorp.tasks import task

# Configure logger
logger = configure_logger()

@task
def main():
    """
    Main entry point of the script.

    Loads the configuration, initializes a NewsScraper instance with the loaded configuration,
    and starts the scraping process.
    """
    config = load_config()
    scraper = NewsScraper(config)
    scraper.scrape()


if __name__ == "__main__":
    main()