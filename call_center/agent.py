from call_center.messages import Message

class Agent:
    def __init__(self, experience_level: int, status):
        self.id = self.create_id()
        self.experience_level: int = experience_level
        self.status = status
        self.tiempo_de_respuesta = self.calculate_time()

    def create_id(self):
        id = 0

        return id + 1
    
    def calculate_time(self, experience_level: int, message: Message):
        ...
