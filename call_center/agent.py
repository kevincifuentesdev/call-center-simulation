# agent.py
import time
import uuid
from messages import Message

class Agent:
    def __init__(self, experience_level: str) -> None:
        """
        Inicializa un agente con un ID único y nivel de experiencia.
        Los niveles pueden ser 'básico', 'intermedio' o 'experto'.
        """
        self.id: str = str(uuid.uuid4())[:8]  # Se usa solo una parte del UUID para legibilidad
        self.experience_level: str = experience_level.lower()
        self.status: str = "disponible"  # "disponible" o "ocupado"
        self.tiempo_de_respuesta: float = 0.0

    def calculate_time(self, message: Message) -> float:
        """
        Calcula el tiempo estimado de atención basado en la longitud del mensaje,
        la prioridad y el factor de experiencia.
        Fórmula: (número de palabras / 10 + prioridad / 2) * factor
        Donde el factor es: 1.0 para 'básico', 0.75 para 'intermedio', 0.5 para 'experto'.
        """
        words = message.message.split()
        base_time = len(words) / 10 + message.priority / 2
        factor = {"básico": 1.0, "intermedio": 0.75, "experto": 0.5}.get(self.experience_level, 1.0)
        tiempo_final = base_time * factor
        self.tiempo_de_respuesta = tiempo_final
        return tiempo_final

    def atender(self, message: Message) -> None:
        """
        Atiende el mensaje asignado: muestra información, simula el tiempo de atención,
        y actualiza el estado del agente.
        """
        self.status = "ocupado"
        t = self.calculate_time(message)
        print(f"\nAgente {self.id} ({self.experience_level.title()}) está atendiendo:")
        print(f"  Mensaje: {message.message}")
        print(f"  Prioridad: {message.priority} | Tiempo estimado: {t:.2f} segundos")
        print("Procesando...\n", flush=True)
        time.sleep(t)
        print(f"Agente {self.id} ha finalizado la atención.\n")
        self.status = "disponible"

    def __repr__(self) -> str:
        return f"Agente {self.id} ({self.experience_level.title()} - {self.status})"
