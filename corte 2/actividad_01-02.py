#Rafael Alejandro Aguilar Mota
from queue import Queue
from threading import Thread, Semaphore
import time

s = Semaphore(1)#variable semaforo
q = Queue(10)

def producer(name):
    count = 1
    while True:
        q.join()
        q.put(count)
        print("--------------------------------------------------------")
        print(f"{name} está produciendo {count}")
        count+=1
        
def customer(name):
    count = 1
    while True:
        q.get()
        print("--------------------------------------------------------")
        print(f"El consumidor {name} está consumiendo {count}")
        count+=1
        q.task_done() 
        time.sleep(1)
        
def main():
    t1 = Thread(target=producer,args=("MOTYE",))
    t2 = Thread(target=customer,args=("PEPE",))
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()

