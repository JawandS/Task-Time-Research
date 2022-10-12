notes = """
Run 1 and 2 - 16 CPU
Run 3+ - 32 CPUs
"""

import os

# open file to write data to
analysis_file = open("analysis_data.txt", "a")
# find all directories in Run_Data
dirs = sorted(name for name in os.listdir("") if os.path.isdir(os.path.join("", name)))
# go through each directory
for dir_name in dirs:
    # read in run data
    with open(dir_name + "/raw/timeline_data.txt", "r") as f:
        f.readline()
        task_times = eval(f.readline())
        f.readline()
        task_counts = eval(f.readline())
        f.readline()
        cpu_usage = eval(f.readline())
        f.readline()
        python_lifespans = eval(f.readline())
    with open(dir_name + "/raw/model_run_data.txt", "r") as f:
        f.readline()
        total_time = eval(f.readline())
        f.readline()
        params = eval(f.readline())
        f.readline()
        breakdown = eval(f.readline())

    # calculate additional data from run data
    data = {}
    names = os.listdir(dir_name)
    # add total time
    data["total_time"] = total_time
    # find python lifespan and lifespan per total time
    for name in names:
        if "lifespan" in name:
            data["lifespan"] = float(name.split(" ")[0])
            data["lifespan_avg"] = data["lifespan"] / total_time
            break
    # unique python pid
    data["python_pid"] = len(python_lifespans)
    # total task time
    data["total_task_time"] = round(sum(task_times.values()), 3)

    # write to the storage file
    analysis_file.write(dir_name + "\n" + str(data) + "\n")
