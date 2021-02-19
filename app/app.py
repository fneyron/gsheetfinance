import yfinance as yf
import pandas as pd
from flask import Flask, request, jsonify, make_response
app = Flask(__name__)


@app.route('/yfinance/<option>/<share>/', methods=['GET'])
def holders(option, share):

    tick = yf.Ticker(share)
    df = getattr(tick, option)
    if not df is None:
        output = make_response(df.to_csv(header=False, index=False))
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
    else: output = "Error with %s function on %s ticker" % (option, share)

    return output

@app.route('/')
def index():
    return "<h1>YFinance-App</h1>" \
           "<div>Do the same as rapid-api but for free :)</div>"
