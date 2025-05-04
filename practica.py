from dataclasses import dataclass, field
from typing import List, Dict, Union
import threading
import time
from random import randint



@dataclass
class Message:
    InitialMessage: str
    PriorityValue: int = 0
    MessageLen: int = 0
    RealMessage: str = ""

    def __post_init__(self):
        self.RealMessage = self.InitialMessage
        self.InitialMessage = self.InitialMessage.lower()
        self.ConvertMessage()
        self.CalcPriorityValue()

    def CalcPriorityValue(self):
        KeywordsValue:Dict = {
            "emergencia": 10, 
            "urgente": 8,
            "fallo crítico": 9,
            "problema": 5,
            "consulta": 2,
            "duda": 1
        }
        for Word in self.InitialMessage:
            if Word in KeywordsValue:
                self.PriorityValue += KeywordsValue[Word]
        return self.PriorityValue


    def ConvertMessage(self) -> None:
        self.InitialMessage = self.InitialMessage.split(" ")
    


    def __lt__(self, other: 'Message') -> bool:
        return self.PriorityValue < other.PriorityValue

    def __repr__(self):
        return str(self.PriorityValue)

@dataclass
class Agent:

    ExperienceLevel: int
    AssignedMessage: Message
    AgentID: int = field(default_factory=lambda: randint(1000, 9999))
    State: bool = True


    def __repr__(self):

        return f"El ID del agente es: {self.AgentID}, su experiencia es {self.ExperienceLevel} & su estado es {self.State}"

    def CalcMessageLen(self):
        if self.ExperienceLevel == 0:
            TimeReduction = 1
        elif self.ExperienceLevel == 1:
            TimeReduction = 0.75
        elif self.ExperienceLevel == 2:
            TimeReduction = 0.5
        
        return (len(self.AssignedMessage.RealMessage) / 10 + (self.AssignedMessage.PriorityValue / 2 )) * TimeReduction

    def __lt__(self, other:'Agent'):
        return self.ExperienceLevel < other.ExperienceLevel
    


@dataclass
class PriorityQueue:

    _index: int = 0
    _queue: List[Union[Message, Agent]] = field(default_factory=list)

    def Push(self, item: Message) -> None:
        self._queue.append(item)
        self._index += 1
        self._queue.sort(reverse=True)

    def Pop(self) -> Message:
        if self._queue:
            return self._queue.pop(0)
        else:
            return None
        
    def First(self) -> Message:
        if self._queue:
            return self._queue[0]
        return None
    
    def __repr__(self):
        return str(self._queue)
    
    def __iter__(self):
        return iter(self._queue)
    
Agents = PriorityQueue()


def ReadData(PathToTxt):
    messages = PriorityQueue()
    try:
        with open(PathToTxt, 'r', encoding='utf-8') as file:
            for line in file:
                content = line.strip()
                if content:
                    messages.Push(Message(InitialMessage=content))
    except FileNotFoundError:
        print(f"Error: The file at {PathToTxt} was not found.")
    return messages



ListaMensajes = ReadData("src/Practicas/Practica2Data.txt")


def HireAgents(NumberOfAgents: int) -> None:
    for _ in range(NumberOfAgents):
        Agents.Push(Agent(randint(0,2), ""))

def AssignMessages(Worker: Agent, NewMessage:Message):
    Worker.AssignedMessage = NewMessage
    Worker.State = False
    print(f"El trabajador {Worker.AgentID} esta trabajando tiempo =  {Worker.CalcMessageLen()}")
    time.sleep(Worker.CalcMessageLen())
    Worker.State = True
    print(f"El trabajador {Worker.AgentID} finalizo su trabajo")


HandlerFlagg = False

def CallCenter(MessagesQueue: PriorityQueue):
    
    while MessagesQueue.First() is not None:
        for Worker in Agents:
            if Worker.State:  
                threading.Thread(target=AssignMessages, args=(Worker, MessagesQueue.Pop())).start()
                          

HireAgents(5)
CallCenter(ListaMensajes)

print("Main Thread ")