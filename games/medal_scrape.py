#! /usr/bin/env scrapy runspider -o /tmp/games.jsonl
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator

from boltons.dictutils import FrozenDict
from bs4 import BeautifulSoup
from frozenlist import FrozenList
from scrapy.http import Response
import scrapy

url = "https://olympics.com/en/paris-2024/schedule/27-july?medalEvents=true"


class OlympicMedals2024(scrapy.Spider):  # type: ignore [misc]
    name = "OlympicMedals2024"
    allowed_domains = FrozenList(["olympics.com"])
    custom_settings = FrozenDict(
        {
            "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
            "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
        }
    )
    # start_urls = ["https://www.whatismybrowser.com/detect/what-is-my-user-agent/"]
    start_urls = FrozenList(
        ["https://olympics.com/en/paris-2024/schedule/27-july?medalEvents=true"]
    )

    def parse(self, response: Response) -> Generator[dict[str, str]]:
        assert 200 == response.status, response
        soup = BeautifulSoup(response.body, "html.parser")
        with open("/tmp/medal-events.html", "w") as fout:
            fout.write(soup.prettify())

        option = response.css('#country-selector-country option[value="BG"]')
        if option:
            value = option.css("::attr(value)").get().lower()
            bg_url = f"https://www.marksandspencer.com/{value}"
            self.logger.info("BG URL found: %s", bg_url)
            yield response.follow(bg_url, callback=self.parse_bg_page)
        else:
            self.logger.warning("BG option not found on the homepage.")


# from geo.gpx.so.word_publisher import get_document
# def report() -> None:
#     print(get_document(url))
# if __name__ == "__main__":
#     report()
