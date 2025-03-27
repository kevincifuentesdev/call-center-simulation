# call_center_queue.py
import random
from messages import Message

class EmptyQueue(Exception):
    pass

class CallCenterQueue:
    def __init__(self):
        self.__queue: list[Message] = []

    def enqueue(self, message: Message):
        """
        Agrega un mensaje a la cola y la ordena en forma descendente.
        """
        self.__queue.append(message)
        self.__queue.sort(reverse=True)
        
    def dequeue(self) -> Message:
        """
        Extrae y retorna el primer mensaje de la cola.
        """
        if not self.__queue:
            raise EmptyQueue("La cola de mensajes está vacía.")
        return self.__queue.pop(0)

    def dequeue_random(self) -> Message:
        """
        Extrae y retorna un mensaje aleatorio de la cola.
        """
        if not self.__queue:
            raise EmptyQueue("La cola de mensajes está vacía.")
        index = random.randrange(len(self.__queue))
        return self.__queue.pop(index)

    def first(self) -> Message:
        """
        Retorna el primer mensaje de la cola sin extraerlo.
        """
        if not self.__queue:
            raise EmptyQueue("La cola de mensajes está vacía.")
        return self.__queue[0]

    def is_empty(self) -> bool:
        """
        Retorna True si la cola está vacía.
        """
        return len(self.__queue) == 0

    def __repr__(self):
        return str(self.__queue)
