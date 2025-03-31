import os
import glob
import random
import threading
import time
from call_center_queue import CallCenterQueue, EmptyQueue
from messages import Message
from agent import Agent

DATA_FOLDER = "data"
stop_event = threading.Event()
print_lock = threading.Lock()

def load_messages_from_data(queue: CallCenterQueue):
    if not os.path.exists(DATA_FOLDER):
        print("La carpeta de datos no existe.")
        return

    txt_files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))
    print(txt_files)
    random.shuffle(txt_files)
    print(txt_files)

    messages_set = set()

    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            mensajes = [line.strip() for line in file if line.strip()]
            messages_set.update(mensajes)

    unique_messages = list(messages_set)
    random.shuffle(unique_messages)
    
    for msj in unique_messages:
        queue.enqueue(Message(msj))
    
    with print_lock:
        print(f"\nSe han cargado {len(unique_messages)} mensajes únicos a la cola en orden aleatorio.")

def agent_worker(agent: Agent, queue: CallCenterQueue, stop_event: threading.Event):
    while not stop_event.is_set():
        if agent.status == "disponible":
            msg = queue.try_dequeue()
            if msg:
                agent.atender(msg)
            else:
                time.sleep(0.5)
        else:
            time.sleep(0.1)

def initialize_agents():
    return [Agent("experto"), Agent("intermedio"),Agent("básico")]

def start_agent_threads(agents, queue):
    threads = []
    for agent in agents:
        t = threading.Thread(target=agent_worker, args=(agent, queue, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
    return threads

def stop_agents(threads):
    stop_event.set()
    for t in threads:
        t.join()

def get_agents_status(agents):
    return "\n".join(str(agent) for agent in agents)

def get_queue_status(queue):
    return str(queue)
