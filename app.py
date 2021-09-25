import json
from os import urandom
import binance
from binance import Client
from flask import Flask, request,render_template,url_for
from flask.json import jsonify
from werkzeug.utils import redirect
from werkzeug.wrappers import response

import config

app = Flask(__name__)
# client = Client(config.API_KEY, config.API_SECRET, tld='us')
# client = Client(config.API_KEY, config.API_SECRET)
client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol,order_type=binance.enums.ORDER_TYPE_MARKET):
    try:
        print(f"sending order {side} - {symbol} - {quantity} api - {config.API_KEY}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        error=(f"sending order {side} - {symbol} - {quantity} an exception occured - {e}")
        print(error)
        return error

    return order

@app.route("/")
@app.route("/home")
def home():
    return render_template('welcome.html',response=None)


#just need to add user input
@app.route('/order', methods=['GET','POST'])
def order_now():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        response=order(data['side'].upper(),data['quantity'],data['ticker'].upper(),data['order_type'].upper())
        # print({
        #     "code": "success" ,
        #     "order-executed": response,
        #     "Message": data
        # })
        user_response= {
            "code": "success" ,
            "order": response,
            "message": data
        }
        return jsonify(user_response)
    
    return render_template("order.html")

