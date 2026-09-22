# Storage Evolution for Exascale Supercomputers: Lessons from Sunway TaihuLight to OceanLight

## 1 Getting Started Instructions

This study analyzes eight years of production data from the Sunway TaihuLight and OceanLight supercomputers, covering workload evolution, scheduler and metadata pressure, architectural trade-offs, and application-level I/O pitfalls. Our study systematically compares the effectiveness and limitations of architectural upgrades, providing actionable insights for designing and optimizing next-generation supercomputers facing converged HPC-AI workloads, and offering solutions for job scheduling, resource management, and I/O system design. This project showcases our data processing and analysis scripts, as well as the data collected by Beacon<sup>+</sup>, an open-source and lightweight collection tool.

## 2 Detailed Instructions

### 2.1 Beacon<sup>+</sup> and Dataset.

Both TaihuLight and OceanLight have deployed Beacon<sup>+</sup> to collect the multi-layer performance data, including computing nodes, forwarding nodes, storage nodes, and job-running information. We have no authority to open the access or provide a simulator to access the Beacon or all these data. However, Beacon's code and part of the collected data (The data is processed to hide the user's information) can be accessed through the link below: 
https://github.com/Beaconsys/Beacon.

### 2.2 Workload_characterization/

This directory contains scripts for "Workload characterization", comparing representative applications on TaihuLight and OceanLight.

- `Figure3a_average_IO_volume.py` reproduces Figure 3a, the average I/O volume of matched LAMMPS, AWP, Kmeans, and SWLBM runs.
- `Figure3b_IO_bandwidth.py` reproduces Figure 3b, the I/O bandwidth of matched runs of the same applications.

### 2.3 HTC_AI/

This directory contains reproducible figures for "Workload-evolution challenges".

- `Figure4_job_submissions.py` reproduces Figure 4 from `TaihuLight_job_counts_1h.csv` and `OceanLight_job_counts_1h.csv`, showing hourly job-submission counts over the operational cycles of both systems.
- `Figure5_batch_parallelism_violin.py` reproduces Figure 5 from `Batch_parallelism_counts.csv`, showing the parallelism distributions in representative OceanLight submission bursts.
- `Figure6_HTC_interference.py` reproduces Figure 6, comparing HPC scheduling time with and without concurrent HTC-job interference.
- `Figure7_token_bucket.py` reproduces Figure 7, comparing direct scheduling and token-bucket admission control.
- `Figure8_MDS_utilization.py` reproduces Figure 8 from `MDS_utilization.csv`, comparing the distribution of MDS utilization.
- `Figure9_IO_performance_HPC_AI.py` reproduces Figure 9 from `HPC_AI_comparison.csv`, comparing the I/O bandwidth and metadata-operation rate of HPC and AI jobs.
- `Figure10_directory_depth.py` reproduces Figure 10 from `Directory_Depth.csv`, comparing the accessed directory-depth distributions.
- `Figure11_performance_degradation.py` reproduces Figure 11, the degradation-rate distribution of I/O-intensive jobs.
- `Figure12_MDS_request_time.py` reproduces the two panels of Figure 12, showing the distributions of MDS request waiting time and execution time.

### 2.4 Architectural_evolution/

This directory contains reproducible figures for "Architectural evolution and its consequences".

- `Figure13a_IO_interference.py` reproduces Figure 13a from `IO_interference_data.csv`, comparing the percentages of normal and degraded jobs.
- `Figure13b_degradation_severity.py` reproduces Figure 13b from the four anonymized read/write degradation CSV files, comparing degradation severity across the two systems.
- `Figure17a_forwarding_node_jobs.py` reproduces Figure 17a from `TaihuLight_FWD_jobs.csv` and `OceanLight_FWD_jobs.csv`, comparing forwarding-node job-load distributions.
- `Figure17b_file_access_proportion.py` reproduces Figure 17b from `File_access_proportions.csv`, comparing the proportions of jobs accessing different numbers of files.
- `Figure18_cache_hit_ratio.py` reproduces Figure 18 from `Cache_hit_ratio_comparation.csv`, comparing cache hit ratios with and without domain-aware forwarding scheduling.
- `Figure20_IO_bandwidth.py` reproduces Figure 20, comparing read and write bandwidth on TaihuLight, OceanLight GFS, and OceanLight HadaFS.
- `Figure21_HadaFS_Migration.py` reproduces Figure 21 from `Hada_RPC_data.csv`, showing compute-node read bandwidth and forwarding-node write bandwidth during HadaFS data migration.

### 2.5 Application_level_IO_pitfalls/

This directory contains reproducible figures for "Application-level I/O pitfalls".

- `Figure22_Write_Read_Bandwidth.py` reproduces Figure 22 from `GRIST_write.csv`, `GRIST_read.csv`, `CWRF_write.csv`, and `CWRF_read.csv`, comparing large-scale write and small-scale read bandwidth.
- `Figure23_Read_Bandwidth_Scaling.py` reproduces Figure 23, comparing read bandwidth across four NetCDF/HDF5 access modes and process counts.

### 2.6 Raw_data_process/*.py
This section contains scripts for processing the original JSON data. The parallel parameter indicates the parallel acceleration of the processing program.
