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

# format output
while 1:
    try:
        data = b.trace_fields() # (task, pid, cpu, flags, ts, msg)
        if prev_data and data[4] - prev_data[4] > 5:
            # check there's prev data and the time jump is greater than 5
            printb(b"%-18.9f %-16s %-6d %s" % (prev_data[4], prev_data[0], prev_data[1], prev_data[2]))
            printb(b"%-18.9f %-16s %-6d %s" % (data[4], data[0], data[1], data[2]))
            # update the previous data
            prev_data = data
        else:
            # store the previous data
            prev_data = data
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()
