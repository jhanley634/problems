#! /usr/bin/env scrapy runspider -o /tmp/m_and_s.jsonl
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/292776/scrapy-spider-for-fetching-product-data-from-multiple-pages
from collections.abc import Generator
import json

from beartype import beartype
from boltons.dictutils import FrozenDict
from scrapy.http import HtmlResponse
import scrapy


@beartype
class MarksAndSpencerSpider(scrapy.Spider):  # type: ignore [misc]
    name = "marksandspencer"
    allowed_domains = ("marksandspencer.com",)
    start_urls = ("https://www.marksandspencer.com",)
    custom_settings = FrozenDict({"REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"})

    def parse(self, response: HtmlResponse) -> Generator[dict[str, str]]:
        option = response.css('#country-selector-country option[value="BG"]')
        if option:
            value = option.css("::attr(value)").get().lower()
            bg_url = f"https://www.marksandspencer.com/{value}"
            self.logger.info("BG URL found: %s", bg_url)
            yield response.follow(bg_url, callback=self.parse_bg_page)
        else:
            self.logger.warning("BG option not found on the homepage.")

    def parse_bg_page(
        self, response: HtmlResponse
    ) -> Generator[dict[str, str]]:
        men_link = response.css(
            ".nav-item.dropdown.order-lg-3 .subcategory a::attr(href)"
        ).get()
        if men_link:
            self.logger.info("Men's link found: %s", men_link)
            yield response.follow(men_link, callback=self.parse_mens_page)
        else:
            self.logger.warning("Men's section link not found on the BG page.")

    def parse_mens_page(
        self, response: HtmlResponse
    ) -> Generator[dict[str, str]]:
        casual_shirts_link = response.xpath(
            '//a[contains(text(), "Casual shirts")]/@href'
        ).get()
        if casual_shirts_link:
            self.logger.info("Casual shirts link found: %s", casual_shirts_link)
            yield response.follow(casual_shirts_link, callback=self.parse_casual_shirts)
        else:
            self.logger.warning("Casual shirts link not found on the Men's page.")

    def parse_casual_shirts(
        self, response: HtmlResponse
    ) -> Generator[dict[str, str]]:
        product_link = response.css(
            'div.pdp-link a:contains("Easy Iron Geometric Print Shirt")::attr(href)'
        ).get()
        if product_link:
            self.logger.info("Product link found: %s", product_link)
            yield response.follow(product_link, callback=self.parse_product_page)
        else:
            self.logger.warning("Product link not found in the Casual Shirts section.")

    def parse_product_page(
        self, response: HtmlResponse
    ) -> Generator[dict[str, float | str | list[str]]]:
        product_name = response.css(".product-name::text").get()
        price = response.css(".value::text").get()
        selected_colour = response.css("button.qa-addtocart-button")
        size = response.css("#plp-select").get()
        reviews_script = response.xpath(
            '(//script[@type="application/ld+json"])[2]/text()'
        ).get()

        if reviews_script:
            json_data = json.loads(reviews_script)
            review_count = json_data.get("AggregateRating", {}).get("reviewCount", 0)
            avg_rating = json_data.get("AggregateRating", {}).get("ratingValue", 0.0)
        else:
            review_count = 0
            avg_rating = 0.0

        color = ""
        for button in selected_colour:
            color = button.attrib.get("data-defaultcolor", "")

        sizes = []
        if size:
            select_element = scrapy.Selector(text=size, type="html")
            option_tags = select_element.css("option")
            for option in option_tags:
                option_text = option.xpath("normalize-space(text())").get()
                if option_text != "Select Size":
                    sizes.append(str(option_text))

        product_data = {
            "name": product_name or "",
            "price": price or "",
            "colour": color,
            "size": sizes,
            "reviews_count": int(review_count),
            "reviews_score": float(avg_rating),
        }

        yield product_data
