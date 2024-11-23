# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
import logging

from beartype import beartype
from boltons.dictutils import FrozenDict
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
import sqlalchemy as sa

from geo.htmx import get_conn
from geo.htmx.models import Author, Book


def populate_books_table(minimum: int = 8) -> None:
    """Ensures that there's always at least a few book titles to scroll through."""
    if Author.query.count() == 0:
        with get_conn() as conn:
            stmt = sa.insert(Author.__table__).values(name="Mark Twain")
            conn.execute(stmt)
            conn.commit()
    if Book.query.count() < minimum:
        process = CrawlerProcess()
        process.crawl(Gutenberg)
        process.start()
        print("Crawl complete!")


@beartype
class Gutenberg(Spider):  # type: ignore [misc]
    name = "gutenberg"
    allowed_domains = ("gutenberg.org",)
    mark_twain = "https://www.gutenberg.org/ebooks/author/53"
    start_urls = (mark_twain,)
    custom_settings = FrozenDict(
        {
            "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
            "LOG_LEVEL": logging.WARNING,
        }
    )

    def parse(self, response: HtmlResponse) -> Generator[None]:
        with get_conn() as conn:
            titles = response.css("span .title")[4:]
            for title in titles:
                stmt = sa.insert(Book.__table__).values(
                    author_id=1, title=title.css("::text").get()
                )
                conn.execute(stmt)

            conn.commit()
            yield None
