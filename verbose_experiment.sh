#!/bin/bash
for counter in {1..3}
do
    sudo python3 model.py quiet & sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> temp.txt
    sudo python3 model.py quiet
    echo $counter
done
