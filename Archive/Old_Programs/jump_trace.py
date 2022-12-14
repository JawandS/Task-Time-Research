#!/usr/bin/python
#
# trace context switch

from __future__ import print_function

import time

from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(text="""
TRACEPOINT_PROBE(sched, sched_switch) {
    //cat /sys/kernel/debug/tracing/events/sched/sched_switch/format
    bpf_trace_printk("%d\\n", args->prev_prio);
    return 0;
}
""")

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "TASK", "PID", "CPU"))

# capture previous data
prev_data = []
counter = 0
sub_counter = 0

# jump value
JUMP_VAL = 1

# start time
START_TIME = time.perf_counter()

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()  # (task, pid, cpu, flags, ts, msg)
        if counter % 100000 == 0:
            # print the time elapsed
            print(str(round(time.perf_counter() - START_TIME, 3)), end=" ")
            sub_counter += 1
            if sub_counter % 10 == 0:
                print("\n")
        if prev_data and ts - prev_data[4] > JUMP_VAL:
            # check there's prev data and the time jump is greater than 5
            print("\nTime jump:")
            print((prev_data[4], prev_data[0], prev_data[1], prev_data[2]))
            print((ts, task, pid, cpu))
            # update the previous data
            prev_data = (task, pid, cpu, flags, ts, msg)
        else:
            # store the previous data
            prev_data = (task, pid, cpu, flags, ts, msg)
        # printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    except ValueError:
        print("ValueError")
        continue
    except KeyboardInterrupt:
        exit()
    counter += 1
