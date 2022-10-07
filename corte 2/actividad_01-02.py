#Rafael Alejandro Aguilar Mota
import multiprocessing
import random
import time
class Producer(multiprocessing.Process):
    def __init__(self, queue, p_load, p_delay, p_done):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.p_done = p_done
        self.p_delay = p_delay
        self.p_load = p_load

    def run(self):
        for i in range(self.p_load):
            while self.queue.full():
                print('producer: La cola esta llena')
                time.sleep(2)
            item = random.randint(0, 999)
            self.queue.put(item)
            print('producer: Produjo el item {}'.format(item))
            time.sleep(self.p_delay)
            print('producer: el tamaño de la cola es {}'.format(self.queue.qsize()))
        self.p_done.value = 1
class Consumer(multiprocessing.Process):
    def __init__(self, queue, c_delay, c_done):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.c_done = c_done
        self.c_delay = c_delay

    def run(self):
        while True:
            if self.queue.empty():
                self.c_done.value = 1
                print('consumer: La cola esta vacia')
                time.sleep(2)
            else:
                self.c_done.value = 0
                time.sleep(self.c_delay)
                item = self.queue.get()
                print('consumer: Consumiendo el item {}.'.format(item))

if __name__ == '__main__':
    pf = multiprocessing.Value('d', 0)
    cf = multiprocessing.Value('d', 0)
    q = multiprocessing.Queue(3)
    p = Producer(q, 10, 2, pf)
    c = Consumer(q, 1, cf)
    p.start()
    c.start()
    # while True:
    #     if int(pf.value + cf.value) == 2:
    #         print('-------------------Proceso terminado----------------')
    #         p.terminate()
    #         c.terminate()
    #         break
    #     time.sleep(1)
