import time, sys

# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Driver Program
if __name__ == "__main__":
    start_time = time.time()
    args = sys.argv
    n = 35
    fib(n)
    if len(args) > 1:
        print(args[1], round(time.time() - start_time, 3))
    else:
        print(-1, round(time.time() - start_time, 3))
