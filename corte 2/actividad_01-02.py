#Rafael Alejandro Aguilar Mota
import queue
import threading
import sys
import time
import random

q = queue.Queue(maxsize=0)

class Producer():
    def __init__(self, q, p_load):
        self.q = q
        self.p_load = p_load
        sys.stdout.flush()

    def run(self, event):
        t_name = threading.current_thread().name
        for i in range(self.p_load):
            while self.q.full():
                print('producer: cola llena')
                time.sleep(2)
            item = random.randint(0,999)
            print(f"{t_name} generated item {item}")
            sys.stdout.flush()
            self.q.put(item)
            time.sleep(0.5)
        print(f'*** producer {t_name} finished work')
        sys.stdout.flush()
        event.set()

class Consumer():
    def __init__(self, q):
        sys.stdout.flush()
        self.q = q

    def run(self, event):
        t_name = threading.current_thread().name
        while True:
            if not self.q.empty():
                try:
                    item = self.q.get()
                    print(f"{t_name} consumed item : {item}".format(item))
                    sys.stdout.flush()
                except queue.Empty:
                    if event.is_set():
                        break
            elif event.is_set():
                break
        print(f'*** consumer {t_name} finished work')
        sys.stdout.flush()

producer = Producer(q, 10)
consumer = Consumer(q)
e = threading.Event()

def main():
    threads = []
    threads.append(threading.Thread(target=producer.run, args=(e,), name="thread1"))
    threads.append(threading.Thread(target=consumer.run, args=(e,), name="thread2"))
    for thread in threads:
        thread.start()

if __name__ == "__main__":
    main()




