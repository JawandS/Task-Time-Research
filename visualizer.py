import matplotlib.pyplot as plt

def visualize(timeline, cpu_time):
    # note to add to directory
    note = ""
    # directory start index
    dir_idx = 27

    # data to plot
    with open("Data/timeline_data.txt", "r") as f:
        f.readline()
        task_times = eval(f.readline())
        f.readline()
        task_counts = eval(f.readline())
        f.readline()
        cpu_usage = eval(f.readline())
        f.readline()
        # python_idle = eval(f.readline())
        # f.readline()
        # python_lifespans = eval(f.readline())
    with open("Data/model_run_data.txt", "r") as f:
        f.readline()
        total_time = eval(f.readline())
        f.readline()
        f.readline() # params = eval(f.readline())
        f.readline()
        breakdown = eval(f.readline())

    # create dictionary without idle
    no_idle_task_times = {}
    no_kworker_task_times = {}
    merged_Tasks = {}
    for task in task_times:
        if task != "<idle>":
            no_idle_task_times[task] = task_times[task]
        if "kworker" not in task:
            no_kworker_task_times[task] = task_times[task]
        if "/" in task:
            key = task.split("/")[0]
            if key in merged_Tasks:
                merged_Tasks[key] += task_times[task]
            else:
                merged_Tasks[key] = task_times[task]
        else:
            if task in merged_Tasks:
                merged_Tasks[task] += task_times[task]
            else:
                merged_Tasks[task] = task_times[task]
    # data structures
    dicts = [task_times, task_counts, cpu_usage, no_idle_task_times, no_kworker_task_times, merged_Tasks]
    titles = ["Task_times", "Task_counts", "CPU_usage", "TT_no_idle", "TT_no_kworker", "TT_merged"]

    # find correct directory
    import os
    while os.path.isdir('Run_Data/Run_' + str(dir_idx)) or os.path.isdir('Run_Data/Run_' + str(dir_idx) + note):
        dir_idx += 1
    dir_idx = str(dir_idx)
    dir_name = 'Run_Data/Run_' + dir_idx + note
    os.mkdir(dir_name)

    # add figures
    for i, data in enumerate(dicts):
        # sort data from greatest to least and put back into dictionary
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        # data
        remaining = 0
        total = sum(data.values())
        labels = []
        values = []
        for sorted_label, value in sorted_data:
            percent = value / total
            if percent > .03 or i == 2: # don't add CPU to other
                labels.append(sorted_label)
                values.append(percent)
            else:
                remaining += percent
        if remaining > 0:
            labels.append("other")
            values.append(remaining)

        # plot horizontal bar chart
        plt.barh(labels, values)
        # label
        plt.xlabel("Percentage")
        plt.ylabel("Tasks")
        # title
        plt.title(titles[i].replace("_", " "))
        # save
        plt.savefig(dir_name + "/" + titles[i] + ".png")
        # close figure
        plt.close()

    # create table for breakdown
    table_breakdown = [["Total", str(round(total_time, 3)), "100"]]
    for key in breakdown:
        percent = breakdown[key] / total_time
        table_breakdown.append([key, str(round(breakdown[key], 3)), str(round(percent, 2) * 100)])
    plt.table(cellText=table_breakdown, colLabels=["Task", "Time(s)", "Percent(%)"], loc="center")
    plt.axis('off')
    plt.savefig(dir_name + "/Breakdown.png", bbox_inches=0)
    plt.close()

    # copy data files to the appropriate directory
    import shutil
    os.mkdir(dir_name + "/Raw")
    try:
        shutil.move("Data/model_run_data.txt", dir_name + "/Raw/model_run_data.txt")
        shutil.move("Data/timeline_data.txt", dir_name + "/Raw/timeline_data.txt")
        shutil.move("Data/start_stop_data.txt", dir_name + "/Raw/start_stop_data.txt")
        shutil.move("Data/model.h5", dir_name + "/Raw/model.h5")
        shutil.move("Data/time_diffs.txt", dir_name + "/Raw/time_diffs.txt")
        shutil.move("Data/pids.txt", dir_name + "/Raw/pids.txt")
        shutil.move("Data/timeline.txt", dir_name + "/Raw/timeline.txt")
        shutil.move("Data/time_jumps.txt", dir_name + "/Raw/time_jumps.txt")
    except FileNotFoundError:
        print("Note: some file not found")
    # write the raw timelines into a file
    with open(dir_name + "/Raw/partial_raw_timeline.txt", "w") as fl:
        fl.write(str(timeline[:2000]))
    # write the cpu time into a file
    with open(dir_name + "/Raw/cpu_time.txt", "w") as fl:
        fl.write(str(cpu_time))
    # update git
    import subprocess
    subprocess.call(["sudo", "git", "add", "."])
    subprocess.call(["sudo", "git", "commit", "-m", "Add and process Run " + dir_idx])
    subprocess.call(["sudo", "git", "push"])
