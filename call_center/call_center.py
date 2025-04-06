import os
import glob
import random
import threading
import time
from call_center_queue import CallCenterQueue, EmptyQueue
from messages import Message
from agent import Agent
from agent_queue import AgentQueue
from datetime import datetime

DATA_FOLDER = "data"
print_lock = threading.Lock()

def load_messages_from_data(queue: CallCenterQueue):
    """Carga mensajes desde archivos en la carpeta data"""
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
                if message:
                    queue.enqueue(Message(message))
    
    with print_lock:
        print(f"\nSe han cargado {len(queue._CallCenterQueue__queue)} mensajes únicos a la cola.")

def agent_worker(
    agent_queue: AgentQueue,
    message_queue: CallCenterQueue,
    stop_event: threading.Event,
    processing_enabled: threading.Event,
    modo_extremos: bool = True,
    registro_atenciones: list = None
):
    try:
        processed = False
        while not stop_event.is_set() and not processed:
            processing_enabled.wait()
            
            try:
                agent = agent_queue.dequeue()
                
                if agent.status == "disponible":
                    if message_queue.is_empty():
                        agent_queue.enqueue(agent)
                        break
                    
                    if modo_extremos:
                        try:
                            mensajes = message_queue.dequeue_extremos_grupo_mayor()
                            if mensajes and len(mensajes) == 2:
                                for msg in mensajes:
                                    registro = {
                                        'agente': agent.id,
                                        'nivel': agent.experience_level,
                                        'mensaje': msg.message,
                                        'prioridad': msg.priority,
                                        'timestamp': datetime.now().strftime("%H:%M:%S")
                                    }
                                    if registro_atenciones is not None:
                                        registro_atenciones.append(registro)
                                    agent.atender(msg)
                                processed = True  # Marcar como procesado
                                stop_event.set()   # Detener todos los hilos
                        except Exception as e:
                            print(f"Error: {str(e)}")
                            continue
                
                agent_queue.enqueue(agent)
                
            except EmptyQueue:
                time.sleep(0.1)
    except Exception as e:
        print(f"Error crítico: {str(e)}")
        
def initialize_agents():
    """Inicializa los agentes disponibles"""
    return [Agent("experto"), Agent("intermedio"), Agent("básico")]

def start_agent_threads(
    agent_queue: AgentQueue, 
    queue: CallCenterQueue, 
    processing_enabled: threading.Event, 
    stop_event: threading.Event, 
    modo_extremos: bool = False,
    registro_atenciones: list = None
):
    """Inicia los hilos de los agentes"""
    threads = []
    for _ in range(len(agent_queue)):
        t = threading.Thread(
            target=agent_worker,
            args=(agent_queue, queue, stop_event, processing_enabled, modo_extremos, registro_atenciones)
        )
        t.daemon = True
        t.start()
        threads.append(t)
    return threads

def stop_agents(threads, stop_event):
    """Detiene los hilos de los agentes"""
    stop_event.set()
    for t in threads:
        t.join(timeout=5)
        if t.is_alive():
            print(f"Advertencia: El hilo {t.name} no se detuvo correctamente.")

def get_queue_status(queue):
    """Obtiene el estado actual de la cola"""
    return str(queue)