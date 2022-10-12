# move all the timelines and time_diffs to a new folder
import os, shutil, math

def iter_dirs():
    # find all the directories in the current location
    dirs = sorted(name for name in os.listdir("") if os.path.isdir(os.path.join("", name)))
    # iterate through the files
    for dir_name in dirs:
        # create a new directory for the data
        os.mkdir("Jawand_Data_Archive/" + dir_name)
        if os.path.isfile(dir_name + "/Raw/timeline.txt"):
            shutil.move(dir_name + "/Raw/timeline.txt", "Jawand_Data_Archive/" + dir_name + "/timeline.txt")
        if os.path.isfile(dir_name + "/Raw/time_diffs.txt"):
            shutil.move(dir_name + "/Raw/time_diffs.txt", "Jawand_Data_Archive/" + dir_name + "/time_diffs.txt")

def trace_logs(log_letter):
    log = "raw_log_" + log_letter + ".txt"
    total_diff = 0 # total difference between timestamps
    num_diffs = 0 # number of differences
    with open(log, "r") as f:
        prev_ts = 0 # previous timestamp
        # read through the lines
        for counter, line in enumerate(f):
            if counter == 0 or line == "\n":
                continue # skip the first line or new line
            data = line.strip().split(" ")
            if len(data) != 2:
                continue # skip empty lines or new lines
            ts = int(data[1])
            if counter == 1: # continue if it's the first timestamp
                prev_ts = ts
                continue
            if (prev_ts > 0 and ts < 0) or (prev_ts < 0 and ts > 0): # if the sign changes ignore it
                continue
            # calculate the difference
            diff = ts - prev_ts
            # add the absolute value of the difference to the total
            total_diff += diff
            num_diffs += 1
            prev_ts = ts
    print("Average difference for log", log_letter, (total_diff / num_diffs) / 1e+6) # print average difference in seconds

if __name__ == "__main__":
    trace_logs(log_letter="B")
    # B=0.0019169486051582826, C=0.0019187149509847137, D=0.00682865379853148
