import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect("../Sunway.db")
cursor = conn.cursor()
query = """
SELECT jobid, submittime, nodenum, runtime 
FROM Haiyang_job_info
WHERE queue = 'q_1' AND DATE(submittime) = '20xx-xx-xx'
ORDER BY submittime
"""
cursor.execute(query)
jobs = cursor.fetchall()
conn.close()

dataset = []
for job in jobs:
    jobid, submittime, nodenum, runtime = job
    submittime = datetime.strptime(submittime, "%Y-%m-%d %H:%M:%S")
    dataset.append({
        "jobid": jobid,
        "submittime": submittime,
        "nodenum": nodenum,
        "runtime": runtime,
        "scheduled": False,
        "wait_time": 0,
        "borrowed_nodes": 0
    })

other_df = pd.read_csv("other_queue.csv")
other_node_status = {
    datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S"): int(row['available_nodes'])
    for _, row in other_df.iterrows()
}

TOTAL_NODES = 15000
available_nodes = [True] * TOTAL_NODES
running_jobs = []
waiting_queue = []
wait_times = []

current_time = datetime(2023, 5, 1, 0, 0, 0)
end_time = datetime(2023, 5, 2, 0, 0, 0)

while current_time < end_time:
    for job in running_jobs[:]:
        if job["end_time"] <= current_time:
            for i in job["allocated_nodes"]:
                available_nodes[i] = True
            # 归还借用节点
            if job["borrowed_nodes"] > 0:
                if current_time in other_node_status:
                    other_node_status[current_time] += job["borrowed_nodes"]
                else:
                    other_node_status[current_time] = job["borrowed_nodes"]
            running_jobs.remove(job)

    waiting_queue.sort(key=lambda job: (
        job["nodenum"],
        (current_time - job["submittime"]).total_seconds() if (current_time - job["submittime"]).total_seconds() > 3000 else 0
    ))
    for job in waiting_queue[:]:
        free_nodes = [i for i, free in enumerate(available_nodes) if free]
        required = job["nodenum"]

        if len(free_nodes) >= required:
            allocated = free_nodes[:required]
            for i in allocated:
                available_nodes[i] = False
            job["scheduled"] = True
            job["start_time"] = current_time
            job["end_time"] = current_time + timedelta(seconds=job["runtime"])
            job["allocated_nodes"] = allocated
            job["borrowed_nodes"] = 0
            job["wait_time"] = (current_time - job["submittime"]).total_seconds()
            running_jobs.append(job)
            waiting_queue.remove(job)
            wait_times.append(job["wait_time"])
            print(f"{current_time}: Job {job['jobid']} started from queue, waited {job['wait_time']} sec.")
        else:
            remaining = required - len(free_nodes)
            other_available = other_node_status.get(current_time, 0)
            if other_available >= remaining:
                allocated = free_nodes[:len(free_nodes)]
                for i in allocated:
                    available_nodes[i] = False
                job["scheduled"] = True
                job["start_time"] = current_time
                job["end_time"] = current_time + timedelta(seconds=job["runtime"])
                job["allocated_nodes"] = allocated
                job["borrowed_nodes"] = remaining
                job["wait_time"] = (current_time - job["submittime"]).total_seconds()
                other_node_status[current_time] -= remaining
                running_jobs.append(job)
                waiting_queue.remove(job)
                wait_times.append(job["wait_time"])
                print(f"{current_time}: Job {job['jobid']} started with {remaining} borrowed nodes, waited {job['wait_time']} sec.")

    while dataset and dataset[0]["submittime"] <= current_time:
        job = dataset.pop(0)
        waiting_queue.append(job)

    current_time += timedelta(seconds=1)

if wait_times:
    avg_wait = sum(wait_times) / len(wait_times)
    print(f"\nAverage wait time: {avg_wait:.2f} seconds")
else:
    print("No jobs were scheduled.")
