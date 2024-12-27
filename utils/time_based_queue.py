import time
from threading import Thread, Lock

'''
- "with self.lock": only one thread can access the queue at a time.
'''

class TimeBasedQueue:
    def __init__(self, expiry_time):
        """
        Initialize the queue with an expiry time for elements.
        :param expiry_time: Time in seconds for elements to expire.
        """
        self.queue = []
        self.expiry_time = expiry_time
        self.lock = Lock()
        self.running = True

        # Start a thread to clean up expired elements
        self.cleaner_thread = Thread(target=self._clean_expired_elements)
        self.cleaner_thread.daemon = True
        self.cleaner_thread.start()

    def add(self, item):
        """
        Add an item to the queue with the current timestamp.
        :param item: Item to add to the queue.
        """
        with self.lock:
            items = [queue_item for queue_item in self.queue if queue_item[0] == item]
            # print(f"Items to delete: {items}")
            if not items:
                self.queue.append((item, time.time()))
            else: 
                # update the timestamp of the item
                self.queue.remove(items[0])
                # print(f"Queue after deleting old item: {self.queue}")
                self.queue.append((item, time.time()))
                # print(f"Queue after appending new item: {self.queue}")
        # print(f"Added: {item}")

    def get(self):
        """
        Get the first item in the queue, if it exists and hasn't expired.
        """
        with self.lock:
            if self.queue:
                item, timestamp = self.queue[0]
                if time.time() - timestamp < self.expiry_time:
                    return item
                else:
                    # Remove expired item
                    self.queue.pop(0)
        return None

    def get_at(self, idx):
        with self.lock:
            if self.queue and idx < len(self.queue):
                item, timestamp = self.queue[idx]
                if time.time() - timestamp < self.expiry_time:
                    return item
                else:
                    # Remove expired item
                    self.queue.pop(idx)
                    return self.get_at(idx)
            else:
                raise IndexError("Index out of range")
            
    def get_all(self):
        with self.lock:
            return [item for item, timestamp in self.queue if time.time() - timestamp < self.expiry_time]

    def _clean_expired_elements(self):
        """
        Periodically remove expired elements from the queue.
        """
        while self.running:
            with self.lock:
                now = time.time()
                # Remove all elements that have expired
                self.queue = [(item, ts) for item, ts in self.queue if now - ts < self.expiry_time]
            time.sleep(1)  # Check every 1 second

    def stop(self):
        """
        Stop the cleaner thread and clean up resources.
        """
        self.running = False
        self.cleaner_thread.join()

    def __len__(self):
        """
        Get the number of active (non-expired) elements in the queue.
        """
        with self.lock:
            return len(self.queue)

# Example usage
if (__name__ == "__main__"):
    queue = TimeBasedQueue(expiry_time=5)  # Elements expire after 5 seconds

    queue.add("item1")
    queue.add("item2")
    time.sleep(6)  # Wait for elements to expire

    print("Queue length:", len(queue))  # Should be 0
    queue.stop()
