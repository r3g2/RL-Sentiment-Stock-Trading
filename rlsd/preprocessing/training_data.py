import pandas as pd
import numpy as np
import os
import sys

from rlsd.config import config

def load_data(csv_path):
    df = pd.read_csv(csv_path,index_col=0)
    return df

def filter_by_ticker(df,tickers=config.stock_tickers,cols=["ticker", "content", "release_date"]):
    return df[df['ticker'].isin(tickers)][cols]

def format_save(df,fname, dir='/Users/rickgentry/github/BigData/RL-Sentiment-Stock-Trading/data'):
    df.rename(columns={'release_date':'date','ticker':'tic'},inplace=True)
    df = df.sort_values(["date","tic"],ignore_index=True)
    df.index = df.date.factorize()[0]
    df.to_csv(os.path.join(dir,fname))
    return df
    



def main():
    data_dir = os.path.relpath('/Users/rickgentry/github/BigData/RL-Sentiment-Stock-Trading/data')
    df = load_data(os.path.join(data_dir,"us_equities_news_dataset.csv"))
    used_df = filter_by_ticker(df)
    saved_df = format_save(used_df,"stock_text_news_dataset.csv")
    print(saved_df.head())
    
if __name__ == "__main__":
    main()