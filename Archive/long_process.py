# find the first and last timestamp for each CPU
def trace_log():
    data = {} # capture first/last timestamp for each CPU
    with open("long_run.txt", "r") as f:
        for idx, line in enumerate(f):
            if line == "\n": # ignore new lines
                continue
            # get the values
            vals = line.split()
            cpu_num, ts = vals[0], vals[1]
            cpu_num, ts = int(cpu_num), int(ts)
            # add the values to the dictionary
            if cpu_num not in data:
                data[cpu_num] = [ts, ts]
            else:
                data[cpu_num][1] = ts
    for cpu_num in data:
        print("CPU", cpu_num, ":", (data[cpu_num][1] - data[cpu_num][0]) / 1e+9, " seconds")

if __name__ == "main":
    trace_log()
