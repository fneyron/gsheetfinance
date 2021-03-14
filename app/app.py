import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)


@app.route('/info/<share>/<option>/', methods=['GET'])
def yfinance(option, share):
    tick = yf.Ticker(share)
    df = getattr(tick, option)
    if not df is None:
        output = make_response(df.to_csv(header=False, index=False, decimal=','))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with %s function on %s ticker" % (option, share)

    return output


@app.route('/financials/<share>/', methods=['GET'])
def financials(share):
    yahoo_financials = YahooFinancials(share)
    tf = request.args.get('timeframe')
    type = request.args.get('type')

    fin_data = {
        'income': 'incomeStatementHistory',
        'balance': 'balanceSheetHistory',
        'cash': 'cashflowStatementHistory',
    }

    header = {'income':
        {
            'totalRevenue': 'Total Revenue',
            'costOfRevenue': 'Cost of Revenue',
            'grossProfit': 'Gross Profit',
        }}
    keep = [v for v in header[type]]
    print(keep)

    datas = yahoo_financials.get_financial_stmts(tf, type)
    datas = datas[fin_data[type]][share]
    datas = [dict(x[y], **{'date': y}) for x in datas for y in x]
    df = pd.DataFrame(datas)
    df = df.set_index('date')
    df = df[keep]
    df = df.rename(columns=header[type]).transpose()
    print(df)
    if not df is None:
        output = make_response(df.to_csv(index=True, index_label='Date', decimal=','))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else:
        output = "Error with %s ticker options : %s" % (share, request.args)

    return output


@app.route('/')
def index():
    return render_template('index.html')
