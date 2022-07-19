import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utilities import page_loader
from models import save_data


class EtsyProductsScrapper:
    def __init__(self):
        self.etsy_url = 'https://etsy.com'
        self.driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
        self.products = []
        self.keyword = ''

    @page_loader
    def get_url(self):
        self.driver.get(self.etsy_url)

    def search_keyword(self):
        search_input = self.driver.find_element(By.ID, "global-enhancements-search-query")
        search_input.send_keys(self.keyword)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)

    def get_products(self):
        products_list = self.driver.find_elements(By.CSS_SELECTOR, "[data-results-grid-container] li")
        for product in products_list:
            product_title = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('title')
            product_currency = product.find_element(By.CSS_SELECTOR, 'a .currency-symbol').text
            product_price = product.find_element(By.CSS_SELECTOR, 'a .currency-value').text
            self.products.append({
                "product_title": product_title,
                "product_price": f"{product_price} {product_currency}"
            })

    def save_products(self):
        save_data(products=self.products)

    def run(self, keyword):
        self.keyword = keyword
        self.get_url()
        self.search_keyword()
        self.get_products()
        self.save_products()
        self.driver.quit()


if __name__ == "__main__":
    etsy_instance = EtsyProductsScrapper()
    etsy_instance.run(keyword="jeans")
