#!/usr/bin/python
#
# trace context switch
import time
start_time = time.time()
from bcc import BPF

print("imports: " + str(time.time() - start_time))

# load BPF program: traces all context switches and logs them
b = BPF(text="""
TRACEPOINT_PROBE(sched, sched_switch) {
    // cat /sys/kernel/debug/tracing/events/sched/sched_switch/format
    bpf_trace_printk("%d\\n", args->prev_prio);
    return 0;
}
""")

print("BPF program set: " + str(time.time() - start_time))

# data structures
timeline = [] # capture context switch traces in chronological order
value_errors = 0 # number of times a value error occurs

"""
Collects data from the context switch trace and stores it in the data structures unique_task_counts and timeline
"""

print("Started tracing: " + str(time.time() - start_time))

while True:
    try:
        # get current time
        current_time = time.perf_counter()
        # capture data from trace
        data = b.trace_fields() # (task, pid, cpu, flags, ts, msg)
        # add data, current time, and time difference to timeline
        timeline.append([data[0], data[1], data[2], data[3], data[4], data[5], current_time, current_time - data[4]])
    except ValueError:
        # add to value error
        value_errors += 1
        # move to the next context switch
        continue
    except KeyboardInterrupt:
        # feedback to the user
        print("Finished tracing: " + str(time.time() - start_time) + " seconds")
        if value_errors:
            # only print if there are value errors to report
            print("value errors: " + str(value_errors))
        # write the differences to a file
        with open("Data/timeline.txt", "w") as fl:
            fl.write("task pid cpu flags real_time time_diff\n")
            # write the timeline and time differences to a file
            for counter in range(len(timeline)):
                fl.write(str(timeline[counter]) + "\n")
        # process the data
        from data_process import tracing_data_process
        tracing_data_process(timeline)
        # finished tracing, give feedback to the user
        print("Finished processing timeline, total run: " + str(round(time.time() - start_time, 3)) + " seconds")
        # exit the program
        exit()
