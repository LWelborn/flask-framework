from flask import Flask, render_template, request
from fetch_stock_data import fetch_stock_data

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/stock',methods = ['POST','GET'])
def stock():
  error = None
  if request.method == 'GET':
    ticker = request.args.get('ticker', '')
    price_options = request.args.getlist('price_options')
    if not ticker:
      error = 'Please select a stock symbol'
      return render_template('error.html', error=error)
    elif not price_options:
      error = 'Please select a price option'
      return render_template('error.html', error=error)  
    else:
      bk_script, bk_div, ticker = fetch_stock_data(ticker,price_options)
      return render_template('stock.html', bk_script=bk_script, bk_div=bk_div, ticker=ticker)

if __name__ == '__main__':
  app.run(port=33507)
