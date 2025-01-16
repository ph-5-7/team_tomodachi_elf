import pandas as pd
import os
import datetime

def load_all_data(data_dir):
    csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
    df_list = []
    for file_path in csv_files:
        df = pd.read_csv(file_path, encoding="utf-8")
        rename_dict = {"アイテム": "加工品", "商品名": "加工品", "アイテム名": "加工品"}
        df.rename(columns=rename_dict, inplace=True)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def get_end_of_day(date):
    return datetime.datetime.combine(date, datetime.time(23, 59, 59))
