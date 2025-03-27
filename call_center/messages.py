# messages.py
class Message:
    def __init__(self, message: str):
        # Diccionario de palabras clave con sus pesos
        self.__key_words = {
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
            # Limpia la palabra de caracteres especiales y la pasa a minúsculas
            word = ''.join(char for char in word if char.isalnum()).lower()
            if word in self.__key_words:
                priority += self.__key_words[word]
        return priority

    def __lt__(self, other):
        # Permite comparar mensajes por prioridad
        return self.priority < other.priority

    def __repr__(self):
        return f"({self.priority}) {self.message}"
