from call_center import (
    CallCenterQueue, load_messages_from_data, initialize_agents,
    start_agent_threads, stop_agents, get_queue_status, agent_worker  # Añadir agent_worker
)
from agent_queue import AgentQueue
import time
from threading import Event
import threading
import sys  # Importamos sys para manejar la salida

def main():
    queue = CallCenterQueue()
    agent_queue = AgentQueue()
    agents = initialize_agents()
    for agent in agents:
        agent_queue.enqueue(agent)

    processing_enabled = Event()
    stop_event = Event()
    threads = []
    processing_started = False
    registro_atenciones = []

    # Forzamos el flush de la salida
    sys.stdout.flush()

    while True:
        print("\n=== SIMULADOR DE CALL CENTER ===", flush=True)
        print("1. Recargar mensajes desde carpeta 'data'", flush=True)
        print("2. Mostrar la cola de mensajes", flush=True)
        print("3. Detener procesamiento y salir", flush=True)
        print("4. Procesar solo PRIMER y ÚLTIMO mensaje del grupo mayoritario", flush=True)
        print("===================================", flush=True)
        
        try:
            opt = input("Seleccione una opción: ").strip()
        except EOFError:
            print("\nEntrada no válida. Saliendo...", flush=True)
            break
            
        if opt == "1":
            registro_atenciones.clear()
            print("\nCargando mensajes desde la carpeta 'data'...", flush=True)
            load_messages_from_data(queue)
            print(f"Mensajes cargados correctamente. Total: {len(queue)}", flush=True)
        elif opt == "2":
            print("\nCola de mensajes actual:", flush=True)
            print(get_queue_status(queue), flush=True)
        elif opt == "3":
            print("\nDeteniendo el procesamiento...", flush=True)
            if processing_started:
                processing_enabled.clear()
                stop_event.set()
                stop_agents(threads, stop_event)
            break
        
        elif opt == "4":
            if not processing_started:
                registro_atenciones.clear()
                print("\nIniciando procesamiento de extremos...", flush=True)
                
                if len(queue) < 2:
                    print("Se necesitan al menos 2 mensajes", flush=True)
                    continue
                    
                processing_enabled.set()
                stop_event.clear()
                
                # Crear y configurar el hilo correctamente
                t = threading.Thread(
                    target= agent_worker,
                    args=(
                        agent_queue,
                        queue,
                        stop_event,
                        processing_enabled,
                        True,  # modo_extremos=True
                        registro_atenciones
                    ),
                    daemon=True
                )
                t.start()
                threads = [t]
                processing_started = True
                
                # Esperar con timeout
                t.join(15)  # Esperar máximo 15 segundos
                
                # Generar reporte
                print("\n\n=== REPORTE FINAL ===", flush=True)
                if len(registro_atenciones) == 2:
                    print("✓ 2 mensajes del grupo mayoritario atendidos:")
                    print(f"1. {registro_atenciones[0]['mensaje']}")
                    print(f"2. {registro_atenciones[1]['mensaje']}")
                    print(f"Prioridad común: {registro_atenciones[0]['prioridad']}")
                else:
                    print(f"✗ Error: Se atendieron {len(registro_atenciones)} mensajes")
                
                print(f"\nMensajes restantes: {len(queue)}")
                processing_enabled.clear()
                stop_event.set()
                break

if __name__ == "__main__":
    main()