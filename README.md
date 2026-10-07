# Storage Evolution for Exascale Supercomputers: Lessons from Sunway TaihuLight to OceanLight

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC--BY--NC--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

This work is licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

## Persistent Archive

The version is archived on Zenodo:
https://doi.org/10.5281/zenodo.23201065

## 1 Getting Started Instructions

This study analyzes eight years of production data from the Sunway TaihuLight and OceanLight supercomputers, covering workload evolution, scheduler and metadata pressure, architectural trade-offs, and application-level I/O pitfalls. Our study systematically compares the effectiveness and limitations of architectural upgrades, providing actionable insights for designing and optimizing next-generation supercomputers facing converged HPC-AI workloads, and offering solutions for job scheduling, resource management, and I/O system design. This project showcases our data processing and analysis scripts, as well as the data collected by Beacon<sup>+</sup>, an open-source and lightweight collection tool.


### 1.1 Environment and dependencies

The plotting scripts run locally with Python, Matplotlib, NumPy, and pandas; no GPU or supercomputer access is required. The scripts were executed on a server with two Intel(R) Xeon(R) Silver 4214 CPUs at 2.20 GHz and 512 GB of DDR4 memory. The following package versions have been tested together:

| Dependency | Version |
| --- | --- |
| Python | 3.14.5 |
| Matplotlib | 3.11.1 |
| NumPy | 2.5.1 |
| pandas | 3.0.5 |

Install the Python packages with:

```text
python -m pip install matplotlib==3.11.1 numpy==2.5.1 pandas==3.0.5
```

Install Arial to match the figure fonts. On Debian/Ubuntu, run `sudo apt-get install ttf-mscorefonts-installer`; alternatively, install Arial `.ttf` files in the system font directory and refresh the font cache with `fc-cache -f`. Modules such as `pathlib`, `csv`, and `multiprocessing` are part of the Python standard library and require no separate installation.

Run each command below from the directory containing that script and its input CSV files. For example, enter `HTC_AI/` before running its scripts.

## 2 Detailed Instructions

### 2.1 Beacon<sup>+</sup> and Dataset.

Both TaihuLight and OceanLight have deployed Beacon<sup>+</sup> to collect the multi-layer performance data, including computing nodes, forwarding nodes, storage nodes, and job-running information. We have no authority to open the access or provide a simulator to access the Beacon or all these data. However, Beacon's code and part of the collected data (The data is processed to hide the user's information) can be accessed through the link below: 
https://github.com/Beaconsys/Beacon.

The following sections list all plotting scripts and associated processed data that can be publicly released.

### 2.2 Workload_characterization/

This directory contains scripts for "Workload characterization", comparing representative applications on TaihuLight and OceanLight.

- `Figure3a_average_IO_volume.py` reproduces Figure 3a, comparing average I/O volume for LAMMPS, AWP, Kmeans, and SWLBM.
  
  Data processing: Representative production runs are grouped by application and parallelism, and their I/O volumes are averaged for each system. The resulting application-level values are embedded in the script in MB. 
  
  Run: `python Figure3a_average_IO_volume.py`

- `Figure3b_IO_bandwidth.py` reproduces Figure 3b, comparing I/O bandwidth for matched application runs.
  
  Data processing: For each of the four applications, we select job records with matching parallelism, comparable I/O volume, and similar I/O characteristics, extract their average I/O bandwidth, and embed the resulting values in the script in GB/s.
  
  Run: `python Figure3b_IO_bandwidth.py`

### 2.3 HTC_AI/

This directory contains reproducible figures for "Workload-evolution challenges".

- `Figure4_job_submissions.py` reproduces Figure 4 from `TaihuLight_job_counts_1h.csv` and `OceanLight_job_counts_1h.csv`.
  
  Data processing: We count hourly job submissions on both supercomputers, and the CSV files provide the resulting statistics.
  
  Run: `python Figure4_job_submissions.py`

- `Figure5_batch_parallelism_violin.py` reproduces Figure 5 from `Batch_parallelism_counts.csv`.
  
  Data processing: We select four representative OceanLight submission bursts and summarize their job-parallelism distributions. The CSV retains `batch`, `parallelism`, and `job_count`; batch identities are replaced with `Batch 1` through `Batch 4`.
  
  Run: `python Figure5_batch_parallelism_violin.py`

- `Figure6_HTC_interference.py` reproduces Figure 6, comparing HPC scheduling times with and without concurrent HTC interference.
  
  Data processing: We first identify representative HTC job bursts, then measure the scheduling times of affected HPC jobs during these periods and group them by parallelism. We also measure scheduling times of jobs with the same parallelism during idle periods. Cases queued due to resource shortages are excluded. The resulting mean scheduling times are embedded in the plotting script.
  
  Run: `python Figure6_HTC_interference.py`

- `Figure7_token_bucket.py` reproduces Figure 7, comparing direct scheduling and token-bucket admission control.
  
  Data processing:  We use production-log replay from one burst submission to compare scheduling results under the two mechanisms. We record the average scheduling times of HTC, medium-scale, and large-scale jobs, as well as the elapsed time from the first submission to the last scheduling completion. These values are embedded in the plotting script in seconds.
  
  Run: `python Figure7_token_bucket.py`

- `Figure8_MDS_utilization.py` reproduces Figure 8 from `MDS_utilization.csv`.
  
  Data processing: MDS request counts in one-second intervals are normalized by the peak per-second count observed on the respective system. The cumulative fraction of intervals at or below each utilization level defines the distribution. The CSV retains prepared curve coordinates: utilization and the corresponding cumulative system-time percentages for both systems. 
  
  Run: `python Figure8_MDS_utilization.py`

- `Figure9_IO_performance_HPC_AI.py` reproduces Figure 9 from `HPC_AI_comparison.csv`.
  
  Data processing: For identified HPC and AI jobs, we extract the average metadata-operation rate and average I/O bandwidth of each job for comparison. The CSV retains only `avg_mdops` (operations/s), `total_iobw` (MB/s), and `workload_type`. Job IDs, usernames, application paths, and filenames are omitted. Each row supplies one scatter-plot point.
  
  Run: `python Figure9_IO_performance_HPC_AI.py`

- `Figure10_directory_depth.py` reproduces Figure 10 from `Directory_Depth.csv`.
  
  Data processing: Accessed directory paths are reduced to directory depths and grouped into `1-3`, `4-6`, `7-9`, `10-12`, `13-15`, `16-18`, and `19+`. The CSV retains the plotted proportions for each system and depth category.
  
  Run: `python Figure10_directory_depth.py`

- `Figure11_performance_degradation.py` reproduces Figure 11, showing degradation rates of affected I/O-intensive jobs.
  
  Data processing: We select the top 5% of jobs by metadata load and identify I/O-intensive jobs sharing their I/O paths and experiencing degradation. Their degradation ratios are grouped into `0-40%`, `40-60%`, `60-80%`, and `80-100%`. The percentages within the affected-job population are embedded for each system.
  
  Run: `python Figure11_performance_degradation.py`

- `Figure12_MDS_request_time.py` reproduces the two panels of Figure 12.
  
  Data processing: We summarize metadata-request waiting and execution times in seven millisecond intervals: `<0.010`, `0.010-0.10`, `0.10-1.0`, `1.0-10`, `10-100`, `100-1000`, and `>=1000`. For plotting, values labeled `<0.1` are represented as 0.05%, since they are invisible in the figure.
  
  Run: `python Figure12_MDS_request_time.py`

### 2.4 Architectural_evolution/

This directory contains reproducible figures for "Architectural evolution and its consequences".

- `Figure13a_IO_interference.py` reproduces Figure 13a from `IO_interference_data.csv`.
  
  Data processing: Beacon<sup>+</sup> identifies whether jobs exhibit normal or degraded performance. We separate jobs by system and read/write direction and summarize the proportion of each status. The CSV contains only `category`, `normal_ratio`, and `abnormal_ratio`.
  
  Run: `python Figure13a_IO_interference.py`

- `Figure13b_degradation_severity.py` reproduces Figure 13b from `TaihuLight_read_degradation.csv`, `TaihuLight_write_degradation.csv`, `OceanLight_read_degradation.csv`, and `OceanLight_write_degradation.csv`.
  
  Data processing: Degradation is calculated as `1 - degraded_bandwidth / normal_bandwidth` and separated by system and read/write direction. Each CSV retains only `degradation_percent`, stored as a fraction between 0 and 1, and `jobid`, replaced with a consecutive index starting at 1 within that file.
  
  Run: `python Figure13b_degradation_severity.py`

- `Figure17a_forwarding_node_jobs.py` reproduces Figure 17a from `TaihuLight_FWD_jobs.csv` and `OceanLight_FWD_jobs.csv`.
  
  Data processing: We examine job counts at representative forwarding nodes. These nodes remained active over the selected observation period. The prepared plotting samples are stored in long format, retaining only `fwd_node` and `job_number`. Physical node identifiers are replaced with local labels `FWD1` and `FWD2`, and timestamps are removed.
  
  Run: `python Figure17a_forwarding_node_jobs.py`

- `Figure17b_file_access_proportion.py` reproduces Figure 17b from `File_access_proportions.csv`.
  
  Data processing: We examine jobs served by representative forwarding nodes over an observation period and count the files accessed by each job at its forwarding node. We then group jobs by file-count range and compute the proportion in each range. The CSV file retains only the ranges and percentages.
  
  Run: `python Figure17b_file_access_proportion.py`

- `Figure18_cache_hit_ratio.py` reproduces Figure 18 from `Cache_hit_ratio_comparation.csv`.
  
  Data processing: We compare application-level cache-hit ratios under default mapping and domain-aware forwarding scheduling. The CSV retains each application's plotted ratios in `default` and `domain_aware_scheduling`, both on a 0--1 scale. Only application names appearing in the paper and these two metrics remain; usernames, job IDs, paths, and node identifiers are omitted.
  
  Run: `python Figure18_cache_hit_ratio.py`

- `Figure20_IO_bandwidth.py` reproduces Figure 20, comparing read/write bandwidth on TaihuLight, OceanLight GFS, and OceanLight HadaFS.
  
  Data processing: We select jobs at a scale of 1024 processes and separate their read/write bandwidth by storage configuration (HadaFS or GFS). The figure's lower quartile, median, upper quartile, and lower/upper whisker values are embedded in MB/s for each group.
  
  Run: `python Figure20_IO_bandwidth.py`

- `Figure21_HadaFS_Migration.py` reproduces Figure 21 from `Hada_RPC_data.csv`.
  
  Data processing: We select a representative interval in which background data migration affects application performance; during this interval, an application running on 106 compute nodes is affected by the background traffic. Application read bandwidth and forwarding-node write bandwidth are aligned over that interval. The CSV retains the prepared curve values in `read_gb` and `write_gb` (both GB/s), with time represented as elapsed `minutes`.
  
  Run: `python Figure21_HadaFS_Migration.py`

### 2.5 Application_level_IO_pitfalls/

This directory contains reproducible figures for "Application-level I/O pitfalls".

- `Figure22_Write_Read_Bandwidth.py` reproduces Figure 22 from `GRIST_write.csv`, `GRIST_read.csv`, `CWRF_write.csv`, and `CWRF_read.csv`.
  
  Data processing: We select all GRIST and CWRF jobs, classify them by scale and read/write dominance into large-scale writes and small-scale post-processing workloads, and cross-check the classifications with users. We then compute the average read and write bandwidths of these jobs. The prepared plotting samples are retained as `io_bandwidth_mb_s`, rounded to two decimal places, and original job identifiers are replaced with a file-local `job_id` sequence starting at 0.
  
  Run: `python Figure22_Write_Read_Bandwidth.py`

- `Figure23_Read_Bandwidth_Scaling.py` reproduces Figure 23, comparing four NetCDF/HDF5 access modes.
  
  Data processing: We compare a NetCDF-4 variable of shape `(1600000, 100)` and chunks of shape `(1600000, 1)` under misaligned reads, an enlarged chunk cache, a transposed layout, and chunk-aligned reads. The figure's read-bandwidth results in MB/s for 1, 2, 4, 8, and 16 processes are embedded as four arrays. The script draws these summarized results.
  
  Run: `python Figure23_Read_Bandwidth_Scaling.py`

### 2.6 Raw_data_process/*.py

This section contains scripts for processing the original Beacon log exports. The `_parallel` suffix indicates multiprocessing. These utilities require the corresponding private logs and configured target identifiers; they are not needed to run the plotting scripts. They use pandas 1.3.0 and NumPy 1.21.0 in a separate Python 3.8 environment because `cache.py` uses the older pandas `error_bad_lines` argument.

```text
python -m pip install pandas==1.3.0 numpy==1.21.0
```

Run the following commands from `Raw_data_process/` after supplying the expected inputs and configuring the targets.

- `cache.py` reads `lustre-client/YYYY/MM/DD/<target>.json`, selects cache records, parses hit/miss/discard counters, differences adjacent counter values, and sums the increments by timestamp. Results are written to `cache_data_sec/YYYY/MM/DD/<target>.csv`.
  
  Run: `python cache.py`

- `cache_parallel.py` applies the same cache-counter processing to the configured target list using worker processes.
  
  Run: `python cache_parallel.py`

- `mds.py` reads `lustre-mds/YYYY/MM/DD/<target>.json`, selects configured nodes, parses 16 counters, differences them within each node, and aggregates the increments under minute-resolution time labels. Results are written to `data/mds_csv_selected/YYYY/MM/DD/<target>.csv`.
  
  Run: `python mds.py`

- `mds_parallel.py` applies the same MDS-counter processing to the configured target list using worker processes.
  
  Run: `python mds_parallel.py`

- `rpc.py` reads `lustre-client/YYYY/MM/DD/<target>.json`, selects RPC records, weights histogram bin counts by `2**i`, differences the totals for each OST, divides by 256, and aggregates under minute-resolution time labels. Results are written to `client_rpc_data/YYYY/MM/DD/<target>.csv`.
  
  Run: `python rpc.py`

- `rpc_parallel.py` applies the same RPC processing to the configured target list using worker processes.
  
  Run: `python rpc_parallel.py`

- `ost_sec.py` reads `lustre-server/YYYY/MM/DD/*.json`, reconstructs read/write totals from weighted histogram counts, differences successive totals, and divides by 256. Results are written to `ost_per_sec/YYYY-MM-DD/<target>.csv`.
  
  Run: `python ost_sec.py`
