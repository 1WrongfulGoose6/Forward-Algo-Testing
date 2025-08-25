import pandas as pd
import time
import atexit
from datetime import datetime
from datetime import time as dtime
from data_fetcher import fetch_live_data
from storage import ensure_folder, save_dataframe, load_dataframe, update_dataframe


def state(num):
    
    match num:
        case 1:
            print("Grabbed API Data:", datetime.now().time())
        case 2:
            print("Appended to DF:", datetime.now().time())
        case 3:
            print("Program Terminated:", datetime.now().time())
        case 4:
            print("Program started:", datetime.now().time())
        case 5:
            print("Sleeping for 5min.")
        case 6:
            print("Positions Reset:", datetime.now().time())

def reset_positions():
    IN_SHORT = False
    IN_LONG = False
    long_sl = None
    short_sl = None
    long_tp = None
    short_tp = None
    state(6)

def trading_time():
    current_time = datetime.now().time()
    start = dtime(23, 30)   # 11:30 PM
    end   = dtime(2, 0)     # 6:00 AM
    
    if current_time >= start or current_time <= end:
        return True
    return False



# Start Program
state(4)
file = open("key.txt", 'r')
key = file.read()
file.close()

SYMBOL = "QQQ"
INTERVAL = "5min"
API_KEY = key

IN_SHORT = False
IN_LONG = False
long_sl = None
short_sl = None
long_tp = None
short_tp = None


df = pd.DataFrame()

# Start Loop
while trading_time():
    print("Loop entered at", datetime.now().time())
    row = fetch_live_data(SYMBOL, INTERVAL, API_KEY, outputsize=500)
    state(1)

    if row.empty:
        print("API returned empty dataframe")
    else:
        # If row exists transform into df and append
        temp_df = row.to_frame().T
        temp_df.index = [row.name]
        df = pd.concat([df, temp_df])
        state(2)

        print("Current Rows:", len(df))

        # extract values
        close = temp_df['close'].iloc[0]
        vwap  = temp_df['vwap'].iloc[0]
        rsi   = temp_df['rsi'].iloc[0]
        print(f"Extracted values are close:{close}, vwap:{vwap} and rsi:{rsi}")

        short_target = vwap * 0.997
        long_target = vwap * 1.007
        print(f"Take longs at {long_target} and shorts {short_target}")

        # long signal
        if (close < vwap * 0.997 and rsi < 35 and not IN_SHORT and not IN_LONG):
            IN_LONG = True
            long_tp = close + 1.0
            long_sl = close - 0.5

            print(f"buy entered at {close} with vwap:{vwap} and rsi:{rsi}", close, vwap, rsi)
        
        # short signal
        elif (close > vwap * 1.007 and rsi > 65 and not IN_SHORT and not IN_LONG):
            IN_SHORT = True
            short_tp = close - 1.0
            short_sl = close + 0.5
            print(f"short entered at {close} with vwap:{vwap} and rsi:{rsi}", close, vwap, rsi)

        if IN_LONG:
            # stop loss
            if(long_sl is not None and close < long_sl):
                print(f"Stop Loss of {long_sl} triggered", long_sl)
                reset_positions()

            # take profit
            if(long_tp is not None and close > long_tp):
                print(f"Take Profit of {long_tp} triggered", long_tp)
                reset_positions()
    
        if IN_SHORT:
            # stop loss
            if(short_sl is not None and close > short_sl):
                print(f"Stop Loss of {short_sl} triggered", short_sl)
                reset_positions()
            # take profit
            if(short_tp is not None and close < short_tp):
            
                print(f"Take Profit of {short_tp} triggered", short_tp)  
                reset_positions() 



    state(5)
    time.sleep(300)
if 'df' in locals():
    save_dataframe(df, SYMBOL)

