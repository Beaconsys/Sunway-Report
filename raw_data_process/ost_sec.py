import os
import pandas as pd
import ast
from datetime import datetime
import numpy as np
from pathlib import Path
import multiprocessing
from functools import partial

def process_ost(df, output_path):

    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values(by='time')

    df['data'] = df['data'].apply(lambda x: ast.literal_eval(x))

    df['read_sum'] = df['data'].apply(lambda x: sum([int(pair.split()[0]) * (2**i) for i, pair in enumerate(x)]))
    df['write_sum'] = df['data'].apply(lambda x: sum([int(pair.split()[1]) * (2**i) for i, pair in enumerate(x)]))

    df['read_ost'] = df['read_sum'].diff()
    df['write_ost'] = df['write_sum'].diff()

    df['read_ost'] /= 256.0
    df['write_ost'] /= 256.0

    df = df.drop(columns=['read_sum', 'write_sum', 'data'])

    df.to_csv(output_path, index=False)
    
    return df

def process_single_json(json_path, output_dir):
    try:
        df = pd.read_csv(json_path,
                        header=None,
                        quotechar='"',
                        delimiter=',',
                        names=['time', 'data'])

        target_ip = json_path.stem

        parts = json_path.parts
        year_name = parts[-4]
        month_name = parts[-3]
        day_name = parts[-2]

        date_output_dir = output_dir / f"{year_name}-{month_name}-{day_name}"
        date_output_dir.mkdir(parents=True, exist_ok=True)

        processed_df = process_ost(df, date_output_dir / f"{target_ip}.csv")
        
        print(f"Process done : {json_path}")
        return True
    except Exception as e:
        print(f"Error with {json_path}: {e}")
        return False

def process_json_files(root_dir):
    root_dir = Path(root_dir)
    output_dir = Path("ost_per_sec")
    output_dir.mkdir(exist_ok=True)

    json_files = []

    for year_dir in root_dir.glob("*"):
        if year_dir.is_dir():
            for month_dir in year_dir.glob("*"):
                if month_dir.is_dir():
                    for day_dir in month_dir.glob("*"):
                        if day_dir.is_dir():
                            day_json_files = list(day_dir.glob("*.json"))
                            json_files.extend(day_json_files)

    num_processes = multiprocessing.cpu_count()
    print(f"使用 {num_processes} 个进程并行处理 {len(json_files)} 个文件")

    with multiprocessing.Pool(processes=num_processes) as pool:
        process_func = partial(process_single_json, output_dir=output_dir)
        results = pool.map(process_func, json_files)

if __name__ == "__main__":
    root_dir = "lustre-server-1"
    process_json_files(root_dir)
