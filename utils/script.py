import time

try:
    while True:
        print("Hello, world!")
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye!")
    
