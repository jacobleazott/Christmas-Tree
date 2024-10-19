import multiprocessing
import time

def child_process():
    print("Child process starting...")
    time.sleep(5)  # Sleep for 5 seconds
    print("Child process finished sleeping.")

if __name__ == "__main__":
    p = multiprocessing.Process(target=child_process)
    p.start()
    
    print("Main thread sleeping...")
    time.sleep(2)  # Sleep for 2 seconds
    print("Main thread finished sleeping.")
    
    p.join()  # Wait for the child process to finish