#!/bin/bash
for counter in 1 2 3 4 5 6 7 8 9
do
  python3 fib.py $counter &
done
sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> Logs/log_"$1".txt &
sudo python3 auto_kill.py 9
