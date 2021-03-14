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
    else: output = "Error with %s function on %s ticker" % (option, share)

    return output

@app.route('/financials/<share>/', methods=['GET'])
def financials(share):

    yahoo_financials = YahooFinancials(share)
    tf = request.args.get('timeframe')
    type = request.args.get('type')

    data = {
        'income': 'incomeStatementHistory',
        'balance': 'balanceSheetHistory',
        'cash': 'cashflowStatementHistory',
    }

    income_statement_data_qt = yahoo_financials.get_financial_stmts(tf, type)
    datas = income_statement_data_qt[data[type]][share]
    datas = [dict(x[y], **{'Date': y}) for x in datas for y in x]
    df = pd.DataFrame(datas)
    df = df.set_index('Date')
    df = df.transpose().reset_index()

    if not df is None:
        output = make_response(df.to_csv(index=False, decimal=','))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else: output = "Error with %s ticker options : %s" % (share, request.args)

    return output


@app.route('/')
def index():
    return render_template('index.html')
