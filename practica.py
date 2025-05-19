from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional
import threading
import time
from random import randint, choice
from collections import defaultdict

@dataclass
class Message:
    message: str
    PriorityValue: int = 0
    MessageLen: int = 0

    def __post_init__(self):
        self.CalcPriorityValue()

    def CalcPriorityValue(self):
        original_text = self.message.lower()
        words = original_text.split()

        KeywordsValue: Dict[str, int] = {
            "emergencia": 10,
            "urgente": 8,
            "fallo": 9,
            "crítico": 9,
            "problema": 5,
            "consulta": 2,
            "duda": 1
        }
        for word in words:
            if word in KeywordsValue:
                self.PriorityValue += KeywordsValue[word]
        self.MessageLen = len(words)
        return

    def __lt__(self, other: 'Message') -> bool:
        return self.PriorityValue < other.PriorityValue

    def __repr__(self):
        return f"[Prioridad: {self.PriorityValue} | Mensaje: {self.message}]"

@dataclass
class Agent:
    ExperienceLevel: str 
    AssignedMessage: Optional[Message] = None
    AgentID: int = field(default_factory=lambda: randint(1000, 9999))
    State: bool = True

    def __repr__(self):
        return f"ID: {self.AgentID} | Experiencia: {self.ExperienceLevel} | Estado: {'Libre' if self.State else 'Ocupado'}"

    def AtentionTime(self):
        TimeReduction = {
            'básico': 1,
            'intermedio': 0.75,
            'experto': 0.5
        }.get(self.ExperienceLevel, 1)

        if not self.AssignedMessage:
            return 0
        return (self.AssignedMessage.MessageLen / 10 + (self.AssignedMessage.PriorityValue / 2)) * TimeReduction

    def __lt__(self, other: 'Agent'):
        levels = {'básico': 0, 'intermedio': 1, 'experto': 2}
        return levels[self.ExperienceLevel] < levels[other.ExperienceLevel]

@dataclass
class PriorityQueue:
    queue: List[Union[Message, Agent]] = field(default_factory=list)

    def enqueue(self, item: Union[Message, Agent]) -> None:
        self.queue.append(item)
        self.queue.sort(reverse=True)

    def dequeue(self) -> Union[Message, Agent, None]:
        if self.queue:
            return self.queue.pop(0)
        return 

    def first(self) -> Union[Message, Agent, None]:
        if self.queue:
            return self.queue[0]
        return 

    def __repr__(self):
        return str(self.queue)

    def __iter__(self):
        return iter(self.queue)


def ReadData(file_path: str) -> PriorityQueue:
    messages = PriorityQueue()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            content = line.strip()
            if content:
                messages.enqueue(Message(message=content))

    return messages

Agents: List[Agent] = []

def HireAgents(NumberOfAgents: int) -> None:
    experience_levels = ['básico', 'intermedio', 'experto']
    for _ in range(NumberOfAgents):
        level = choice(experience_levels)
        Agents.append(Agent(level))

def AssignMessages(worker: Agent, new_message: Message):
    worker.AssignedMessage = new_message
    worker.State = False
    duration = worker.AtentionTime()
    print(f"Agente {worker.AgentID} ({worker.ExperienceLevel}) trabajando por {duration:.2f}s en: {new_message}")
    time.sleep(duration)
    worker.State = True
    print(f"Agente {worker.AgentID} finalizó el trabajo.")

def CallCenter(MessagesQueue: PriorityQueue):
    while MessagesQueue.first() is not None:
        for worker in sorted(Agents, reverse=True): 
            if worker.State and MessagesQueue.first():
                msg = MessagesQueue.dequeue()
                if msg:
                    threading.Thread(target=AssignMessages, args=(worker, msg)).start()
        time.sleep(0.1)

def moda_len(cola: PriorityQueue):
        prioridades = defaultdict(int)
        for msg in cola:
            prioridades[msg.MessageLen] += 1
        moda = max(prioridades.values())
        for len, frecuencia in prioridades.items():
            if frecuencia == moda:
                return len       
        
      
def CallCenter_moda(MessagesQueue: PriorityQueue):
    moda = moda_len(MessagesQueue)
    aux_queue = PriorityQueue()
    while MessagesQueue.first() is not None:
        for worker in sorted(Agents, reverse=True): 
            if worker.State and MessagesQueue.first():    
                    msg = MessagesQueue.dequeue()
                    if msg.MessageLen == moda: 
                     threading.Thread(target=AssignMessages, args=(worker, msg)).start()
                    else:                     
                     aux_queue.enqueue(msg)
                     
    while aux_queue.first() is not None:
        MessagesQueue.enqueue(aux_queue.dequeue())
                     

                        
ListaMensajes = ReadData("messages_test2.txt")
HireAgents(5)
#CallCenter(ListaMensajes)

CallCenter_moda(ListaMensajes)