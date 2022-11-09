import time

timestamps = [time.time()]  # 0: start imports and overall file

import sys
args = sys.argv
if len(args) > 1:
    OUT_FLAG = False
else:
    OUT_FLAG = True

if not OUT_FLAG:
    import logging
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
    logging.getLogger('tensorflow').setLevel(logging.FATAL)


import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow.keras.optimizers as opt # optimizer
import time

# https://aditya-bhattacharya.net/2020/07/11/time-series-tips-and-tricks/2/
# uses the MIT license https://github.com/adib0073/TimeSeries-Using-TensorFlow/blob/main/LICENSE
# data uses public domain dedication https://www.kaggle.com/datasets/robervalt/sunspots
timestamps.append(time.time())  # 1: stop imports, start setup

# load and convert data to np.array
df = pd.read_csv('Archive/Data/data.csv', index_col=0)
time_index = np.array(df['Date'])
data = np.array(df['Monthly Mean Total Sunspot Number'])

# Static hyperparameters
SPLIT_RATIO = 0.8
WINDOW_SIZE = 60
SHUFFLE_BUFFER = 1000
EPOCHS = 200
# Changeable hyperparameters (to be tuned) - optimizer, batch size, number of layers, multi-worker training
BATCH_SIZE = 64
LAYER_COUNT = 3
optimizers_choices = {0: "SGD", 1: "Adam", 2: "adagrad", 3: "adadelta", 4: "adamax", 5: "nadam"}
params = {"Optimizer": optimizers_choices[0], "Batch Size": BATCH_SIZE, "Layers": LAYER_COUNT, "Multi-Worker": False, "epochs": EPOCHS}
# standard_params = {"Optimizer": "SGD", "Batch Size": 32, "Layers": 3, "Multi-Worker Training": False}

timestamps.append(time.time())  # 2: stop setup, start processing data

# Splitting the data into training and testing
split_index = int(SPLIT_RATIO * data.shape[0]) # index where data is split
train_data = data[:split_index]
train_time = time_index[:split_index]
test_data = data[split_index:]
test_time = time_index[split_index:]


def time_series_gen(data, window_size, batch_size, shuffle_buffer):
    ts_data = tf.data.Dataset.from_tensor_slices(data)
    ts_data = ts_data.window(window_size + 1, shift=1, drop_remainder=True)
    ts_data = ts_data.flat_map(lambda window: window.batch(window_size + 1))
    ts_data = ts_data.shuffle(shuffle_buffer).map(lambda window: (window[:-1], window[-1]))
    ts_data = ts_data.batch(batch_size).prefetch(1)
    return ts_data


train_dataset = time_series_gen(train_data, WINDOW_SIZE, BATCH_SIZE, SHUFFLE_BUFFER)
test_dataset = time_series_gen(test_data, WINDOW_SIZE, BATCH_SIZE, SHUFFLE_BUFFER)

timestamps.append(time.time())  # 3: stop processing data, start creating and compiling model

# build the layers
layers = [tf.keras.layers.Dense(20, input_shape=[WINDOW_SIZE], activation="relu")]
for i in range(params["Layers"] - 2):
    layers.append(tf.keras.layers.Dense(10, activation="relu"))
layers.append(tf.keras.layers.Dense(1))
# add layers to the model
model = tf.keras.models.Sequential(layers)
# compile the model
model.compile(loss="mse", optimizer=opt.SGD(learning_rate=1e-7, momentum=0.9))
# optimizer=opt.Adam(learning_rate=1e-7)
# optimizer=opt.SGD(learning_rate=1e-7, momentum=0.9)

timestamps.append(time.time())  # 4: stop creating and compiling model, start training

# train the model
if OUT_FLAG:
    model.fit(train_dataset, epochs=EPOCHS, verbose=1)
else:
    model.fit(train_dataset, epochs=EPOCHS, validation_data=test_dataset, verbose=0)

timestamps.append(time.time())  # 5: stop training, end program

# indicate model end
if OUT_FLAG:
    print("model ended, time taken: " + str(timestamps[-1] - timestamps[0]) + " seconds")
else:
    print(str(timestamps[-1] - timestamps[0])) # print time taken

# kill the tracing
import os, signal

name = "bpftrace"
for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
    fields = line.split()
    # extracting Process ID from the output
    pid = fields[0]
    # terminating process
    if OUT_FLAG:
        print("killing " + name + " with pid " + pid)
    # kill process
    os.kill(int(pid), signal.SIGINT)  # SIGINT is the signal for "Interrupt"

# end the program for now
exit()

# send signal to end context_switch_trace.py and fib.java
import os, signal
names = ["context_switch_trace.py", "fib"]
pids = []
for idx, name in enumerate(names):
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        fields = line.split()
        # extracting Process ID from the output
        pid = fields[0]
        # terminating process
        print("killing " + name + " with pid " + pid)
        # capture data
        pids.append((name, pid))
        # kill process
        if idx == 0:
            os.kill(int(pid), signal.SIGINT) # SIGINT is the signal for "Interrupt"
        else:
            os.kill(int(pid), signal.SIGTERM) # SIGTERM is the signal for "Terminate"

# process the data
from Archive.Old_Programs.data_process import model_data_process
model_data_process(timestamps, params, model)
# write PIDs to a file
with open("Data/pids.txt", "w") as f:
    for name, pid in pids:
        f.write(name + " " + pid + "\n")
# print end of job
print("finished processing model data")
