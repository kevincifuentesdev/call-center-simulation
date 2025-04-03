import os
import glob
import random
import threading
import time
from call_center_queue import CallCenterQueue, EmptyQueue
from messages import Message
from agent import Agent
from agent_queue import AgentQueue

DATA_FOLDER = "data"
print_lock = threading.Lock()

def load_messages_from_data(queue: CallCenterQueue):
    if not os.path.exists(DATA_FOLDER):
        print("La carpeta de datos no existe.")
        return

    txt_files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))
    print(f"Archivos encontrados: {txt_files}")
    random.shuffle(txt_files)

    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                mensaje = line.strip()
                if mensaje:  # Ignorar líneas vacías
                    queue.enqueue(Message(mensaje))
    
    with print_lock:
        print(f"\nSe han cargado {len(queue._CallCenterQueue__queue)} mensajes únicos a la cola.")

def agent_worker(agent_queue: AgentQueue, message_queue: CallCenterQueue, stop_event: threading.Event, processing_enabled: threading.Event):
    try:
        while not stop_event.is_set():
            processing_enabled.wait()  # Esperar hasta que el procesamiento esté habilitado
            try:
                agent = agent_queue.dequeue()  # Obtener el agente con mayor prioridad
                if agent.status == "disponible":
                    if message_queue.is_empty():
                        # Si no hay más mensajes, reinsertar el agente y salir del bucle
                        agent_queue.enqueue(agent)
                        break
                    msg = message_queue.dequeue()
                    if msg:
                        agent.atender(msg)
                # Reinsertar el agente en la cola después de atender o si no hay mensajes
                agent_queue.enqueue(agent)
            except EmptyQueue:
                time.sleep(0.1)
    except Exception as e:
        print(f"Error en el agente: {e}")

def initialize_agents():
    return [Agent("experto"), Agent("intermedio"), Agent("básico")]

def start_agent_threads(agent_queue: AgentQueue, queue: CallCenterQueue, processing_enabled: threading.Event, stop_event: threading.Event):
    threads = []
    for _ in range(len(agent_queue)):  # Use len(agent_queue) to determine the number of threads
        t = threading.Thread(target=agent_worker, args=(agent_queue, queue, stop_event, processing_enabled))
        t.daemon = True
        t.start()
        threads.append(t)
    return threads

def stop_agents(threads, stop_event):
    stop_event.set()
    for t in threads:
        t.join(timeout=5)  # Esperar hasta 5 segundos por cada hilo
        if t.is_alive():
            print(f"Advertencia: El hilo {t.name} no se detuvo correctamente.")

def get_agents_status(agents):
    return print(agents)

def get_queue_status(queue):
    return str(queue)
