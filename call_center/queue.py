from message import Message

class EmptyQueue(Exception):
    ...

class CallCenterQueue:
    def __init__(self):
        self.__queue: list[Message] = []

    def enqueue(self, element: int):
        self.__queue.append(element)
        self.__queue.sort(reverse=True)

    def dequeue(self):
        if(len(self.__queue) == 0):
            raise EmptyQueue("Cola de Mensajes vacía...")
        return self.__queue.pop(0)

    def first(self):
        if(len(self.__queue) == 0):
            raise EmptyQueue("Cola de Mensajes vacía...")
        return self.__queue[0]

    def __repr__(self):
        return str(self.__queue)