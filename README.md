# TF-Analysis
### TensorFlow Analysis using bpftrace 
##

Run data collection:  
bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }'

- Using bpftrace to trace context switches
- model.py is a TensorFlow deep learning job that automatically kills tracing
- The timeline is analyzed with processing.py
- fib.py is a fibonacci job (does not kill tracing)

-------------------------- 
**Notes for project version in Archive**  
General notes:
- The first 2k elements of the raw timeline are saved
- Processes like kworker/# are combined to kworker  
- CPU usage doesn't include <idle>

Visuals/Data Generated:  
- Breakdown (chart of the time spent during the job)
- CPU_usage (time spent on each CPU)  
- Task_counts (unique PID per task)  
- Task_times (time spent on each task, combines all PID)  
- TT_no_idle (time spent on tasks, excluding idle
- Text file (name is the average lifespan for python processes)
  
Files Descriptions:  
- model.py (sequential neural network with timestamps)  
- context_switch_timeline.py (tracer that generates a timeline of context switches)  
- data_process.py (processes the timeline from the tracer to get information)  
- visualizer.py (generates graphs and copies data to Run_Data)  
- Run_Data/analyzer.py (performs further analysis on collected data)
- Archives (contains old files and data)  
- Data (contains data necessary during the run)  
- Run_Data (stores visuals and data)
  
Server:  
- Ubuntu 20.04 on https://www.cloudlab.us/  

Setup notes:  
- Package names vary based on Ubuntu version  
- BCC or eBPF may require kernel flags to be changed  
- The version for linux-headers can be found with (uname -r)  
- Need your username and access token to clone the repo

References:
- https://aditya-bhattacharya.net/2020/07/11/time-series-tips-and-tricks/2/
- https://www.tensorflow.org/tutorials/structured_data/time_series
- https://arxiv.org/pdf/2103.06915.pdf
