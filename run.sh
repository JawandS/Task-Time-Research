#!/bin/bash
sudo python3 model.py "$1" & sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> Logs/log_"$1".txt
