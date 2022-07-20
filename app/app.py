import pandas as pd
import yfinance as yf
from flask import Flask, request, make_response, jsonify
from forex_python.converter import CurrencyRates
from datetime import datetime
from pytrends.request import TrendReq

app = Flask(__name__)

def df_to_csv(df):
    if not df is None:
        output = make_response(df.to_csv(index=False))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with pytrend function"

    return output

@app.route('/fx/<symbol>/historical', methods=['GET'])
def fx_historical(symbol):
    c = CurrencyRates()
    date = datetime.strptime(request.args.get("date"),"%d-%m-%Y")
    exchange_rate = c.get_rate(symbol[:3], symbol[3:], date)

    return make_response(jsonify(exchange_rate))


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

    if not df is None:
        output = make_response(df.to_csv(index=False))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with pytrend function"

    return output

@app.route('/stock/<symbol>/', methods=['GET'])
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


# @app.route('/')
# def index():
#     return render_template('index.html')
