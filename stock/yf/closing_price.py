#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pyrate_limiter import Duration, Limiter, RequestRate
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
import typer
import yfinance as yf


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("/tmp/yfinance.cache"),
)


def stock_report(symbols: str = "ADBE,MSFT") -> None:
    first, *_ = symbols.upper().split(",")
    tickers = yf.Tickers(symbols, session=session)
    tickers.history(period="1mo", progress=False)

    hist_df = tickers.history(period="1mo")
    hist_df = hist_df[["Close", "Volume"]]
    assert len(hist_df) == len(hist_df.Close)  # == len(hist_df.Close.ADBE)

    print(hist_df.Close[first])
    # pp(msft.history_metadata)
    # pp(msft.info)


if __name__ == "__main__":
    typer.run(stock_report)
