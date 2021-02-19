import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
from flask import Flask, request, jsonify, make_response
app = Flask(__name__)


@app.route('/yfinance/<option>/<share>/', methods=['GET'])
def yfinance(option, share):

    tick = yf.Ticker(share)
    df = getattr(tick, option)
    if not df is None:
        output = make_response(df.to_csv(header=False, index=False, decimal=','))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else: output = "Error with %s function on %s ticker" % (option, share)

    return output

@app.route('/yahoofinancials/<share>/', methods=['GET'])
def yahoofinancials(share):

    yahoo_financials = YahooFinancials(share)
    tf = request.args.get('timeframe')
    type = request.args.get('type')

    income_statement_data_qt = yahoo_financials.get_financial_stmts(tf, type)
    datas = income_statement_data_qt['incomeStatementHistory'][share]
    datas = [dict(x[y], **{'Date': y}) for x in datas for y in x]
    df = pd.DataFrame(datas)

    if not df is None:
        output = make_response(df.to_csv(index=False, decimal=','))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else: output = "Error with %s ticker options : %s" % (share, request.args)

    return output


@app.route('/')
def index():
    return "<h1>YFinance-App</h1>" \
           "<div>Do the same as rapid-api but for free :)</div>"
