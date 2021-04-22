import yfinance as yf
import pandas as pd
import os
import json
from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)


@app.route('/info/<symbol>/', methods=['GET'])
def yfinance(symbol):
    tick = yf.Ticker(symbol)
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
    df.index = df.index.str.replace(' ', '')

    #df = df.transpose()
    #for d in df:
            #df[d + 'Perf'] = (df[d] - df[d].shift(-1)) / df[d].shift(-1)
    #if type == 'income':
    #    df['OperatingExpenses'] = df['TotalOperatingExpenses'] - df['CostOfRevenue']
    #df = df.transpose()


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
