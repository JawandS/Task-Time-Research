#!/bin/bash
for counter in {1..500}
do
    sudo python3 model.py quiet >> Data/run_time.txt & sudo python3 context_switch_trace.py >> temp.txt
    sudo python3 model.py quiet >> Data/run_time.txt
    echo "Run $counter complete"
done