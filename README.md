# Getting Started

Tool to get all python datas from package yfinance, yahoofinancials, etc. to google sheet.

I deployed it on Heroku and runned with python 3.8. It's currently in active devlopment.

> python run.py

## Google sheet integration
You can use https://gsheet-tracker.herokuapp.com for testing purpose only. 
Then you will need to install it on your own heroku. 

Each function return a CSV, try it with:
> https://gsheet-tracker.herokuapp.com/financials/AAPL/?timeframe=annual&type=income

### Financial datas:
> =IMPORTDATA("https://gsheet-tracker.herokuapp.com/financials/AAPL/?timeframe=annual&type=income")

| Date             | 31/12/2020         | 31/12/2019         | 31/12/2018         | 31/12/2017         |
|------------------|--------------------|--------------------|--------------------|--------------------|
| **Total Revenue**    | 49 912 000 000 €   | 70 478 000 000 €   | 63 707 000 000 €   | 59 022 000 000 €   |
| **Cost of Revenue**  | (43 324 000 000) € | (59 973 000 000) € | (54 753 000 000) € | (52 149 000 000) € |
| **Gross Profit**    | 6 588 000 000 €    | 10 505 000 000 €   | 8 954 000 000 €    | 6 873 000 000 €    |
| **Operating Income** | 1 590 000 000 €    | 1 022 000 000 €    | 3 302 000 000 €    | 1 627 000 000 €    |
### Holders:
> =importdata("https://gsheet-tracker.herokuapp.com/info/AAPL/major_holders/")
> =importdata("https://gsheet-tracker.herokuapp.com/info/AAPL/institutional_holders/")
> 
|||
|--------|---------------------------------------|
| 25.90% | % of Shares Held by All Insider       |
| 27.21% | % of Shares Held by Institutions      |
| 36.73% | % of Float Held by Institutions       |
| 583    | Number of Institutions Holding Shares |

| HOLDER                                                          | %     |
|-----------------------------------------------------------------|-------|
| Vanguard International Stock Index-Total Intl Stock Indx        | 1,37% |
| College Retirement Equities Fund-Stock Account                  | 0,87% |
| Vanguard Tax Managed Fund-Vanguard Developed Markets Index Fund | 0,57% |
| iShares Core MSCI EAFE ETF                                      | 0,43% |
| DFA International Value Series                                  | 0,38% |
| Bridge Builder Tr-Bridge Builder International Equity Fd        | 0,38% |