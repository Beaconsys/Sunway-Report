import pandas as pd
from pathlib import Path

def calculate_rpc_sum(row , ost_dict):
    read_sum, write_sum= 0, 0
    for item in filter(None, row.data.split("'")):
        ost = item.split(',')[0]
        if not ost:
            continue
        t_read, t_write, count = 0,0,0
        for num in filter(None, item.split(',')[1:]):
            num1, num2 = num.strip().split()[:2]
            t_read += (1 << count) * int(num1)
            t_write += (1 << count) * int(num2)
            count += 1
        if ost in ost_dict:
            read_sum = read_sum + t_read - ost_dict[ost][0]
            write_sum = write_sum + t_write - ost_dict[ost][1]
        ost_dict[ost] = (t_read,t_write)
    return pd.Series([read_sum / 256.0, write_sum / 256.0], index=['read_sum', 'write_sum'])


def process_rpc(rpc_df, out_path):
    rpc_df['data'] = rpc_df['data'].str[1:-1]
    rpc_df = rpc_df.assign(read_sum=None, write_sum=None)

    ost_dict = {}
    for row in rpc_df.itertuples():
        read_val, write_val = calculate_rpc_sum(row, ost_dict)
        rpc_df.at[row.Index, 'read_sum'] = read_val
        rpc_df.at[row.Index, 'write_sum'] = write_val

    grouped_rpc = rpc_df.groupby('time')[['read_sum', 'write_sum']].sum().reset_index()
    grouped_rpc.to_csv(out_path, index=False)


def process_single_ip(target_ip):
    base_path = Path(__file__).parent / "lustre-client-1"

    for date_dir in base_path.glob("*/*/*"):
        rel_parts = date_dir.relative_to(base_path).parts

        if len(rel_parts) != 3:
            continue

        year, month, day = rel_parts

        json_path = date_dir / f"{target_ip}.json"
        if not json_path.exists():
            continue

        output_dir = Path("client_rpc_data") / year / month / day
        output_dir.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(json_path,
                         header=None,
                         quotechar='"',
                         delimiter=',',
                         names=['time', 'part', 'data'])
        df = df.sort_values('time')
        df['time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        rpc_df = df[df['part'] == 'rpc'].copy()
        process_rpc(rpc_df, output_dir / f"{target_ip}.csv")
        print(f"Processed: {output_dir}\\{target_ip}.csv")
