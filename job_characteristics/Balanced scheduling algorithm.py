# simulate_scheduler
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pickle

conn = sqlite3.connect("../Sunway.db")
cursor = conn.cursor()

query = """
SELECT jobid, submittime, nodenum, runtime 
FROM Taihu_job_info
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
        "wait_time": 0
    })

TOTAL_NODES = 4096
GROUP_COUNT = 8
NODES_PER_GROUP = TOTAL_NODES // GROUP_COUNT
available_nodes = [True] * TOTAL_NODES
running_jobs = []
waiting_queue = []
wait_times = []
heatmap_data = np.zeros((GROUP_COUNT, 24), dtype=int)

current_time = datetime(2018, 5, 14, 0, 0, 0)
end_time = datetime(2018, 5, 15, 0, 0, 0)

while current_time < end_time:
    for job in running_jobs[:]:
        if job["end_time"] <= current_time:
            for i in job["allocated_nodes"]:
                available_nodes[i] = True
            running_jobs.remove(job)

    if current_time.minute == 0 and current_time.second == 0:
        hour_index = current_time.hour
        for group_id in range(GROUP_COUNT):
            start = group_id * NODES_PER_GROUP
            end = (group_id + 1) * NODES_PER_GROUP
            used_nodes = sum(not available_nodes[i] for i in range(start, end))
            if used_nodes <= 127:
                heatmap_data[group_id, hour_index] = 1
            elif used_nodes <= 255:
                heatmap_data[group_id, hour_index] = 2
            elif used_nodes <= 383:
                heatmap_data[group_id, hour_index] = 3
            else:
                heatmap_data[group_id, hour_index] = 4

    waiting_queue.sort(key=lambda job: (
        job["nodenum"],
        (current_time - job["submittime"]).total_seconds() if (current_time - job["submittime"]).total_seconds() > 3000 else 0
    ))
    for job in waiting_queue[:]:
        free_nodes = [i for i, free in enumerate(available_nodes) if free]
        if job["nodenum"] < 64:
            group_free_nodes = {
                gid: [i for i in range(gid * NODES_PER_GROUP, (gid + 1) * NODES_PER_GROUP) if available_nodes[i]]
                for gid in range(GROUP_COUNT)
            }
            allocated = []
            if len(group_free_nodes[7]) >= job["nodenum"]:
                allocated = group_free_nodes[7][:job["nodenum"]]
            else:
                max_gid = max(group_free_nodes, key=lambda g: len(group_free_nodes[g]))
                first = group_free_nodes[max_gid][:min(len(group_free_nodes[max_gid]), job["nodenum"])]
                allocated.extend(first)
                remaining = job["nodenum"] - len(first)
                if remaining > 0:
                    for gid in range(GROUP_COUNT):
                        if gid == max_gid: continue
                        more = group_free_nodes[gid][:min(len(group_free_nodes[gid]), remaining)]
                        allocated.extend(more)
                        remaining -= len(more)
                        if remaining == 0:
                            break
            if len(allocated) == job["nodenum"]:
                for i in allocated: available_nodes[i] = False
                job.update({
                    "scheduled": True,
                    "start_time": current_time,
                    "end_time": current_time + timedelta(seconds=job["runtime"]),
                    "allocated_nodes": allocated,
                    "wait_time": (current_time - job["submittime"]).total_seconds()
                })
                running_jobs.append(job)
                waiting_queue.remove(job)
                wait_times.append(job["wait_time"])
        else:
            allocated, needed = [], job["nodenum"]
            while needed > 0:
                if sum(available_nodes) < needed: break
                for gid in range(GROUP_COUNT):
                    group_free = [i for i in range(gid * NODES_PER_GROUP, (gid + 1) * NODES_PER_GROUP) if available_nodes[i]]
                    if group_free:
                        batch = group_free[:min(64, needed, len(group_free))]
                        allocated.extend(batch)
                        for node in batch: available_nodes[node] = False
                        needed -= len(batch)
                        if needed == 0: break
            if needed == 0:
                job.update({
                    "scheduled": True,
                    "start_time": current_time,
                    "end_time": current_time + timedelta(seconds=job["runtime"]),
                    "allocated_nodes": allocated,
                    "wait_time": (current_time - job["submittime"]).total_seconds()
                })
                running_jobs.append(job)
                waiting_queue.remove(job)
                wait_times.append(job["wait_time"])
            else:
                for node in allocated: available_nodes[node] = True

    while dataset and dataset[0]["submittime"] <= current_time:
        job = dataset.pop(0)
        if waiting_queue:
            waiting_queue.append(job)
        else:
            free_nodes = [i for i, free in enumerate(available_nodes) if free]
            if job["nodenum"] < 64 and len(free_nodes) >= job["nodenum"]:
                allocated = free_nodes[:job["nodenum"]]
                for i in allocated: available_nodes[i] = False
                job.update({
                    "scheduled": True,
                    "start_time": current_time,
                    "end_time": current_time + timedelta(seconds=job["runtime"]),
                    "allocated_nodes": allocated,
                    "wait_time": 0
                })
                running_jobs.append(job)
                wait_times.append(0)
            else:
                waiting_queue.append(job)

    current_time += timedelta(seconds=1)

if wait_times:
    print(f"Average wait time: {sum(wait_times) / len(wait_times):.2f} seconds")
else:
    print("No jobs were scheduled.")

with open("heatmap_data.pkl", "wb") as f:
    pickle.dump(heatmap_data, f)
