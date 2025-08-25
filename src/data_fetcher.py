from twelvedata import TDClient
import pandas as pd

# Initialize client
def init_td_client(api_key):
    return TDClient(apikey=api_key)

# Fetch OHLCV + VWAP + RSI in one call
def fetch_live_data(symbol, interval, api_key, outputsize=1):
    td = init_td_client(api_key)

    # Build request: time series + indicators
    ts = td.time_series(
        symbol=symbol,
        interval=interval,
        outputsize=outputsize
    ).with_vwap().with_rsi()

    # Return as Pandas DataFrame
    df = ts.as_pandas()
    df.index = pd.to_datetime(df.index).tz_localize('UTC')
     
    # Ensure datetime index is sorted
    df.sort_index(inplace=True)

    df = df.iloc[-1]
    return df

if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"
    df = fetch_live_data("QQQ", "5min", API_KEY, outputsize=1)
    print(df.tail())