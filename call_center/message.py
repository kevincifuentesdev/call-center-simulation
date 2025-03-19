class Message:
    def __init__(self, message: str):
        self.__key_words = {"urgente": 9, "emergencia": 8, "fallo": 7, "problema": 6, "ayuda": 4, "consulta": 3, "duda": 2}
        self.message: str = message
        self.priority: int = self.calculate_priority()

    def calculate_priority(self):
        words_message = self.message.split()
        priority = 0

        for word in words_message:
            if word.lower() in self.__key_words.keys():
                priority += self.__key_words[word]

        return priority
    
    def __lt__(self, other):
        return len(self.message) < len(other.message)