from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()

class Stock(db.Model):
    ticker = db.Column(db.String(6), primary_key=True)
    lastPrice = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.ticker} - {self.lastPrice}"

@app.route('/')
def index():
    return 'Hello'

@app.route('/tickers')
def get_tickers():
    tickers = Stock.query.all()
    output  = []
    for i in tickers:
        data = {'ticker': i.ticker,'last price': i.lastPrice}
        output.append(data)
    dctTickers = {"stocks": output}
    return dctTickers

@app.route('/tickers/<ticker>')
def get_tickers_by_id(ticker):
    stock = Stock.query.get_or_404(ticker)
    return {"Ticker": stock.ticker, "Last Price": stock.lastPrice}

@app.route('/tickers', methods=['POST'])
def add_stock():
    stock = Stock(ticker=request.json['ticker'], lastPrice=request.json['lastPrice'])
    db.session.add(stock)
    db.session.commit()
    return {"ticker":stock.ticker, "status":200}

@app.route('/tickers/<ticker>',methods=['DELETE'])
def delete_drink(ticker):
    stock = Stock.query.get(ticker)
    if stock is None:
        abort(404)
    db.session.delete(stock)
    db.session.commit()
    return {"status":200}

''' Ran in terminal (if using app.app_context().push(), we don't need the with app.app_context())
with app.app_context():
    db.create_all() #creates instance of db
    s1 = Stock(ticker="AAPL") #create object
    db.session.add(s1) #insert to db
    db.session.commit() #commit transaction
    Stock.query.all() #select *
'''






