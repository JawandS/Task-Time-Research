import time

# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Driver Program
if __name__ == "__main__":
    start_time = time.time()
    n = 35
    fib(n)
    print("Time taken: " + str(time.time() - start_time))
