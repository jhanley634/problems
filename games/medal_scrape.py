#! /usr/bin/env scrapy runspider -o /tmp/games.jsonl
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
from pprint import pp

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
import scrapy

url = "https://olympics.com/en/paris-2024/schedule/27-july?medalEvents=true"


class OlympicMedals2024(scrapy.Spider):  # type: ignore [misc]
    name = "OlympicMedals2024"
    allowed_domains = ["olympics.com"]
    custom_settings = {"REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"}
    # start_urls = ["https://olympics.com/en/paris-2024/schedule/27-july"]
    start_urls = ["https://olympics.com"]

    def parse(self, response: HtmlResponse) -> Generator[dict[str, str], None, None]:
        print(response, type(response))
        soup = BeautifulSoup(response.body, "html.parser")
        print(soup.prettify())
        pp(type(response))

        option = response.css('#country-selector-country option[value="BG"]')
        if option:
            value = option.css("::attr(value)").get().lower()
            bg_url = f"https://www.marksandspencer.com/{value}"
            self.logger.info(f"BG URL found: {bg_url}")
            yield response.follow(bg_url, callback=self.parse_bg_page)
        else:
            self.logger.warning("BG option not found on the homepage.")


# from geo.gpx.so.word_publisher import get_document
# def report() -> None:
#     print(get_document(url))
# if __name__ == "__main__":
#     report()
