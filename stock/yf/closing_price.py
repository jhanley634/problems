#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import typer
import yfinance as yf


def stock_report(symbols: str = "ADBE,MSFT") -> None:
    first, *_ = symbols.upper().split(",")
    tickers = yf.Tickers(symbols)
    tickers.history(period="1mo", progress=False)

    hist_df = tickers.history(period="1mo")
    hist_df = hist_df[["Close", "Volume"]]
    assert len(hist_df) == len(hist_df.Close)  # == len(hist_df.Close.ADBE)

    print(hist_df.Close[first])
    # pp(msft.history_metadata)
    # pp(msft.info)


if __name__ == "__main__":
    typer.run(stock_report)
