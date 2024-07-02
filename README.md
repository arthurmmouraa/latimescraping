# Web Scraping with Selenium and Python

This project utilizes Python along with Selenium for web scraping news from the "Los Angeles Times" website. The goal is to extract information about posts related to a specific search phrase and save the data into an Excel file.

## Requirements

To run this project, you will need to have the following prerequisites installed:

- Python 3.x
- Google Chrome (or another browser supported by Selenium)
- WebDriver for your browser
- Python libraries specified in the requirements.txt file

You can install the necessary dependencies by running the following command:

> pip install -r requirements.txt

## Configuration

Before starting the scraping process, it's necessary to configure some variables in the config.yaml file located inside the config/ folder. The configurable variables include:

- SEARCH_PHRASE: Search phrase to find specific posts.
- CATEGORY: Category to filter the posts.
- MONTHS: Number of months of posts to consider (0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on)

By default, the configuration file comes pre-set with the following values:

> SEARCH_PHRASE: "Brazil"
> CATEGORY: "World & Nation"
> MONTHS: 1

Ensure these variables are configured according to your specific scraping requirements before proceeding.

## Running the Project

To start the scraping process, execute the main.py file:

> python "main.py"

The script will launch the browser, search for and extract relevant information from the website, and save the data into an Excel file named post_data.xlsx in the project's root folder.
