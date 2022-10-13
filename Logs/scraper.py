def trace_logs(log_num):
    # variables
    log = "log_" + log_num + ".txt"
    # read the file
    with open(log, "r") as f:
        data = {}  # store the data
        # iterate  through the lines and add it to data
        for counter, line in enumerate(f):
            # skip the first line (header) or any new line
            if counter == 0 or line == "\n":
                continue
            # split the data
            line_val = line.strip().split(" ")
            # if the line is empty skip it
            if len(line_val) == 0:
                continue
            # get the values and add it to data
            cpu_num = int(line_val[2])
            if cpu_num not in data:
                data[cpu_num] = []
            data[cpu_num].append((line_val[0], int(line_val[1]), int(line_val[3])))  # pname, pid, ts
        # CPU time for each process
        task_time = {}
        pid_time = {}
        # average length for context switch on each cpu
        cpu_total = {i: 0 for i in range(len(data))}
        cpu_switches = {i: 0 for i in range(len(data))}
        # iterate through the data by cpu
        for cpu_num in data:
            prev_ts = 0  # previous timestamp
            for vals in data[cpu_num]:
                # get the values
                pname, pid, ts = vals[0], vals[1], vals[2]
                if not prev_ts:  # continue if it's the first timestamp
                    prev_ts = ts
                    continue
                # calculate the difference
                diff = ts - prev_ts
                # add the absolute value of the difference to the total
                if pname not in task_time:
                    task_time[pname] = 0
                task_time[pname] += diff
                if pid not in pid_time:
                    pid_time[pid] = 0
                pid_time[pid] += diff
                # add the difference to the cpu total
                cpu_total[cpu_num] += diff
                cpu_switches[cpu_num] += 1

    # print average length between context switch in seconds for each CPU
    for cpu_num in range(len(data)):
        print("CPU " + str(cpu_num))
        print("\tTotal: " + str(cpu_total[cpu_num] / 1e+9) + "s")
        print("\tAverage: " + str((cpu_total[cpu_num] / cpu_switches[cpu_num]) / 1e+9) + "s")
    # calculate total time for all processes vs total time for all processors
    print("Total task time: " + str(sum(task_time.values()) / 1e+9))
    print("Total pid time: " + str(sum(pid_time.values()) / 1e+9))
    print("Total cpu time: " + str(sum(cpu_total.values()) / 1e+9))

    # save the data to a file
    with open("processed_" + log_num + ".txt", "w") as f:
        for cpu_num in range(len(data)):
            # average time spent on CPU
            f.write("CPU " + str(cpu_num) + "\n")
            f.write("\tTotal: " + str(cpu_total[cpu_num] / 1e+9) + "s\n")
            f.write("\tAverage: " + str((cpu_total[cpu_num] / cpu_switches[cpu_num]) / 1e+9) + "s\n")
        # calculate total time for all processes vs total time for all processors
        f.write("Total task time: " + str(sum(task_time.values()) / 1e+9) + "\n")
        f.write("Total pid time: " + str(sum(pid_time.values()) / 1e+9) + "\n")
        f.write("Total cpu time: " + str(sum(cpu_total.values()) / 1e+9) + "\n\n")
        # print the time spent on each process
        total_time_spent = sum(cpu_total.values())
        for task in task_time:
            f.write(task + " " + str(task_time[task] / 1e+9) + " " + str(round((task_time[task] / total_time_spent) * 100, 3)) + "%\n")
        print("\n")
        for pid in pid_time:
            f.write(str(pid) + " " + str(pid_time[pid] / 1e+9) + "\n")


if __name__ == "__main__":
    trace_logs(log_num="1")
    # B=0.0019169486051582826, C=0.0019187149509847137, D=0.00682865379853148