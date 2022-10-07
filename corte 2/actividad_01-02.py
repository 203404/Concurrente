#Rafael Alejandro Aguilar Mota
import queue
import threading
import time
import random

q = queue.Queue(maxsize=0)
class Producer():
    def __init__(self, q, p_load):
        self.q = q
        self.p_load = p_load       

    def run(self, event):
        t_name = threading.current_thread().name
        for i in range(self.p_load):
            while self.q.full():
                print('producer: cola llena')
                time.sleep(2)
            item = random.randint(0,999)
            print(f"{t_name} generated item {item}")           
            self.q.put(item)
            time.sleep(0.5)
        print(f'*** producer {t_name} finished work')
        
        event.set()

class Consumer():
    def __init__(self, q):        
        self.q = q

    def run(self, event):
        t_name = threading.current_thread().name
        while True:
            if not self.q.empty():
                try:
                    item = self.q.get()
                    print(f"{t_name} consumed item: {item}".format(item))                   
                except queue.Empty:
                    if event.is_set():
                        break
            elif event.is_set():
                break
        print(f'*** consumer {t_name} finished work')
        
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