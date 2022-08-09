import time
import pytest
import logging

from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)


class TestCaseJiraAddDoc:
    search_btn = (By.CSS_SELECTOR, 'input[type="search"]')
    product_name_label = (By.CSS_SELECTOR, 'h4[class="product-name"]')
    no_product_label = (By.CSS_SELECTOR, '[class="no-results"] h2')

    @pytest.fixture
    def initialise(self, driver):
        self.driver = driver
        self.driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")

    @pytest.mark.parametrize("ticket_id", ["TP-1"])
    @pytest.mark.xfail
    def test_search_with_valid_value_TP_1(self, ticket_id, initialise):
        self.driver.find_element(*self.search_btn).send_keys("cau")
        product_name_text = self.driver.find_element(*self.product_name_label).text
        assert product_name_text == "Cauliflower - 1 Kg", "Product name is not matched"

    @pytest.mark.parametrize("ticket_id", ["TP-2"])
    def test_search_with_invalid_value_TP_2(self, ticket_id, initialise):
        self.driver.find_element(*self.search_btn).send_keys("aksdjfasfjsfs")
        product_name_text = self.driver.find_element(*self.no_product_label).text
        if product_name_text is "Sorry, no products matched your search!":
            assert False, "No products found for search value"

    @pytest.mark.parametrize("ticket_id", ["TP-3"])
    def test_search_with_valid_value_TP_3(self, ticket_id, initialise):
        self.driver.find_element(*self.search_btn).send_keys("bri")
        product_name_text = self.driver.find_element(*self.product_name_label).text
        assert product_name_text == "Brinjal - 1 Kg", "Product name is not matched"
