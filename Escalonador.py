from glob import glob


class Process:
    
    def __init__(self, enterTime, name, priority, burstList, ioList) -> None:
        self.enterTime = enterTime
        self.name = name
        self.priority = priority
        self.burstList = burstList
        self.ioList = ioList

    def readProcess(text):
        info = text.split()
        enterTime = int(info[0])
        name = info[1]
        priority = int(info[2])
        burstList = [int(x) for x in info[3::2]]
        ioList = [int(x) for x in info[4::2]]

        return Process(enterTime, name, priority, burstList, ioList)

def enterReady(p: Process):    
    readyQueue.append(p)
    interruption()

def interruption():
    global exec
    
    if exec != None:
        readyQueue.append(exec)
        exec = None
        print('> Interrupt <')

def enterWait(p: Process):
    waitQueue.append(p)
    
def waitIOs():
    global waitQueue
    
    for p in waitQueue:
        p.ioList[0] -= 1
        if p.ioList[0] == 0:
            p.ioList.remove(p.ioList[0])
            enterReady(p)
            waitQueue.remove(p)

def aging():
    global readyQueue
    
    #decrease pririty
    for p in readyQueue:
        if p.priority > 0:
            p.priority -= 1
            
    interruption()

def getNextProcess()-> Process:
    global readyQueue
    
    readyQueue.sort(key=lambda x: (x.priority, x.enterTime))
    if readyQueue: return readyQueue.pop(0)
    else: return None

def enterNewProcesses():
    global timeLine
    
    for p in timeLine:
        if p.enterTime == time:
            enterReady(p)
            timeLine.remove(p)

def execute():  
    global exec, quantum, readyQueue
    
    if exec == None:
        #enter new process in exec
        exec = getNextProcess()
        quantum = 0
    
    #execute current
    if exec != None:
        exec.burstList[0] -= 1
        quantum += 1
        
        if exec.burstList[0] == 0:
            del exec.burstList[0]
            if exec.ioList:
                enterWait(exec)
                exec = None
            else:
                processEndedCallback(exec)
                exec = getNextProcess()
                
                quantum = 0
                
        if quantum > 5:
            quantum = 0
            aging()
            exec = getNextProcess()
        
def processEndedCallback(p: Process):
    print(f'O processo: {p.name} terminou!')

def printReport():
    print(f'Estado Atual:\n')
    print(f'Tempo: {time} | Aging: {quantum}')
    print(f'Executando: ', end='')
    if exec != None: print(f'{exec.name} | Prioridade: {exec.priority} | Tempo restante: {exec.burstList[0]}', end='')
    print(f'\nFila de Pronto:')
    for p in readyQueue:
        print(f'   {p.name} | Prioridade: {p.priority} | Tempo restante: {p.burstList[0]}')
    print(f'Fila de Espera:')
    for p in waitQueue:
        print(f'   {p.name} | Prioridade: {p.priority} | Tempo restante: {p.ioList[0]}')
    
    
    print("---------------------------------------------")
    

time = 0
quantum = 0
readyQueue = []
waitQueue = []
exec = None

timeLine = []
with open("processos.in","r") as inputFile:
    for line in inputFile:
        timeLine.append(Process.readProcess(line))

timeLine.sort(key = lambda x: x.enterTime)

enterNewProcesses()    
    
#Processing Loop base:
#While there are processes in the system
print("Escalonador com Prioridade, Aging e Preemp:\n")

while(exec or readyQueue or waitQueue):
    
    enterNewProcesses()
    waitIOs()
    execute()    
    
    printReport()
    
    time += 1
    
print('\nFim da Sim.\n')