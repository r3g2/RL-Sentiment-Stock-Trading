import sys
import os
import pandas as pd
import numpy as np
import datetime
from finrl.config import config
from finrl.marketdata.yahoodownloader import YahooDownloader
from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split
from finrl.env.env_stocktrading import StockTradingEnv

from finrl.model.models import DRLAgent
from finrl.trade.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline

sys.path.append("/Users/rickgentry/github/BigData/RL-Sentiment-Stock-Trading")
from config.config import stock_tickers
from env.env_stocks import StockEnv
from env.env_onlinestocktrading import OnlineStockTradingEnv
from preprocessing.training_data import load_data

def create_training_environment(data,env_kwargs = {
                                            "hmax": 100, 
                                            "initial_amount": 1000000, 
                                            "buy_cost_pct": 0.001, 
                                            "sell_cost_pct": 0.001, 
                                            "state_space": 331, 
                                            "stock_dim": 30, 
                                            "tech_indicator_list": ['sentiment'] + config.TECHNICAL_INDICATORS_LIST, 
                                            "action_space": 30, 
                                            "reward_scaling": 1e-4
                                            }):
    e_train_gym = StockTradingEnv(df = data,**env_kwargs)
    return e_train_gym

def train_model(e_train_gym,tb_log_name,model_type="a2c",load_model_path='',save_model_path='',train_timesteps=80000):
    training_env, _ = e_train_gym.get_sb_env()
    training_agent = DRLAgent(training_env)
    model = training_agent.get_model(model_type)
    if load_model_path:
        print("LOADING MODEL PARAMETERS")
        model = model.load(load_model_path)
    print("=======TRAINING MODEL========")
    trained_model = training_agent.train_model(model,tb_log_name=tb_log_name,total_timesteps=train_timesteps)
    trained_model.save(save_model_path)
    return trained_model


def main():
    # Load training data
    data_dir = '/Users/rickgentry/github/BigData/RL-Sentiment-Stock-Trading/data'
    train_df = load_data(os.path.join(data_dir,"historical_feature_data_2019-2020.csv"))
    train_data = train_df.sort_values(["date", "tic"], ignore_index=True)
    train_data.index = train_data.date.factorize()[0]
    stock_dimension = len(train_data.tic.unique())
    indicator_list = ['sentiment'] + config.TECHNICAL_INDICATORS_LIST
    state_space = 1 + 2*stock_dimension + len(indicator_list)*stock_dimension
    print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

    env_kwargs = {
                "hmax": 100, 
                "initial_amount": 1000000, 
                "buy_cost_pct": 0.001, 
                "sell_cost_pct": 0.001, 
                "state_space": state_space, 
                "stock_dim": stock_dimension, 
                "tech_indicator_list": ['sentiment'] + config.TECHNICAL_INDICATORS_LIST, 
                "action_space": stock_dimension, 
                "reward_scaling": 1e-4
                }

    # Create training environment
    e_train = create_training_environment(train_data,env_kwargs=env_kwargs)
    save_model_path = '/Users/rickgentry/github/BigData/RL-Sentiment-Stock-Trading/trained_models/a2c_2019-2020_80k'
    trained_model = train_model(e_train,"a2c_2019-2020_log",save_model_path=save_model_path,train_timesteps=80000)
    print("DONE")

if __name__ == "__main__":
    main()