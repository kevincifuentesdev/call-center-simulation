# agent.py
import time
import uuid
import sys
from messages import Message

class Agent:
    def __init__(self, experience_level: str):
        """
        Inicializa un agente con un ID único y nivel de experiencia.
        Los agentes pueden ser "básico", "intermedio" o "experto".
        """
        self.id = str(uuid.uuid4())[:8]  # Genera un ID único (solo los primeros 8 caracteres)
        self.experience_level: str = experience_level.lower()
        self.status: str = "disponible"
        self.tiempo_de_respuesta: float = 0.0

    def calculate_time(self, message: Message) -> float:
        """
        Calcula el tiempo estimado de atención basado en la longitud del mensaje,
        la prioridad (peso de palabras clave) y el factor según la experiencia.
        """
        longitud_mensaje = len(message.message.split())
        peso_palabras_clave = message.priority
        tiempo_estimado = (longitud_mensaje / 10) + (peso_palabras_clave / 2)
        
        # Factor de ajuste según el nivel de experiencia
        factor = {"básico": 1.0, "intermedio": 0.75, "experto": 0.5}.get(self.experience_level, 1.0)
        
        tiempo_final = tiempo_estimado * factor
        self.tiempo_de_respuesta = tiempo_final
        return tiempo_final

    def atender(self, message: Message):
        """
        Simula la atención del mensaje con una barra de progreso visual.
        """
        self.status = "ocupado"
        tiempo = self.calculate_time(message)

        print(f"\n\033[1;34mAgente {self.id} ({self.experience_level.title()}) está atendiendo:\033[0m")
        print(f"  📩 Mensaje: {message.message}")
        print(f"   Prioridad: {message.priority} | ⏳ Tiempo estimado: {tiempo:.2f} segundos\n")

        # Simulación con barra de progreso
        self.simular_progreso(tiempo)

        print(f"\n\033[1;32m✅ Agente {self.id} ha finalizado la atención.\033[0m\n")
        self.status = "disponible"

    def simular_progreso(self, tiempo: float):
        """
        Simula la espera con una barra de progreso visual en la consola.
        """
        barra_longitud = 30  # Longitud de la barra de progreso
        intervalo = tiempo / barra_longitud  # Tiempo de espera por cada paso

        for i in range(barra_longitud):
            porcentaje = int((i + 1) / barra_longitud * 100)
            barra = "█" * (i + 1) + "-" * (barra_longitud - (i + 1))
            sys.stdout.write(f"\r[{barra}] {porcentaje}%")
            sys.stdout.flush()
            time.sleep(intervalo)
        
        sys.stdout.write("\n")  # Nueva línea después de la barra de progreso

    def __repr__(self):
        return f"Agente {self.id} ({self.experience_level.title()} - {self.status})"
