#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pprint import pp

from yahoofinancials import YahooFinancials as YF


def query_yahoo_financials() -> None:
    tickers = ["ADBE", "MSFT"]
    fin = YF(tickers, concurrent=True, max_workers=1, country="US")
    # balance_sheet_data_qt = fin.get_financial_stmts("quarterly", "balance")
    # pp(balance_sheet_data_qt)

    # result = fin.get_stock_data()
    # result = fin.get_open_price()
    result = fin.get_prev_close_price()
    pp(result)
    assert len(result) == len(tickers)


if __name__ == "__main__":
    query_yahoo_financials()
