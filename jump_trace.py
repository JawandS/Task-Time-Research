#!/usr/bin/python
#
# trace context switch

from __future__ import print_function
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

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields() # (task, pid, cpu, flags, ts, msg)
        if counter % 10000 == 0:
            printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
        if prev_data and ts - prev_data[4] > 5:
            # check there's prev data and the time jump is greater than 5
            print("Time jump start\n\n\n")
            print((prev_data[4], prev_data[0], prev_data[1], prev_data[2]))
            print((ts, task, pid, cpu))
            print("\n\n\nTime jump end")
            # update the previous data
            prev_data = (task, pid, cpu, flags, ts, msg)
        else:
            # store the previous data
            prev_data = (task, pid, cpu, flags, ts, msg)
    except ValueError:
        print("ValueError")
        continue
    except KeyboardInterrupt:
        exit()
    counter += 1
