import pandas as pd
from pathlib import Path

def diff_adjacent_rows(group):
    data_columns = group.columns.difference(['time', 'node'])
    diff_result = group[data_columns].astype(int).diff().iloc[1:]
    diff_result['time'] = group['time'].iloc[1:]
    return diff_result

def process_mds(mds_df, out_path):
    mds_df['data'] = mds_df['data'].str[1:-1]

    split_columns = mds_df['data'].str.split(",", expand=True)
    split_columns.columns = [f'col_{i + 1}' for i in range(16)]
    mds_df = pd.concat([mds_df, split_columns], axis=1)
    mds_df.drop(columns=['data'], inplace=True)
    grouped = mds_df.groupby(['node'])
    result = grouped.apply(diff_adjacent_rows).reset_index(level=1, drop=True)

    final_res = result.groupby(['time']).sum()
    # print(final_res)
    final_res.to_csv(out_path)

def is_ip_in_range(ip):
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False

        if parts[0] != '17' or parts[1] != '0':
            return False

        third = int(parts[2])
        if third < 0 or third > 6:
            return False

        fourth = int(parts[3])
        if fourth < 0 or fourth > 100:
            return False

        if third == 6 and fourth > 30:
            return False

        return True
    except:
        return False

def process_single_ip(target_mds):
    base_path = Path(__file__).parent / "lustre-mds-1" 

    for date_dir in base_path.glob("*/*/*"):
        rel_parts = date_dir.relative_to(base_path).parts

        if len(rel_parts) != 3:
            continue

        year, month, day = rel_parts

        json_path = date_dir / f"{target_mds}.json"
        if not json_path.exists():
            continue

        output_dir = Path("data/mds_csv_selected") / year / month / day
        output_dir.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(json_path,
                         header=None,
                         quotechar='"',
                         delimiter=',',
                         index_col=False,
                         names=['time', 'node', 'data'])
        df = df.sort_values('time')
        df['time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        mask = df['node'].apply(is_ip_in_range)
        df = df[mask]

        if not df.empty:
            print(f"Processed: {output_dir}/{target_mds}.csv")
            process_mds(df, output_dir / f"{target_mds}.csv")
        else:
            print(f"Skipped empty dataframe for: {target_mds}")

if __name__ == "__main__":
    target_mds = "20.0.10.1_0"
    process_single_ip(target_mds)