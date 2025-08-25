# storage.py

import os
import pandas as pd
import glob

DATA_ROOT = "E:/Ashwin/importantFiles/Programming Projects/Forwardtesting/data"

def ensure_folder(symbol):
    folder_path = os.path.join(DATA_ROOT, symbol)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_dataframe(df, symbol, filename='merged.csv'):
    folder_path = ensure_folder(symbol)
    file_path = os.path.join(folder_path, filename)
    df.to_csv(file_path, index_label='datetime')  # <- important
    return file_path
