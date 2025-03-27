# call_center.py
import os
import sys
import signal
import time
import glob
import random
from call_center_queue import CallCenterQueue, EmptyQueue
from messages import Message
from agent import Agent

DATA_FOLDER = "data"

def load_messages_from_data(queue: CallCenterQueue):
    """
    Recorre la carpeta DATA_FOLDER, carga todos los archivos .txt,
    y encola cada mensaje encontrado en orden aleatorio sin repetirlos.
    """
    if not os.path.exists(DATA_FOLDER):
        print("La carpeta de datos no existe.")
        return

    txt_files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))
    all_messages = set()  # Usamos un conjunto para evitar duplicados

    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            mensajes = {line.strip() for line in file if line.strip()}  # Usamos un conjunto para evitar duplicados en cada archivo
            all_messages.update(mensajes)  # Agregamos los mensajes al conjunto global

    # Convertir a lista y mezclar aleatoriamente
    unique_messages = list(all_messages)
    random.shuffle(unique_messages)

    # Encolar los mensajes únicos en orden aleatorio
    for msj in unique_messages:
        queue.enqueue(Message(msj))

    print(f"\nSe han cargado {len(unique_messages)} mensajes únicos a la cola en orden aleatorio.")

    respuesta = input("¿Desea ver la cola ordenada? (s/n): ")
    
    if respuesta.lower() == "s":
        print("Mensajes en cola:")
        print(queue)
    
    print("Continuando con la operación...\n")


def seleccionar_agente(agents: list[Agent]) -> Agent:
    """
    Retorna el primer agente disponible. Si hay más de uno,
    se elige el que tenga mayor experiencia (según el factor: experto < intermedio < básico).
    """
    disponibles = [agent for agent in agents if agent.status == "disponible"]
    if not disponibles:
        return None
    # Se define un diccionario para ordenar por experiencia
    factor_experiencia = {"experto": 0.5, "intermedio": 0.75, "básico": 1.0}
    disponibles.sort(key=lambda agent: factor_experiencia.get(agent.experience_level, 1.0))
    return disponibles[0]

def mostrar_estado_agentes(agents: list[Agent]):
    """
    Imprime el estado actual de todos los agentes.
    """
    print("Estado de agentes:")
    for agent in agents:
        print(agent)
    print("")

def mostrar_menu():
    """
    Muestra el menú interactivo.
    """
    print("=== SIMULADOR DE CALL CENTER ===")
    print("1. Recargar mensajes desde carpeta 'data'")
    print("2. Atender un mensaje (selección aleatoria)")
    print("3. Mostrar estado de agentes")
    print("4. Salir")
    print("===============================")

def main():
    queue = CallCenterQueue()
    # Se crean tres agentes: uno de cada nivel de experiencia.
    agents = [
        Agent("básico"),
        Agent("intermedio"),
        Agent("experto")
    ]
    
    while True:
        mostrar_menu()
        # Siempre se muestra el estado de los agentes
        mostrar_estado_agentes(agents)
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            load_messages_from_data(queue)
        elif opcion == "2":
            if queue.is_empty():
                print("No hay mensajes en la cola.\n")
                continue
            # Selecciona aleatoriamente un mensaje a atender
            try:
                mensaje = queue.dequeue()
            except EmptyQueue as e:
                print(e)
                continue
            agente = seleccionar_agente(agents)
            if not agente:
                print("No hay agentes disponibles en este momento.\n")
                # Vuelve a encolar el mensaje
                queue.enqueue(mensaje)
                continue
            # El agente atiende el mensaje seleccionado aleatoriamente
            agente.atender(mensaje)
        elif opcion == "3":
            mostrar_estado_agentes(agents)
        elif opcion == "4":
            print("Saliendo del simulador. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")
        
        # Breve pausa antes de la siguiente iteración
        time.sleep(1)

if __name__ == "__main__":
    main()
