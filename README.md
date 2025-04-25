# Job Characteristics and I/O Behavior on Sunway TaihuLight and Sunway OceanLight
## 1 Getting Started Instructions
This study presents a comprehensive analysis of workload characteristics and I/O behaviors across two generations of Sunway supercomputers (TaihuLight and OceanLight). Our study systematically compares the effectiveness and limitations of architectural upgrades, providing actionable insights for designing and optimizing next-generation supercomputers facing converged HPC-AI workloads, and offering solutions for job scheduling, resource management, and I/O system design. This project showcases our data processing and analysis scripts, as well as the data collected by Beacon<sup>+</sup>, an open-source and lightweight collection tool.
## 2 Detailed Instructions
### 2.1 Beacon<sup>+</sup> and Dataset.
Both TaihuLight and OceanLight have deployed Beacon<sup>+</sup> to collect the multi-layer performance data, including computing nodes, forwarding nodes, storage nodes, and job-running information. We have no authority to open the access or provide a simulator to access the Beacon or all these data. However, Beacon's code and part of the collected data (The data is processed to hide the user's information) can be accessed through the link blew: 
https://github.com/Beaconsys/Beacon.
### 2.2 job_characteristics/*.py
This section contains all the plotting scripts and data for the job runing information section of the experiments. We provide the processed secondary data, and the charts can be reproduced simply by running the scripts. All necessary data are either embedded within the Python scripts or included as standalone files in the corresponding directory.
- Abnormal rate.py presents a comparison of job abnormal termination rates on TaihuLight and OceanLight.
- Number and abnormal rate.py presents the relationship between the number of large-scale job submissions and the abnormal termination rate of small- scale jobs.
- Affected and unaffected.py presents the abnormal termination rates of affected and unaffected small-scale jobs.
- Balanced scheduling algorithm.py implements a queue scheduling algorithm designed for small job dispersion and load balancing. And Balanced scheduling heatmap.py is plotted using file heatmap_data.pkl and presents a heatmap of scheduling result.
- Waiting of queues.py presents the average job waiting time of three types of queues.
- Elastic scheduling algorithm.py implements an elastic queue scheduling algorithm. The key idea of this algorithm lies in its cross-queue scheduling and resource reclamation mechanism.
- HPC jobs’ scheduling time.py presents the comparison of HPC jobs’ scheduling time under varying parallelism with and without HTC job interference.
### 2.3 analysis_app_io
This section contains all the plotting scripts and data for the application I/O section of the experiments. We provide the processed secondary data, and the charts can be reproduced simply by running the scripts. All necessary data are either embedded within the Python scripts or included as standalone files in the corresponding directory.
#### 2.3.1 job_IO_chara_comparsion
- job IO characteristics.py presents the comparison of job I/O characteristics on TaihuLight and OceanLight.
- data.csv contains the processed data required for plotting the figure.
#### 2.3.2 application_comparsion
- application_comparison presents a comparison of the application domain distribution on TaihuLight and OceanLight.
#### 2.3.3 IO_comparsion_AIandHPC
- IO comparison HPC AI.py presents I/O performance comparison between HPC workloads and AI workloads on OceanLight.
- data.csv contains the processed data required for plotting the figure.
### 2.4 analysis_sys/*.py
his section contains all the plotting scripts and data for the storage system workload section of the experiments. We provide the processed secondary data, and the charts can be reproduced simply by running the scripts. All necessary data are either embedded within the Python scripts or included as standalone files in the corresponding directory.
- OST CDF.py presents a CDF of OST utilization on two supercomputers.
- OST cumulative volume.py presents the cumulative I/O volume on OceanLight.
- OST burst rw.py presents the duration and I/O volume of burst on OceanLight.
- Cache hit rate burst volume.py presents the cache hit rate and read burst volume on OceanLight.
- Cache hit data.csv contains the processed data required for plotting the figure.
- COV_OST.py presents the CoV and load status of OSTs on OceanLight.
- COV_FWD.py presents the CoV and load status of forwarding nodes on OceanLight.
- IO interference.py presents a comparison of I/O interference on TaihuLight and OceanLight.
- IO interference_data.csv ontains the processed data required for plotting the figure.
- MDS CDF.py presents the CDF of MDS utilization on TaihuLight and OceanLight.
- MDS operation.py presents the Major metadata operations and operation numbers on TaihuLight and OceanLight.

