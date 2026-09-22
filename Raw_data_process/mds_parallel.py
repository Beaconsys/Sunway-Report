import multiprocessing
from mds import process_single_ip 

def main():
    target_ips = [
        "x.x.x.x_0",
        "x.x.x.x_1",
        "x.x.x.x_2",
        "x.x.x.x_3"
    ]
    pool_size = multiprocessing.cpu_count() - 1 or 1
    with multiprocessing.Pool(pool_size) as pool:
        pool.map(process_single_ip, target_ips)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
