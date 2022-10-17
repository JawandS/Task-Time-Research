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

def check_diffs(file_name, min_diff):
    data = split_by_CPU(file_name)
    max_difference = 0
    for cpu_num in range(len(data)):
        print(f"CPU {cpu_num} total difference: {(data[cpu_num][-1][2] - data[cpu_num][0][2]) / 1e+9}")
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
                print("Difference greater than 0.1: " + str(diff))
                print(str(prev_data))
                print(str(vals))
                print("---")
            # update the max difference
            if diff > max_difference:
                max_difference = diff
            # update the prev timestamp
            prev_ts = ts
            prev_data = [pname, pid, ts]
    print("Max difference: " + str(max_difference))

if __name__ == "__main__":
    # check for difference greater than 0.1
    check_diffs("log_6.txt", 0.1)
