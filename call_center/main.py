from call_center import (
    CallCenterQueue, load_messages_from_data, initialize_agents,
    start_agent_threads, stop_agents, get_agents_status, get_queue_status
)
import time

def main():
    queue = CallCenterQueue()
    agents = initialize_agents()
    threads = start_agent_threads(agents, queue)
    
    while True:
        print("=== SIMULADOR DE CALL CENTER ===")
        print("1. Recargar mensajes desde carpeta 'data'")
        print("2. Mostrar la cola de mensajes")
        print("3. Mostrar estado de agentes")
        print("4. Detener procesamiento y salir")
        print("5. Procesar TODOS los mensajes y finalizar")
        print("===================================")
        opt = input("Seleccione una opción: ").strip()
        
        if opt == "1":
            load_messages_from_data(queue)
        elif opt == "2":
            print("Cola de mensajes:")
            print(get_queue_status(queue))
        elif opt == "3":
            print("Estado de agentes:")
            print(get_agents_status(agents))
        elif opt == "4":
            print("Deteniendo el procesamiento y finalizando...")
            stop_agents(threads)
            break
        elif opt == "5":
            print("Procesando TODOS los mensajes y finalizando...")
            load_messages_from_data(queue)
            while not queue.is_empty():
                time.sleep(1)
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
