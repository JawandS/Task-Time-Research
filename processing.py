# split the log into separate logs for each CPU
def split_by_CPU(file_name):
    # split the log into a dictionary per CPU
    data = {}
    with open(file_name, "r") as f:
        for idx, line in enumerate(f):
            if line == "\n" or idx == 0:
                continue
            # get the values
            vals = line.split()
            pname, pid, cpu_num, ts = vals[0], vals[1], vals[2], vals[3]
            pid, cpu_num, ts = int(pid), int(cpu_num), int(ts)
            # add the values to the dictionary
            if cpu_num not in data:
                data[cpu_num] = []
            data[cpu_num].append((pname, pid, ts))
    return data


def trace_logs(log_num):
    # variables
    log = "Logs/log_" + log_num + ".txt"
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
                # update the prev timestamp and values
                prev_ts = ts

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
    with open("Data/processed_" + log_num + ".txt", "w") as f:
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
            f.write(task + " " + str(task_time[task] / 1e+9) + " " + str(
                round((task_time[task] / total_time_spent) * 100, 3)) + "%\n")
        print("\n")
        for pid in pid_time:
            f.write(str(pid) + " " + str(pid_time[pid] / 1e+9) + "\n")


# a function that calculates the percent time each process takes on each CPU
def process_time_by_CPU(log_num):
    data = split_by_CPU("Logs/log_" + log_num + ".txt")
    # calculate the time for each process on each CPU
    process_time = {}
    # total time for each CPU
    cpu_total = {i: 0 for i in range(len(data))}
    # go through each CPU's log
    for cpu_num in range(len(data)):
        # calculate the total time for the CPU
        cpu_total[cpu_num] = data[cpu_num][-1][2] - data[cpu_num][0][2]
        # previous timestamp
        prev_ts = 0
        # go through the CPU's log
        for idx, vals in enumerate(data[cpu_num]):
            # get data
            pname, pid, ts = vals[0], vals[1], vals[2]
            if idx == 0:
                prev_ts = ts
                continue
            # calculate the time
            time_diff = ts - prev_ts
            # add the time to the dictionary
            if cpu_num not in process_time:
                process_time[cpu_num] = {}
            if pname not in process_time[cpu_num]:
                process_time[cpu_num][pname] = 0
            process_time[cpu_num][pname] += time_diff
            # update the previous timestamp
            prev_ts = ts
    # calculate the percent time for each process on each CPU
    process_percent_time = {}
    for cpu_num in range(len(data)):
        if cpu_num not in process_percent_time:
            process_percent_time[cpu_num] = {}
        for pname in process_time[cpu_num]:
            process_percent_time[cpu_num][pname] = process_time[cpu_num][pname] / cpu_total[cpu_num]

    with open("Data/by_CPU_" + log_num + ".txt", "w") as f:
        for cpu_num in range(len(data)):
            f.write(f"CPU {cpu_num} total time: {cpu_total[cpu_num] / 1e+9}\n")
            for pname in process_percent_time[cpu_num]:
                f.write(f"{pname}: {round(process_percent_time[cpu_num][pname] * 100, 3)}%\n")
            f.write("\n")

def check_diffs(log_num, min_diff):
    file_name = "Logs/log_" + log_num + ".txt"
    data = split_by_CPU(file_name)
    max_difference = 0
    with open("Data/time_diffs_" + log_num + ".txt", "w") as f:
        for cpu_num in range(len(data)):
            f.write(f"CPU {cpu_num} total difference: {(data[cpu_num][-1][2] - data[cpu_num][0][2]) / 1e+9}\n")
            prev_ts = 0
            prev_data = []
            for counter, vals in enumerate(data[cpu_num]):
                # get the values
                pname, pid, ts = vals[0], vals[1], vals[2]
                if not prev_ts:
                    prev_ts = ts
                    prev_data = [pname, pid, ts]
                    continue
                # calculate the difference
                diff = (int(ts) - int(prev_ts)) / 1e+9
                # check if the difference (in seconds) is greater than 0.1
                if diff > min_diff:
                    f.write("Difference greater than 0.1: " + str(diff) + "\n")
                    f.write(str(prev_data) + "\n")
                    f.write(str(vals) + "\n")
                    f.write("---\n")
                # update the max difference
                if diff > max_difference:
                    max_difference = diff
                # update the prev timestamp
                prev_ts = ts
                prev_data = [pname, pid, ts]
        f.write("Max difference: " + str(max_difference) + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        num = sys.argv[1]
    else:
        num = "7"
    # trace the logs for analysis
    trace_logs(log_num=num)
    # calculate the percent time each process takes on each CPU
    process_time_by_CPU(log_num=num)
    # check for difference greater than 0.1
    check_diffs(log_num="7", min_diff=0.1)
