import yfinance as yf
import pandas as pd
from pytrends.request import TrendReq
from dateutil.relativedelta import relativedelta
import datetime
import os
import json
from flask import Flask, request, jsonify, make_response, render_template

#os.environ['HTTP_PROXY'] = "http://172.16.99.9:3129"
#os.environ['HTTPS_PROXY'] = "http://172.16.99.9:3129"

app = Flask(__name__)

@app.route('/pytrend', methods=['GET'])
def pytrend():
    pytrends = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1, requests_args={'verify': False},
                        timeout=(10, 25))
    kw_list = [request.args.get('string')]
    if request.args.get('tf') is not None:
        tf = request.args.get('tf')
    else:
        tf = "today 12-m"
    pytrends.build_payload(kw_list, cat=0, timeframe=tf, geo='', gprop='')
    df = pytrends.interest_over_time().reset_index()

    print(df)

    if not df is None:
        output = make_response(df.to_csv(index=False))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with pytrend function"

    return output

@app.route('/info/<symbol>/', methods=['GET'])
def yfinance(symbol):
    tick = yf.Ticker(symbol)
    print(tick.info)
    df = pd.DataFrame.from_dict(tick.info, orient='index')
    if not df is None:
        output = make_response(df.to_csv(header=False))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with %s function on %s ticker" % (type, symbol)
    return output

@app.route('/financials/<symbol>/', methods=['GET'])
def financials(symbol):
    type = request.args.get('type')
    if request.args.get('tf').lower() == "quarterly":
        tf = "quarterly_"
    else: tf = ""

    data = {
        'income': 'financials',
        'balance': 'balance_sheet',
        'cash': 'cashflow',
    }
    #diff = ['TotalRevenue', 'CostOfRevenue', 'GrossProfit']
    df: pd.DataFrame = getattr(yf.Ticker(symbol), tf+data[type])
    df = df[df.columns[::-1]]
    df.index = df.index.str.replace(' ', '')
    #df = df.transpose()
    #for d in df:
            #df[d + 'Perf'] = (df[d] - df[d].shift(-1)) / df[d].shift(-1)
    #if type == 'income':
    #    df['OperatingExpenses'] = df['TotalOperatingExpenses'] - df['CostOfRevenue']
    #df = df.transpose()



    ## In case there is less than 4 columns results we add the missing one
    last_date = df.columns[len(df.columns) - 1]
    if len(df.columns) < 5:
        id_col = 5-len(df.columns)
        for i in range(0, id_col-1):
            print(i)
            date = last_date.replace(year=last_date.year - (5-(i+2)))
            print(date)
            df.insert(i, date, None)
    print(df)

    if not df is None:
        output = make_response(df.to_csv())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with %s function on %s ticker" % (type, symbol)

    return output


@app.route('/')
def index():
    return render_template('index.html')
