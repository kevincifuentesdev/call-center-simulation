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
                message = line.strip()
                if message:  # Ignorar líneas vacías
                    queue.enqueue(Message(message))
    
    with print_lock:
        print(f"\nSe han cargado {len(queue)} mensajes únicos a la cola.")

def major_value_messages(messages: CallCenterQueue) -> tuple[int, Message, Message]:
    """
    Encuentra el grupo de mensajes con la prioridad más frecuente y retorna:
    - La prioridad con más ocurrencias.
    - El primer mensaje del grupo.
    - El último mensaje del grupo.
    """
    aux_queue = CallCenterQueue()
    priority_counts = {}

    # Step 1: Count occurrences of each priority
    with messages.lock:
        while len(messages) > 0:
            msg = messages.dequeue()
            priority_counts[msg.priority] = priority_counts.get(msg.priority, 0) + 1
            aux_queue.enqueue(msg)

    # Step 2: Find the priority with the most occurrences
    major_priority = max(priority_counts, key=priority_counts.get)

    first_message = None
    last_message = None

    # Step 3: Process messages and remove all messages of the major group
    with aux_queue.lock:
        while len(aux_queue) > 0:
            msg = aux_queue.dequeue()
            if msg.priority == major_priority:
                if first_message is None:
                    first_message = msg  # Capture the first message
                last_message = msg  # Update the last message
            else:
                messages.enqueue(msg)  # Re-enqueue non-major-priority messages

    return major_priority, first_message, last_message

def agent_worker(agent_queue: AgentQueue, message_queue: CallCenterQueue, stop_event: threading.Event, processing_enabled: threading.Event):
    while not stop_event.is_set():
        processing_enabled.wait()  # Esperar hasta que el procesamiento esté habilitado
        agent = agent_queue.dequeue()  # Obtener el agente con mayor prioridad
        if agent.status == "disponible":
            if message_queue.is_empty():
                # Si no hay más mensajes, reinsertar el agente y salir del bucle
                agent_queue.enqueue(agent)
                break
            msg = message_queue.dequeue()
            
            agent.atender(msg)

        # Reinsertar el agente en la cola después de atender o si no hay mensajes
        agent_queue.enqueue(agent)

def initialize_agents(agent_queue: AgentQueue):
    agents = [Agent("experto"), Agent("intermedio"), Agent("básico")]
    for agent in agents:
        agent_queue.enqueue(agent)  # Encolar agentes

    return agent_queue

def start_agent_threads(agent_queue: AgentQueue, queue: CallCenterQueue, processing_enabled: threading.Event, stop_event: threading.Event):
    threads = []
    for _ in range(len(agent_queue)):
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
