import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

def get_historical_stock_data(ticker: str, start_date, end_date):
    try:
        raw_data = YahooFinancials(ticker)
        historical_data = raw_data.get_historical_price_data(start_date, end_date, "daily")
        prices = historical_data.get(ticker, {}).get("prices", [])  # Necessary block of stocks data
        
        df = pd.DataFrame(prices)
        df['date'] = pd.to_datetime(df['formatted_date'] + ' 14:30:00')  # investigate which time of the day is the best
        df = df[['date', 'open', 'high', 'low', 'adjclose', 'volume']]
        df = df.fillna(method="ffill", axis=0)
        df = df.fillna(method="bfill", axis=0)
        df['volume'].replace(to_replace=0, method='ffill', inplace=True) # Replace 0 to avoid dividing by 0 later on
        df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
        #df.set_index('DateTime', inplace=True)
        return df
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame if no data is available


def fetch_tickers_data(tickers: list, start_date, end_date) -> pd.DataFrame:
    data_frames = []

    for ticker in tickers:
        ticker_data = get_historical_stock_data(ticker, start_date, end_date)
        if len(tickers) > 1 and not ticker_data.empty:
            ticker_data['Ticker'] = ticker  # Add a 'ticker' column to identify each ticker
        data_frames.append(ticker_data)

    if data_frames:
        concatenated_data = pd.concat(data_frames)
        return concatenated_data
    return pd.DataFrame()


def stock_plot(stock_str, df):
    
    sns.set(style="whitegrid")
    
    fig = plt.figure(figsize=(15,10))
    st = fig.suptitle(stock_str, fontsize=20)
    st.set_y(0.92)

    ax1 = fig.add_subplot(211)
    ax1.plot(df['Close'], label='Close Price')
    ax1.set_xticks(range(0, df.shape[0], 1464))
    #ax1.set_xticklabels(df['DateTime'].dt.strftime('%Y-%m-%d').loc[::1464])
    ax1.set_ylabel('Close Price', fontsize=18)
    ax1.legend(loc="upper left", fontsize=12)

    ax2 = fig.add_subplot(212)
    ax2.plot(df['Volume'], label='Volume')
    ax2.set_xticks(range(0, df.shape[0], 1464))
    #ax2.set_xticklabels(df['DateTime'].dt.strftime('%Y-%m-%d').loc[::1464])
    ax2.set_ylabel('Volume', fontsize=18)
    ax2.legend(loc="upper left", fontsize=12)
    
    plt.legend()