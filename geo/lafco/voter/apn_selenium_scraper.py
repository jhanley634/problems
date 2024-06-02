#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Downloads 4-digit APN prefixes from San Mateo County's assessor website.
This gives us an APN --> address mapping.
"""
from time import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait
import selenium

PROPERTY_MAPS_PORTAL = "https://gis.smcgov.org/Html5Viewer/?viewer=raster"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"


class ApnScraper:
    def __init__(self) -> None:
        assert "4.21.0" == selenium.__version__, selenium.__version__
        self.driver = webdriver.Firefox()

    def step1_find_by_apn(self) -> None:
        """Click on "Find Parcels by APN"."""

        # Step # | name | target | value | comment
        # 1 | open | /Html5Viewer/?viewer=raster |  |
        self.driver.get("https://gis.smcgov.org/Html5Viewer/?viewer=raster")

        # 2 | setWindowSize | 1100x850 |  |
        self.driver.set_window_size(1100, 850)

        # 3 | waitForElementVisible | css=form:nth-child(2) .button | 14000 |
        accept_terms_ok = "form:nth-child(2) .button"
        WebDriverWait(self.driver, 14).until(
            visibility_of_element_located((By.CSS_SELECTOR, accept_terms_ok))
        )
        # 4 | click | css=form:nth-child(2) .button |  |
        self.driver.find_element(By.CSS_SELECTOR, accept_terms_ok).click()

        # 5.1 await visible
        find_parcels_by_apn = (
            ".toolbar-group:nth-child(1) .nested-group:nth-child(2)"
            " li:nth-child(1) .bound-visible-inline"
        )
        WebDriverWait(self.driver, 14).until(
            visibility_of_element_located((By.CSS_SELECTOR, find_parcels_by_apn))
        )
        # 5.2 | click | css=.toolbar-group:nth-child(1) .nested-group:nth-child(2) li:nth-child(1) .bound-visible-inline
        self.driver.find_element(By.CSS_SELECTOR, find_parcels_by_apn).click()

        # 6.1 await visible
        apn_input = "//form/div/div/div/div/div/div/input"
        WebDriverWait(self.driver, 6).until(
            visibility_of_element_located((By.XPATH, apn_input))
        )
        # 6.2 | type | id=formitem-D9c3JdxO | 0635 |
        self.driver.find_element(By.XPATH, apn_input).send_keys("0635")

        # 7 | click | css=form:nth-child(2) .button:nth-child(1) |  |
        self.driver.find_element(
            By.CSS_SELECTOR, "form:nth-child(2) .button:nth-child(1)"
        ).click()

        # 13.1 await visible
        request_csv = ".view:nth-child(5) .panel-header-button:nth-child(4)"
        WebDriverWait(self.driver, 14).until(
            visibility_of_element_located((By.CSS_SELECTOR, request_csv))
        )
        # 13.2 | click | css=.view:nth-child(5) .panel-header-button:nth-child(4) |  |
        self.driver.find_element(By.CSS_SELECTOR, request_csv).click()

        # 14 | mouseOut | css=.view:nth-child(5) .panel-header-button:nth-child(4) |  |
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # 15.1 await present
        # The CSV menu offers several data options, including "Export to CSV"
        csv_menu = ".bound-visible > div > .list-menu > .list-menu-item:nth-child(4) .list-menu-name"
        print(15.1, "will timeout here", csv_menu)
        t0 = time()
        WebDriverWait(self.driver, 44).until(
            presence_of_element_located((By.CSS_SELECTOR, csv_menu))
        )
        print("elapsed", round(time() - t0), 1)

        # 15.2 | mouseOver | css=.bound-visible > div > .list-menu > .list-menu-item:nth-child(4) .list-menu-name |  |
        element = self.driver.find_element(By.CSS_SELECTOR, csv_menu)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # 16.2 | click | css=.bound-visible > div > .list-menu > .list-menu-item:nth-child(4) .list-menu-name |  |
        self.driver.find_element(By.CSS_SELECTOR, csv_menu).click()

        if False:
            # 17 | mouseOut | css=.view:nth-child(5) .panel-header .list-menu-item:nth-child(4) .list-menu-name |  |
            element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions = ActionChains(self.driver)
            actions.move_to_element(element, 0, 0).perform()

        # 18.1 await visible
        confirm_csv_download_ok = ".confirm .button:nth-child(1)"
        WebDriverWait(self.driver, 9).until(
            visibility_of_element_located((By.CSS_SELECTOR, confirm_csv_download_ok))
        )
        # 18.2 | click | css=.confirm .button:nth-child(1) |  |
        self.driver.find_element(By.CSS_SELECTOR, confirm_csv_download_ok).click()

        # 19 | close |  |  |
        self.driver.close()

        self.driver.quit()


if __name__ == "__main__":
    scrp = ApnScraper()
    scrp.step1_find_by_apn()
