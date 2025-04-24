import multiprocessing
from cache import process_single_ip  # 假设原脚本保存为rpc.py

def main():
    target_ips = []

    for third in range(0, 7):
        max_fourth = 99
        for fourth in range(0, max_fourth + 1):
            ip = f"20.0.{third}.{fourth}"
            target_ips.append(ip)

    pool_size = multiprocessing.cpu_count() - 1 or 1
    with multiprocessing.Pool(pool_size) as pool:
        pool.map(process_single_ip, target_ips)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
