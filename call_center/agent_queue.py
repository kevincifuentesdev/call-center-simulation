import threading
from typing import List, Optional
from agent import Agent

# filepath: /home/kevin/call-center-simulation/call_center/agent_queue.py
# agent_queue.py

class EmptyQueue(Exception):
    pass

class AgentQueue:
    def __init__(self) -> None:
        self.__queue: List[Agent] = []
        self.__lock = threading.Lock()  # Lock para acceso seguro en hilos

    def enqueue(self, agent: Agent) -> None:
        """
        Agrega un agente a la cola y la ordena en forma ascendente según el nivel de experiencia.
        'Experto' tiene mayor prioridad, seguido de 'Intermedio' y luego 'Básico'.
        """
        with self.__lock:
            self.__queue.append(agent)
            self.__queue.sort()

    def dequeue(self) -> Agent:
        """
        Extrae y retorna el agente con mayor prioridad. Lanza EmptyQueue si la cola está vacía.
        """
        with self.__lock:
            if not self.__queue:
                raise EmptyQueue("La cola de agentes está vacía.")
            return self.__queue.pop(0)

    def is_empty(self) -> bool:
        """
        Verifica si la cola está vacía.
        """
        with self.__lock:
            return len(self.__queue) == 0
        
    def __len__(self) -> int:
        """
        Retorna el número de agentes en la cola.
        """
        with self.__lock:
            return len(self.__queue)

    def __repr__(self) -> str:
        """
        Representación de la cola de agentes.
        """
        with self.__lock:
            return str(self.__queue)