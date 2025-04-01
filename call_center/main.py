from call_center import (
    CallCenterQueue, load_messages_from_data, initialize_agents,
    start_agent_threads, stop_agents, get_agents_status, get_queue_status
)
import time
from threading import Event

def main():
    queue = CallCenterQueue()
    agents = initialize_agents()
    processing_enabled = Event()  # Bandera para controlar el procesamiento
    threads = []  # Lista para almacenar los hilos de los agentes
    processing_started = False  # Bandera para verificar si el procesamiento ya comenzó

    while True:
        # Mostrar el menú principal
        print("=== SIMULADOR DE CALL CENTER ===")
        print("1. Recargar mensajes desde carpeta 'data'")
        print("2. Mostrar la cola de mensajes")
        print("3. Mostrar estado de agentes")
        print("4. Detener procesamiento y salir")
        print("5. Procesar TODOS los mensajes y finalizar")
        print("===================================")
        opt = input("Seleccione una opción: ").strip()
        
        if opt == "1":
            print("Cargando mensajes desde la carpeta 'data'...")
            load_messages_from_data(queue)
            print("Mensajes cargados correctamente.")
        elif opt == "2":
            print("Cola de mensajes:")
            print(get_queue_status(queue))
        elif opt == "3":
            print("Estado de agentes:")
            print(get_agents_status(agents))
        elif opt == "4":
            print("Deteniendo el procesamiento y finalizando...")
            if processing_started:
                processing_enabled.clear()  # Detener procesamiento
                stop_agents(threads)
            break
        elif opt == "5":
            if not processing_started:
                print("Iniciando el procesamiento de mensajes...")
                processing_enabled.set()  # Habilitar procesamiento
                threads = start_agent_threads(agents, queue, processing_enabled)
                processing_started = True
            else:
                print("El procesamiento ya está en curso.")
            
            # Esperar a que todos los mensajes sean procesados
            while not queue.is_empty() or any(agent.status == "ocupado" for agent in agents):
                print("Procesando mensajes... Por favor, espere.")
                time.sleep(1)
            
            print("Todos los mensajes han sido procesados.")
            processing_enabled.clear()  # Detener procesamiento
            stop_agents(threads)
            break
        else:
            print("Opción inválida. Intente de nuevo.")
        
        time.sleep(1)
    
    if queue.is_empty():
        print("Procedimiento finalizado: todos los mensajes han sido atendidos.")
    else:
        print("Procesamiento detenido. Mensajes pendientes en la cola:")
        print(get_queue_status(queue))

if __name__ == "__main__":
    main()
