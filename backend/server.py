from flask import Flask, Response
from flask_socketio import SocketIO, send, emit
from flask_sse import sse
from flask_cors import CORS
from datetime import datetime
import json
app = Flask(__name__)
CORS(app)
#app.config["REDIS_URL"] = "redis://127.0.0.1"
#app.register_blueprint(sse, url_prefix='/events')
socketio = SocketIO(app, cors_allowed_origins='*')
import random
import time
import threading
from stock_metadata import company_and_ticks

x = 0


def get_data():
    global x
    x += 1000
    return {"portfolio": x,
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            random.choice(list(company_and_ticks.values())): int(random.uniform(-1, 1) * 10),
            random.choice(list(company_and_ticks.values())): int(random.uniform(-1, 1) * 10),
            random.choice(list(company_and_ticks.values())): int(random.uniform(-1, 1) * 10)
            }

@app.route('/events')
def server_side_event():
    """ Function to publish server side event """
    while True:
        new_data = get_data()
        time.sleep(15)
        print(new_data)
        portfolio_value= {}
        transaction_values = []
        for key, value in new_data.items():
            if key == "portfolio":
                portfolio_value["y"] = value
            elif key == "time":
                portfolio_value["x"] = value
            else:
                transaction = dict()
                transaction["tick"] = key
                if value < 0:
                    transaction["operation"] = "SELL"
                else:
                    transaction["operation"] = "BUY"
                transaction["qty"] = abs(value)
                transaction_values.append(transaction)
        socketio.emit('portfolio', portfolio_value)
        socketio.emit('transaction', transaction_values)
        #sse.publish(portfolio_value, type='portFolioValues')
        #sse.publish(transaction_values, type='transactionValues')

@socketio.on('connect')
def continuous_thread():
    thread_start = threading.Thread(target=server_side_event)
    thread_start.start()


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)
