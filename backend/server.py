from flask import Flask
from flask_sse import sse
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://127.0.0.1"
app.register_blueprint(sse, url_prefix='/events')
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

def server_side_event():
    """ Function to publish server side event """
    with app.app_context():
        new_data = get_data()
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
        sse.publish(portfolio_value, type='portFolioValues')
        sse.publish(transaction_values, type='transactionValues')
        print("Event Scheduled at ",datetime.now())

def continuous_thread():
    while True:
        server_side_event()
        time.sleep(3)


if __name__ == '__main__':
    test_thread = threading.Thread(target=continuous_thread())
    try:
        test_thread.start()
        app.run(debug=True,host='0.0.0.0',port=5000, threaded=True)
    finally:
        test_thread.join()