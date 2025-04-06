from collections import defaultdict
from threading import Lock
from messages import Message
from typing import List

class EmptyQueue(Exception):
    pass

class CallCenterQueue:
    def __init__(self) -> None:
        self.__queue = []
        self.__lock = Lock()  # Lock para acceso seguro en hilos

    def enqueue(self, message: Message) -> None:
        """
        Agrega un mensaje a la cola y la ordena en forma descendente (mayor prioridad primero).
        """
        with self.__lock:
            self.__queue.append(message)
            self.__queue.sort(reverse=True)

    def dequeue(self) -> Message:
        """
        Extrae y retorna el mensaje de mayor prioridad. Lanza EmptyQueue si la cola está vacía.
        """
        with self.__lock:
            if not self.__queue:
                raise EmptyQueue("La cola de mensajes está vacía.")
            return self.__queue.pop(0)
        
    
    def is_empty(self) -> bool:
        with self.__lock:
            return len(self.__queue) == 0
        

    def dequeue_extremos_grupo_mayor(self) -> List[Message]:
        """Extrae SOLO el primer y último mensaje del grupo mayoritario"""
        with self.__lock:
            if len(self.__queue) < 2:
                raise EmptyQueue("No hay suficientes mensajes")

            # 1. Contar prioridades
            prioridades = defaultdict(int)
            for msg in self.__queue:
                prioridades[msg.priority] += 1

            # 2. Determinar prioridad objetivo
            max_count = max(prioridades.values())
            target_priority = max(p for p, cnt in prioridades.items() if cnt == max_count)

            # 3. Buscar todos los índices de la prioridad objetivo
            target_indices = [i for i, msg in enumerate(self.__queue) if msg.priority == target_priority]
            
            if len(target_indices) < 2:
                return []

            # 4. Obtener primer y último índice
            primer_idx = target_indices[0]
            ultimo_idx = target_indices[-1]

            # 5. Extraer mensajes y actualizar cola
            primer_msg = self.__queue[primer_idx]
            ultimo_msg = self.__queue[ultimo_idx]
            
            # Eliminar de mayor a menor índice para evitar desfases
            for idx in sorted([primer_idx, ultimo_idx], reverse=True):
                del self.__queue[idx]

            return [primer_msg, ultimo_msg]

    def __repr__(self) -> str:
        with self.__lock:
            return str(self.__queue)

    def __len__(self):
        return len(self.__queue)
    
    def size(self) -> int:
        """Devuelve el número de mensajes en la cola"""
        with self.__lock:
            return len(self.__queue)






           