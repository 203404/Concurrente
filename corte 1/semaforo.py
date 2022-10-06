from telnetlib import SE
from threading import Thread, Semaphore
semaforo = Semaphore(1)#variable semaforo

def crito(id):
    global x;
    x +=id
    print("Hilo = " +str(id)+" => " + str(x))
    x=1

class Hilo(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id=id
    
    def run(self):
        semaforo.acquire()#inicializacion semaforo
        crito(self.id)
        semaforo.release()#librera un semaforo e incrementa la variable semaforo
Threads_semaphore = [Hilo(1), Hilo(2),Hilo(3)]
x=1;
for t in Threads_semaphore:
    t.start()
