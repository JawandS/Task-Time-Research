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
    // do nothing
    bpf_trace_printk("%d\\n", args->prev_prio);
    // bpf_trace_printk("1");
    return 0;
}
""")

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "GOTBITS"))

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()
    printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
