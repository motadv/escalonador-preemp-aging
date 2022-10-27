class Process:
    def __init__(self, enterTime, name, priority, burstList, ioList) -> None:
        self.enterTime = enterTime
        self.name = name
        self.priority = priority
        self.burstList = burstList
        self.ioList = ioList

    def debug_print(self):
        print(f"{self.enterTime} {self.name} {self.priority} {self.burstList} {self.ioList}")


def readProcess(text)->Process:
    info = text.split()
    enterTime = int(info[0])
    name = info[1]
    priority = int(info[2])
    burstList = [int(x) for x in info[3::2]]
    ioList = [int(x) for x in info[4::2]]

    return Process(enterTime, name, priority, burstList, ioList)


timeLine = []
with open("processos.in","r") as inputFile:
    for line in inputFile:
        timeLine.append(readProcess(line))

timeLine.sort(key = lambda x: x.enterTime)

for x in timeLine:
    x.debug_print()
time = 0
quantum = 0
readyQueue = []
waitQueue = []
exec = None

def enterReady(p: Process):
    readyQueue.append(p)
    interruption()

def interruption():
    if exec != None:
        readyQueue.append(exec)
        exec = None

def waitIOs():
    for p in waitQueue:
        p.ioList[0] -= 1
        if p.ioList[0] == 0:
            del p.ioList[0]
            enterReady(p)
            waitQueue.remove(p)

def execute():  
    if exec == None:
        #enter new process in exec
        readyQueue.sort(key=lambda x: x.priority)
        exec = readyQueue.pop(0)
        quantum = 0
    
    



        
#Processing Loop base:
#While there are processes in the system
while(len(timeLine) != 0 and len(readyQueue) != 0 and len(waitQueue) != 0 and exec == None):
    
    #Entra processos novos na lista de pronto
    for item in timeLine:
        if item.enterTime == time:
            enterReady(item)
            timeLine.remove(item)
        else:
            break

    #Resolve o IO da fila de espera
    waitIOs()
    execute()
    time += 1
