from config.config import load_config
from config.logging_config import configure_logger
from scraper.scraper import NewsScraper

# Configure logger
logger = configure_logger()

if __name__ == "__main__":
    config = load_config()
    scraper = NewsScraper(config)
    scraper.scrape()
