#!/bin/bash
for counter in {1...3}
do
  python3 fib.py 1 & python3 fib.py 2 & python3 fib.py 3 & python3 fib.py 4 & python3 fib.py 5
done
