# messages.py
from typing import Dict

class Message:
    def __init__(self, message: str) -> None:
        # Diccionario de palabras clave con sus pesos
        self.__key_words: Dict[str, int] = {
            "urgente": 9, "emergencia": 8, "fallo": 7,
            "problema": 6, "ayuda": 4, "consulta": 3, "duda": 2
        }
        self.message: str = message
        self.priority: int = self.calculate_priority()

    def calculate_priority(self) -> int:
        """
        Calcula la prioridad del mensaje sumando los pesos
        de cada palabra clave encontrada en el mensaje.
        """
        words_message = self.message.split()
        priority = 0
        for word in words_message:
            word = ''.join(char for char in word if char.isalnum()).lower()
            if word in self.__key_words:
                priority += self.__key_words[word]
        return priority

    def __lt__(self, other: 'Message') -> bool:
        # Permite comparar mensajes por prioridad (para ordenarlos)
        return self.priority < other.priority

    def __repr__(self) -> str:
        return f"({self.priority}) {self.message}"
