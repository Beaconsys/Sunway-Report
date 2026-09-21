import multiprocessing
from mds import process_single_ip  # 假设原脚本保存为rpc.py

def main():
    target_ips = [
        "20.0.10.1_0",
        "20.0.10.2_1",
        "20.0.10.3_2",
        "20.0.10.4_3"
    ]
    pool_size = multiprocessing.cpu_count() - 1 or 1
    with multiprocessing.Pool(pool_size) as pool:
        pool.map(process_single_ip, target_ips)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
