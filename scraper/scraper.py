import datetime
import os

from loguru import logger
from openpyxl import Workbook
from RPA.Browser.Selenium import By, Selenium, WebDriverWait
from RPA.Browser.Selenium import expected_conditions as EC

from .downloader import download_image
from .utils import (calculate_date_limit, contains_money_amount,
                    convert_abbreviated_date, count_search_phrase)


class NewsScraper:
    def __init__(self, config):
        self.config = config
        self.browser = Selenium(auto_close=False)
        self.image_dir = "images"
        os.makedirs(self.image_dir, exist_ok=True)
        logger.info("NewsScraper initialized with config: {}", config)

    def save_data_to_excel(self, data):
        wb = Workbook()
        ws = wb.active
        ws.title = "Post Data"
        ws.append(
            [
                "Date",
                "Title",
                "Description",
                "Picture Filename",
                "Title Search Count",
                "Description Search Count",
                "Title Contains Money",
                "Description Contains Money",
            ]
        )

        for row in data:
            ws.append(row)

        wb.save("post_data.xlsx")
        logger.info("Data saved in post_data.xlsx file")

    def scrape(self):
        search_phrase = self.config["search_phrase"]
        category = self.config["category"]
        months = self.config["months"]
        date_limit = calculate_date_limit(months)

        logger.info(
            "Starting scrape with search_phrase:: {}, category: {}, months: {}",
            search_phrase,
            category,
            months,
        )

        self.browser.open_available_browser("https://www.latimes.com")
        try:
            self.browser.maximize_browser_window()
            logger.info("Window maximized")
        except Exception as e:
            logger.error("Error maximizing the window: {}", e)

        try:
            search_button = WebDriverWait(self.browser.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-element='search-button']")
                )
            )
            search_button.click()
            logger.info("Search button clicked")
        except Exception as e:
            logger.error("Error clicking the search button: {}", e)
            self.browser.close_browser()
            return

        try:
            search_field = WebDriverWait(self.browser.driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "q"))
            )
            logger.info("Search field found")
        except Exception as e:
            logger.error("Error finding the search field: {}", e)
            self.browser.close_browser()
            return

        search_field.send_keys(search_phrase)
        search_field.send_keys("\ue007")  # Pressing ENTER
        logger.info("Search phrase: '{}' sent", search_phrase)

        try:
            see_all_button = WebDriverWait(self.browser.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.button.see-all-button")
                )
            )
            see_all_button.click()
            logger.info("See All' button clicked")
        except Exception as e:
            logger.error("Error clicking the 'See All' button': {}", e)
            self.browser.close_browser()
            return

        try:
            filters_section = WebDriverWait(self.browser.driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "body > div.page-content > ps-search-results-module > form > div.search-results-module-ajax > ps-search-filters > div > aside > div > div.search-results-module-filters-content.SearchResultsModule-filters-content > div:nth-child(1) > ps-toggler",
                    )
                )
            )
            logger.info("Filters section loaded")
        except Exception as e:
            logger.error("Error loading the filters section: {}", e)
            self.browser.close_browser()
            return

        try:
            filter_option = WebDriverWait(self.browser.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{category}']"))
            )
            filter_option.click()
            logger.info("Filter '{}' selected", category)
        except Exception as e:
            logger.error("Error selecting the filter '{}': {}", category, e)
            self.browser.close_browser()
            return

        try:
            newest_option = WebDriverWait(self.browser.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "select.select-input option[value='1']")
                )
            )
            self.browser.select_from_list_by_value("css:.select-input", "1")
            logger.info("'Newest' option selected")
        except Exception as e:
            logger.error("Error selecting the 'Newest' option: {}", e)

        all_data = []
        postagem_anterior_ao_limite = False

        while True:
            date_elements = self.browser.find_elements(
                'xpath://p[@class="promo-timestamp"]'
            )
            title_elements = self.browser.find_elements("xpath://h3/a")
            description_elements = self.browser.find_elements(
                'xpath://p[@class="promo-description"]'
            )
            image_elements = self.browser.find_elements('xpath://img[@class="image"]')

            for date_element, title_element, description_element, image_element in zip(
                date_elements, title_elements, description_elements, image_elements
            ):
                date_text = convert_abbreviated_date(date_element.text.strip())
                title_text = title_element.text.strip()
                description_text = description_element.text.strip()
                image_src = image_element.get_attribute("src")

                image_filename = download_image(image_src, self.image_dir)

                title_search_count = count_search_phrase(title_text, search_phrase)
                description_search_count = count_search_phrase(
                    description_text, search_phrase
                )

                title_contains_money = contains_money_amount(title_text)
                description_contains_money = contains_money_amount(description_text)

                post_date = datetime.datetime.strptime(date_text, "%B %d, %Y").date()
                if post_date < date_limit:
                    postagem_anterior_ao_limite = True
                    logger.info(
                        "Previous post found before the date limit: {}", post_date
                    )
                    break

                all_data.append(
                    (
                        post_date,
                        title_text,
                        description_text,
                        image_filename,
                        title_search_count,
                        description_search_count,
                        title_contains_money,
                        description_contains_money,
                    )
                )

            self.save_data_to_excel(all_data)

            if postagem_anterior_ao_limite:
                break

            try:
                next_page_button_container = WebDriverWait(
                    self.browser.driver, 20
                ).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "div.search-results-module-next-page")
                    )
                )
                next_page_button = next_page_button_container.find_element(
                    By.TAG_NAME, "a"
                )
                self.browser.click_element(next_page_button)
                logger.info("Navigating to the next page")
            except Exception as e:
                logger.info(
                    "All pages processed or error while navigating to the next page: {}",
                    e,
                )
                break

        self.browser.close_browser()
        logger.info("Navegador fechado, raspagem concluída")
