#!/bin/bash
for counter in {1..500}
do
    sudo python3 model.py quiet >> Data/run_time.txt & sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> temp.txt
    sudo python3 model.py quiet >> Data/run_time.txt
    echo "Run $counter complete"
done