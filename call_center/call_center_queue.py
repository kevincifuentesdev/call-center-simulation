# call_center_queue.py
import random
import threading
from typing import List, Optional
from messages import Message

class EmptyQueue(Exception):
    pass

class CallCenterQueue:
    def __init__(self) -> None:
        self.__queue: List[Message] = []
        self.lock = threading.Lock()  # Lock para acceso seguro en hilos

    def enqueue(self, message: Message) -> None:
        """
        Agrega un mensaje a la cola y la ordena en forma descendente (mayor prioridad primero).
        """
        with self.lock:
            self.__queue.append(message)
            self.__queue.sort(reverse=True)

    def dequeue(self) -> Message:
        """
        Extrae y retorna el mensaje de mayor prioridad. Lanza EmptyQueue si la cola está vacía.
        """
        with self.lock:
            if not self.__queue:
                raise EmptyQueue("La cola de mensajes está vacía.")
            return self.__queue.pop(0)
        
    def first(self) -> Message:
        with self.lock:
            return self.__queue[0]

    def is_empty(self) -> bool:
        with self.lock:
            if not self.__queue:
                raise EmptyQueue("La cola de mensajes está vacía.")
            return len(self.__queue) == 0
        
    def __len__(self):
        return len(self.__queue)

    def __repr__(self) -> str:
        with self.lock:
            return str(self.__queue)
