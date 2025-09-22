import time

for i in range(10):
    print("Count: {}".format(i), end='\r', flush=True)
    time.sleep(0.5)