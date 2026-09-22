import pandas as pd
from pathlib import Path

def diff_adjacent_rows(group):
    data_columns = group.columns.difference(['time', 'part'])
    diff_result = group[data_columns].astype(int).diff().iloc[1:]
    diff_result['time'] = group['time'].iloc[1:]  # 保留 time 列
    return diff_result

def process_cache(cache_df, out_path):
    cache_df['data'] = cache_df['data'].str[2:-2]
    split_data = cache_df['data'].str.split(',', expand=True)
    cache_df['hit'] = split_data.iloc[:, 0].astype(int)
    cache_df['miss'] = split_data.iloc[:, 1].astype(int)
    cache_df['discard'] = split_data.iloc[:, 2].astype(int)
    cache_df.drop('data', axis=1, inplace=True)

    result = diff_adjacent_rows(cache_df)
    final_res = result.groupby(['time']).sum()
    final_res.to_csv(out_path)

def process_single_ip(target_ip):
    base_path = Path(__file__).parent / "lustre-client-1"  
    # print(base_path)

    for date_dir in base_path.glob("*/*/*"):
        rel_parts = date_dir.relative_to(base_path).parts

        if len(rel_parts) != 3:
            continue

        year, month, day = rel_parts

        json_path = date_dir / f"{target_ip}.json"
        if not json_path.exists():
            continue

        output_dir = Path("cache_data_sec") / year / month / day
        output_dir.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(json_path,
                         header=None,
                         quotechar='"',
                         delimiter=',',
                         names=['time', 'part', 'data'],
                         error_bad_lines=False)
        df = df.sort_values('time')
        # df['time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        cache_df = df[df['part'] == 'cache'].copy()

        if not cache_df.empty:
            print(f"Processed: {output_dir}/{target_ip}.csv")
            process_cache(cache_df, output_dir / f"{target_ip}.csv")
        else:
            print(f"Skipped empty dataframe for: {target_ip}")

if __name__ == "__main__":
    target_ip = "x.x.x.x"
    process_single_ip(target_ip)