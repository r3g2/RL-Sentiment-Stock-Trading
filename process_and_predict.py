import argparse
import datetime
import json
import time
import numpy as np
from config import config
from finrl.marketdata.yahoodownloader import YahooDownloader
from finrl.preprocessing.preprocessors import FeatureEngineer
from sentiment_analysis.Sentiment_model import init_from_file, save_to_file, get_sentiment_score
from model.online_stock_prediction import OnlineStockPrediction, setup_model
from preprocessing.data_processor import DataProcessor, generate_sentiment_scores, get_initial_data
from threading import Thread, Event, RLock
from kafka import KafkaConsumer
from kafka import KafkaProducer

current_df = None
cur_stock_quants = { tick : 0 for tick in config.stock_tickers }

class Predicter(Thread):
    def __init__(self, event, model, producer, topic):
        Thread.__init__(self)
        self.stopped = event
        self.model = model
        self.producer = producer
        self.topic = topic

    def run(self):
        while not self.stopped.wait(5):
            self.predict()
        print("Stopping")

    def predict(self):
        global current_df
        global cur_stock_quants
        df = None
        lock = threading.RLock()
        with lock:
            df = current_df
        self.model.add_data(df)
        action,states, next_obs, rewards = self.model.predict()

        # portfolio value, timestamp, map of ticker to buy sell quantities
        stock_quant_map = { tick : value for tick, value in zip(config.stock_tickers, next_obs[31:61]) }
        reserve = next_obs[0]
        stock_prices = np.array(next_obs[1:31])
        stock_quants = np.array(next_obs[31:61])
        portfolio = reserve + sum(stock_prices*stock_quants)

        timestamp = time.time()
        stock_deltas = { tick : int(stock_quant_map[tick] - cur_stock_quants[tick]) for tick in config.stock_tickers }
        cur_stock_quants = stock_quant_map
        message_obj = { "portfolio": portfolio, "timestamp":timestamp, "stock_deltas": stock_deltas, "ticker": ticker}
        self.output(message_obj)


    def output(self, message):
        if self.producer is None:
            print(message)
        else:
            if self.topic is None:
                raise ValueError("topic not supplied")
            key = "{0}_{1}".format(message["ticker"],message["timestamp"])
            try:
                key_bytes = bytes(key, encoding='utf-8')
                value = json.dumps(comment)
                value_bytes = bytes(value, encoding='utf-8')
                self.producer.send(self.topic, key=key_bytes, value=value_bytes)
            except Exception as e:
                print("Error {0} occurred while publishing message with key {1}".format(e, key))



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Read text data from kafka topic and compute score, write to Kafka topic again")
    parser.add_argument('topic', metavar='<topic_name>', help='Kafka topic name to read from')
    parser.add_argument('write_topic', metavar='<write_topic_name>', help='Kafka topic name to write from')
    parser.add_argument('hosts', metavar='<hosts>', nargs='+', help='space separated list of Hostname:port of bootstrap servers')
    parser.add_argument('-s', '--start-date', metavar='<start_date>', help='training data start date')
    parser.add_argument('-e', '--end-date', metavar='<end_date>', help='training data end date')
    parser.add_argument('-t', '--trade-date', metavar='<trade_date>', help='trading start date')
    args = parser.parse_args()
    consumer = KafkaConsumer(args.topic, auto_offset_reset='latest', \
            bootstrap_servers=args.hosts, api_version=(0, 10), consumer_timeout_ms=1000)
    
    producer = KafkaProducer(bootstrap_servers=args.hosts, api_version=(0, 10))
    # data initialization
    tday = datetime.date.today()
    yday = tday - datetime.timedelta(days=1)
    fmt = "%Y-%m-%d"
    numerical_df = YahooDownloader(args.start_date, args.end_date, config.stock_tickers).fetch_data()
    sentiment_df = generate_sentiment_scores(args.start_date, args.end_date)
    initial_data = get_initial_data(numerical_df, sentiment_df)
    data_processor = DataProcessor(FeatureEngineer(),initial_data)
    
    new_numerical = YahooDownloader(datetime.datetime.strftime(yday,fmt),datetime.datetime.strftime(tday,fmt), config.stock_tickers).fetch_data()
    # set up model to train on initial data
    model = setup_model(initial_data, load_path)

    while consumer is None:
        sleep(20)

    stop_flag = Event()
    th = MyThread(stop_flag,predict)
    th.start()

    init_from_file()
    try:
        for msg in consumer:
            msg_json = json.loads(msg.decode('utf-8'))
            scores = get_sentiment_score(msg_json["text"], msg_json["ticker"])
            print("Computed score {0} for stock ticker {1}".format(score, msg_json["ticker"]))
            # construct new sentiment df
            new_sentiment = 
            new_df=data_processor.process_data(new_numerical,new_sentiment)

    except KeyboardInterrupt:
        save_to_file()
        stop_flag.set()

