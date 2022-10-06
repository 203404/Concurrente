import threading
import time

mutex=threading.Lock()
class Person:
    def __init__(self,stick, ate,id):
        self.stick=stick
        self.ate=ate
        self.id=id
    def getAll(self):
        return f"sticks: {self.stick}, Person: {self.id}, ate: {self.ate}"

def eating(person):
    mutex.acquire()
    person.stick=2
    print(f'Person{person.id} eating')
    print(person.getAll())
    time.sleep(3)
    person.stick=1
    person.ate=True
    print(f'Person{person.id} is done')
    print(f'Final Data:{person.getAll()}')
    mutex.release()
    
def table(people):
    for person in people:
        personEating=threading.Thread(target=eating, args=[person])
        print(f'Person{person.id} waiting')
        personEating.start()

def done(people):
    time.sleep(28)
    for singleP in people:
        print(singleP.getAll())

def startCounter(people):
    hiloToPrint=threading.Thread(target=done,args=[people])
    hiloToPrint.start()

def main():
    people=[]
    for id in range (0,8):
        person = Person(1,False,id+1)
        people.append(person)
    table(people)
    startCounter(people);
    
if __name__ == "__main__":
    main()
