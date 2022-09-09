def model_data_process(timestamps, params, model):
    """
    Processes the data from the model and writes it to a file.
    :param timestamps: timestamps for the breakdown of time spent in the model
    :param params: parameters used for model creation and training
    :param model: model used for training
    :return: nothing
    """
    # create timestamps definitions
    timestamps_definitions = ['', 'imports', 'read_data', 'splitting_data', 'compiling_model', 'training_model',
                              'total_job']

    # add timestamps to file
    with open("Data/model_run_data.txt", "w") as fl:
        # total time
        fl.write(str(timestamps_definitions[-1]) + " =\n" + str(round(timestamps[-1] - timestamps[0], 5)) + "\n")
        # parameters used
        fl.write("params =\n" + str(params) + "\n")
        total_time_taken = 0
        # add time taken for the 5 main sub-jobs
        fl.write("breakdown =\n{")
        for i in range(1, len(timestamps)):
            time_taken = round(timestamps[i] - timestamps[i - 1], 5)
            total_time_taken += time_taken
            fl.write('"' + str(timestamps_definitions[i]) + '"' + ": " + str(time_taken) + ", ")
        fl.write("}\n")

    # save the model
    model.save("Data/model.h5")


def tracing_data_process(timeline):
    """
    Processes the data from the tracing and writes it to a file. Ignore idle and combines tasks like kworker/1 to kworker
    :timeline: timestamps creating a sequence of context switches
    :return: nothing
    """
    # make sure model has ended
    if not timeline:
        print("no data to process")
        return

    # data structures
    unique_pid_counts = {}
    cpu_timelines = {}  # timeline for each CPU
    task_times = {} # the amount of CPU time each task gets
    real_task_times = {} # the amount of real time (python timestamps) each task gets
    pid_times = {}
    cpu_usage = {}
    python_start_stop = {}
    all_start_stop = {}
    time_jumps = {} # capture if the timestamp jumps in value

    # name of python process
    PYTHON = "python3"

    # preprocess the timeline to split into a timeline for each CPU
    for index, data in enumerate(timeline):
        # get data from the primary timeline
        task_name, pid, cpu_num, flags, timestamp, msg, real_time, time_diff = data
        # decode name
        task_name = task_name.decode('utf-8')
        # add to correct cpu_timeline
        if cpu_num not in cpu_timelines:
            cpu_timelines[cpu_num] = []
        # add relevant data and real time to cpu_timeline
        cpu_timelines[cpu_num].append([timestamp, task_name, pid, real_time])
    # capture any time jumps that occur in the timeline
    for cpu_num, cpu_timeline in cpu_timelines.items():
        for index, data in enumerate(cpu_timeline):
            # get data from the cpu_timeline
            timestamp, task_name, pid, real_time = data
            # check if the timestamp is the same as the previous one
            if index > 0:
                prev_timestamp, prev_task_name, prev_pid, prev_real_time = cpu_timeline[index - 1]
                if timestamp - prev_timestamp > 5:
                    if cpu_num not in time_jumps:
                        time_jumps[cpu_num] = []
                    time_jumps[cpu_num].append([prev_timestamp, prev_task_name, prev_pid, prev_real_time])
                    time_jumps[cpu_num].append("-->")
                    time_jumps[cpu_num].append([timestamp, task_name, pid, real_time])
    # get the total time spent on each cpu
    cpu_time_spent = {}
    for cpu_num in range(len(cpu_timelines)):
        timestamp_difference = cpu_timelines[cpu_num][-1][0] - cpu_timelines[cpu_num][0][0]
        real_difference = cpu_timelines[cpu_num][-1][3] - cpu_timelines[cpu_num][0][3]
        cpu_time_spent[cpu_num] = (timestamp_difference, real_difference)
    # process the timeline for task times and cpu usage
    for cpu in cpu_timelines:
        cpu_timeline = cpu_timelines[cpu]
        for counter, data in enumerate(cpu_timeline):
            # get data
            ts, task, pid, real_time = data
            # add to unique PID counts
            if task not in unique_pid_counts:
                unique_pid_counts[task] = set()
            unique_pid_counts[task].add(pid)
            # make sure that counter isn't the first one
            if counter == 0:
                continue
            # add time to task
            if task not in task_times:
                task_times[task] = 0
            prev_ts = cpu_timeline[counter - 1][0]
            task_time_taken = ts - prev_ts
            task_times[task] += task_time_taken
            # add time to real_task_times
            if task not in real_task_times:
                real_task_times[task] = 0
            real_prev_ts = cpu_timeline[counter - 1][3]
            real_task_time_taken = cpu_timeline[counter][3] - real_prev_ts
            real_task_times[task] += real_task_time_taken
            # add time to pid
            if pid not in pid_times:
                pid_times[pid] = 0
            pid_times[pid] += task_time_taken
            # add to cpu counts
            if cpu not in cpu_usage:
                cpu_usage[cpu] = 0
            # add time to cpu if not idle
            if task != "<idle>":
                cpu_usage[cpu] += task_time_taken
            # add task to start/stop times
            if pid not in all_start_stop:
                all_start_stop[pid] = [prev_ts, ts]
            else:
                all_start_stop[pid][1] = ts
            # add python task to python start/stop times
            if task == PYTHON and pid not in python_start_stop:
                python_start_stop[pid] = [prev_ts, ts]
            elif task == PYTHON:
                python_start_stop[pid][1] = ts

    # see how much total idle
    total_idle = {}
    for pid in all_start_stop:
        total_exist = all_start_stop[pid][1] - all_start_stop[pid][0]
        total_idle[pid] = total_exist - pid_times[pid]
    # see how much time python idles for
    python_idle = {}
    for pid in python_start_stop:
        total_exist = python_start_stop[pid][1] - python_start_stop[pid][0]
        python_idle[pid] = total_exist - pid_times[pid]

    # write tasks counts and times to file
    with open("Data/timeline_data.txt", "w") as fl:
        # task times
        fl.write("task_times =\n{")
        for task in task_times:
            fl.write('"' + task + '"' + ": " + str(task_times[task]) + ", ")
        # task counts
        fl.write("}\nunique_pid__counts =\n{")
        for task_key in unique_pid_counts:
            fl.write('"' + task_key + '"' + ": " + str(len(unique_pid_counts[task_key])) + ", ")
        fl.write("}\n")
        # cpu usage
        fl.write("cpu_usage =\n{")
        for idx in range(len(cpu_usage)):
            fl.write('"' + str(idx) + '"' + ": " + str(cpu_usage[idx]) + ", ")
        fl.write("}\n")
        # python idle
        fl.write("python_pid_idle =\n{")
        for pid in python_idle:
            fl.write('"' + str(pid) + '"' + ": " + str(python_idle[pid]) + ", ")
        fl.write("}\n")
        # python lifespans
        fl.write("python_pid_start_stop =\n{")
        for pid in python_start_stop:
            fl.write('"' + str(pid) + '"' + ": " + str(python_start_stop[pid]) + ", ")
        fl.write("}\n")

    # save total aggregate data
    sum_tasks_existence = 0
    for pid in all_start_stop:
        sum_tasks_existence += all_start_stop[pid][1] - all_start_stop[pid][0]
    tasks_total_idle = 0
    for pid in total_idle:
        tasks_total_idle += total_idle[pid]
    # save aggregate python data
    python_total_lifespan = 0
    for pid in python_start_stop:
        python_total_lifespan += python_start_stop[pid][1] - python_start_stop[pid][0]
    python_total_idle = 0
    for pid in python_idle:
        python_total_idle += python_idle[pid]
    with open("Data/start_stop_data.txt", "w") as f:
        # total lifespan
        f.write("all_average_start_stop =\n")
        f.write(str(sum_tasks_existence / len(all_start_stop)))
        f.write("\nall_average_idle =\n")
        f.write(str(tasks_total_idle / len(total_idle)))
        # python lifespan
        f.write("\npython_average_start_stop_length =\n")
        f.write(str(python_total_lifespan / len(python_start_stop)))
        f.write("\npython_average_idle =\n")
        f.write(str(python_total_idle / len(python_idle)))

    # write the difference between CPU ts time and python ts time
    with open("Data/time_diffs.txt", "w") as f:
        for process in task_times:
            f.write(str(process) + ": " + str(task_times[process] - real_task_times[process]) + "\n")

    # write the time jumps to a file
    with open("Data/time_jumps.txt", "w") as f:
        f.write("CPU num: [system ts, task name, pid, python ts]\n")
        for cpu_num in time_jumps:
            f.write(str(cpu_num) + ": " + str(time_jumps[cpu_num]) + "\n")

    # feedback to user
    print("finished processing timeline data")
    # run visualizer
    from visualizer import visualize
    visualize(timeline, cpu_time_spent)
