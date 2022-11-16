#!/bin/bash
for counter in {1..500}
do
    sudo python3 model.py -1 quiet >> Run_Time_Experiment/20_core_run_time.txt & sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> temp.txt
    sudo python3 model.py -1 quiet >> Run_Time_Experiment/20_core_run_time.txt
    echo $counter
done
