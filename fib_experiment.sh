#!/bin/bash
for outer in {1...3}
do
  for inner in {1...10}
  do
    sudo python3 fib.py outer inner
  done
done
