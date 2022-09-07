# move all the timelines and time_diffs to a new folder
import os, shutil
# find all the directories in the current location
dirs = sorted(name for name in os.listdir(".") if os.path.isdir(os.path.join("", name)))
# iterate through the files
for dir_name in dirs:
    # create a new directory for the data
    os.mkdir("Jawand_Data_Archive/" + dir_name)
    if os.path.isfile(dir_name + "/Raw/timeline.txt"):
        shutil.move(dir_name + "/Raw/timeline.txt", "Jawand_Data_Archive/" + dir_name + "/timeline.txt")
    if os.path.isfile(dir_name + "/Raw/time_diffs.txt"):
        shutil.move(dir_name + "/Raw/time_diffs.txt", "Jawand_Data_Archive/" + dir_name + "/time_diffs.txt")
