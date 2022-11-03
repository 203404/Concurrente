import threading
import time
import queue
import math
from random import choice, randint

capacidadRestaurante = 5
clientesRestaurante = 10
meserosRestaurante = math.ceil(capacidadRestaurante * 0.1) if capacidadRestaurante <= 5 else round(capacidadRestaurante * 0.1)
cocinerosRestaurante = meserosRestaurante 
reservacionMaxima = round(capacidadRestaurante * 0.2)


class Monitor(object):
    def __init__(self, espacio):
        self.espacio = espacio
        self.mutex = threading.Lock()
        self.recepcion = threading.Condition()
        self.clientes = threading.Condition()
        self.mesero = threading.Condition()
        self.cocinero = threading.Condition()
        self.reservaciones = queue.Queue(reservacionMaxima)
        self.num_clientes = queue.Queue(self.espacio)
        self.ordenes = queue.Queue()
        self.ordenes_plato = queue.Queue()
        self.comida = queue.Queue()

    def reservar(self, comensal):
        self.recepcion.acquire()
        if self.reservaciones.full():
            self.recepcion.wait()
        else:
            print(f"Comensal {comensal.id} hizo una reservación")
            self.reservaciones.put(comensal)
            time.sleep(1)
        self.mutex.acquire()
        self.entrar(comensal)
        self.reservaciones.get()
        self.recepcion.notify()
        self.recepcion.release()

    def cola(self, comensal):
        self.recepcion.acquire()
        print(f"Comensal {comensal.id} se formó en la cola")
        time.sleep(1)
        self.mutex.acquire()
        self.entrar(comensal)
        self.recepcion.notify()
        self.recepcion.release()

    def entrar(self, comensal):
        self.clientes.acquire()
        if self.num_clientes.full():
            print(f"Comensal {comensal.id} esperando a que haya lugar")
            self.clientes.wait()
        else:
            print(f"Comensal {comensal.id} entra al restaurante")
            self.num_clientes.put(comensal)
            print(
                f"Comensal {comensal.id} se prepara para ordenar")
            self.mesero.acquire()
            self.mesero.notify()
            self.mesero.release()
            self.mutex.release()
            self.clientes.release()

    def comer(self):
        if not self.comida.empty():
            comensal = self.comida.get()
            comensal_id = list(comensal.keys())[0]
            comensal_plato = list(comensal.values())[0]
            print(f"Comensal {comensal_id} está comiendo {comensal_plato}")
            time.sleep(randint(1, 5))
            print(f"Comensal {comensal_id} terminó de comer")
            print(f"Comensal {comensal_id} ha salido")

    def crear_orden(self, mesero):
        while True:
            self.mesero.acquire()
            if self.num_clientes.empty():
                self.mesero.wait()
                print(f"Mesero {mesero} esta descansando")
            else:
                comensal = self.num_clientes.get()
                if comensal.orden == False:
                    plato = Menu()
                    print(f"Mesero {mesero} tomo la orden del cliente {comensal.id} que comerá {plato.menuAlimentos}")
                    time.sleep(1)
                    self.ordenes.put({comensal.id: plato.menuAlimentos})
                    self.cocinero.acquire()
                    self.cocinero.notify()
                    self.cocinero.release()
                    comensal.orden = True
                    self.mesero.release()
                else:
                    self.mesero.release()

    def cocinar(self, id):
        while True:
            self.cocinero.acquire()
            if self.ordenes.empty():
                self.cocinero.wait()
                print(f"Cocinero {id} esta descansando")
            else:
                comensal = self.ordenes.get()
                comensal_id = list(comensal.keys())[0]
                comensal_plato = list(comensal.values())[0]
                print(f"Cocinero {id} está cocinando la orden del comensal {comensal_id}: {comensal_plato}")
                time.sleep(1)
                self.comida.put(comensal)
                self.cocinero.release()


class Menu():
    alimentos = ["Chilaquiles", "Quesadilla", "Torta",
             "Guajolota", "Burrito", "Tacos de canasta"]

    def __init__(self):
        self.menuAlimentos = choice(self.alimentos)


class Comensal(threading.Thread):
    def __init__(self, id, monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.orden = False
        self.restaurant = monitor

    def run(self):
        reserva = randint(0, 1)
        if reserva == 1:
            self.restaurant.reservar(self)
        if reserva == 0:
            self.restaurant.cola(self)
        self.restaurant.comer()


class Mesero(threading.Thread):
    def __init__(self, id, monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.restaurant = monitor

    def run(self):
        self.restaurant.crear_orden(self.id)


class Cocinero(threading.Thread):
    def __init__(self, id, monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.restaurant = monitor

    def run(self):
        self.restaurant.cocinar(self.id)


def main():
    restaurant = Monitor(capacidadRestaurante)
    clientes = []
    meseros = []
    cocineros = []

    for x in range(clientesRestaurante):
        clientes.append(Comensal(x+1, restaurant))
    for comensal in clientes:
        comensal.start()

    for x in range(meserosRestaurante):
        meseros.append(Mesero(x+1, restaurant))
    for mesero in meseros:
        mesero.start()

    for x in range(cocinerosRestaurante):
        cocineros.append(Cocinero(x+1, restaurant))
    for cocinero in cocineros:
        cocinero.start()


if __name__ == "__main__":
    main()
