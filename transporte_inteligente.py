"""
Sistema Inteligente de Transporte Masivo - Algoritmo de Búsqueda A* (A-Star)
=============================================================================
Este módulo modela una red de transporte público (Metro) como un grafo ponderado
y utiliza el algoritmo de búsqueda heurística A* para encontrar la ruta óptima
(con menor tiempo estimado en minutos) entre dos estaciones cualesquiera.
"""

import heapq


class SistemaTransporteInteligente:
    """
    Clase que encapsula el grafo de la red de transporte y la lógica del algoritmo A*.
    """

    def __init__(self):
        # -------------------------------------------------------------------------
        # BASE DE CONOCIMIENTO (GRAFO PONDERADO)
        # Representa las estaciones y sus conexiones adyacentes directas.
        # Las claves secundarias son las estaciones vecinas y los valores son el
        # tiempo promedio de traslado entre ellas medido en minutos.
        # -------------------------------------------------------------------------
        self.grafo = {
            "Niquía": {"Bello": 4},
            "Bello": {"Niquía": 4, "Madera": 3},
            "Madera": {"Bello": 3, "Acevedo": 3},
            "Acevedo": {"Madera": 3, "Tricentenario": 4},
            "Tricentenario": {"Acevedo": 4, "Caribe": 3},
            "Caribe": {"Tricentenario": 3, "Universidad": 3},
            "Universidad": {"Caribe": 3, "Hospital": 2},
            "Hospital": {"Universidad": 2, "Prado": 2},
            "Prado": {"Hospital": 2, "Parque Berrio": 2},
            "Parque Berrio": {"Prado": 2, "San Antonio": 3},
            "San Antonio": {"Parque Berrio": 3, "Alpujarra": 2, "Cisneros": 4},
            "Alpujarra": {"San Antonio": 2, "Exposiciones": 2},
            "Exposiciones": {"Alpujarra": 2, "Industriales": 3},
            "Industriales": {"Exposiciones": 3, "Poblado": 4},
            "Poblado": {"Industriales": 4, "Aguacatala": 3},
            "Aguacatala": {"Poblado": 3, "Ayurá": 3},
            "Ayurá": {"Aguacatala": 3, "Envigado": 3},
            "Envigado": {"Ayurá": 3, "Itagüí": 3},
            "Itagüí": {"Envigado": 3, "Sabaneta": 4},
            "Sabaneta": {"Itagüí": 4, "La Estrella": 5},
            "La Estrella": {"Sabaneta": 5}
        }
        
        # -------------------------------------------------------------------------
        # FUNCIÓN HEURÍSTICA BASE: h(n)
        # Representa una estimación del tiempo ideal (en minutos) desde cada estación
        # hacia un punto de referencia a lo largo de la línea troncal.
        # Sirve para guiar la búsqueda hacia el destino de manera eficiente y admisible.
        # -------------------------------------------------------------------------
        self.heuristica_base = {
            "Niquía": 35, "Bello": 31, "Madera": 28, "Acevedo": 25, 
            "Tricentenario": 21, "Caribe": 18, "Universidad": 15, "Hospital": 13, 
            "Prado": 11, "Parque Berrio": 9, "San Antonio": 6, "Alpujarra": 8, 
            "Exposiciones": 10, "Industriales": 12, "Poblado": 16, "Aguacatala": 19, 
            "Ayurá": 22, "Envigado": 25, "Itagüí": 28, "Sabaneta": 32, "La Estrella": 37
        }

    def obtener_heuristica(self, actual, destino):
        """
        Calcula el valor heurístico h(n) entre la estación actual y el destino final.
        Utiliza la diferencia absoluta de sus posiciones estimadas para proyectar
        el tiempo mínimo restante.
        """
        return abs(self.heuristica_base.get(actual, 0) - self.heuristica_base.get(destino, 0))

    def buscar_mejor_ruta(self, inicio_input, destino_input):
        """
        Implementa el algoritmo de búsqueda A* (A-Star) para calcular el camino óptimo.
        
        Parámetros:
            inicio_input (str): Nombre de la estación de origen ingresada por el usuario.
            destino_input (str): Nombre de la estación de destino ingresada por el usuario.

        Retorna:
            dict: Con la lista de estaciones ('ruta') y el tiempo acumulado ('tiempo_estimado_minutos').
            str: Mensaje de error si la estación no existe o si no hay conexión disponible.
        """
        # Normalización: buscar coincidencia insensible a mayúsculas, minúsculas y espacios
        inicio = next((k for k in self.grafo if k.lower() == inicio_input.strip().lower()), None)
        destino = next((k for k in self.grafo if k.lower() == destino_input.strip().lower()), None)

        # Validación: comprobar que ambas estaciones existan en la red
        if not inicio or not destino:
            return "Error: Una de las estaciones ingresadas no existe en la base de conocimiento."

        # Cola de prioridad (min-heap) para gestionar los nodos por explorar.
        # Estructura de cada elemento: (f, g, estación_actual, camino_recorrido)
        # - f = g + h : Costo total estimado
        # - g : Costo real acumulado en minutos desde el origen hasta aquí
        # - actual : Nombre de la estación en curso
        # - camino : Lista de estaciones visitadas hasta el momento
        pq = [(0, 0, inicio, [inicio])]
        
        # Conjunto para registrar estaciones ya evaluadas y evitar ciclos o rutas redundantes
        visitados = set()

        while pq:
            # Extraer el nodo con el menor costo estimado 'f'
            f, g, actual, camino = heapq.heappop(pq)

            # Si llegamos al destino, hemos encontrado la ruta óptima
            if actual == destino:
                return {"ruta": camino, "tiempo_estimado_minutos": g}

            # Si ya expandimos este nodo con un costo menor, continuamos
            if actual in visitados:
                continue
            visitados.add(actual)

            # Explorar cada estación adyacente (vecinos)
            for vecino, peso in self.grafo[actual].items():
                if vecino not in visitados:
                    # g: costo real acumulado sumando el tramo actual
                    nuevo_g = g + peso
                    # h: estimación heurística restante desde el vecino al destino
                    nuevo_h = self.obtener_heuristica(vecino, destino)
                    # f = g + h : función de evaluación del algoritmo A*
                    nuevo_f = nuevo_g + nuevo_h
                    
                    # Insertar el vecino en la cola de prioridad con el camino actualizado
                    heapq.heappush(pq, (nuevo_f, nuevo_g, vecino, camino + [vecino]))

        # En caso de no existir conexión entre origen y destino
        return "No se encontró una ruta disponible."


# ==============================================================================
# EJECUCIÓN INTERACTIVA EN CONSOLA
# ==============================================================================
if __name__ == "__main__":
    sistema = SistemaTransporteInteligente()
    
    print("==================================================")
    print("    SISTEMA INTELIGENTE DE TRANSPORTE MASIVO")
    print("==================================================")
    print("Estaciones disponibles:")
    print(", ".join(sistema.grafo.keys()))
    print("--------------------------------------------------")
    
    # Solicitar datos al usuario
    origen = input("Ingrese la estación de ORIGEN: ")
    destino = input("Ingrese la estación de DESTINO: ")
    
    print(f"\n--- CALCULANDO MEJOR RUTA DE '{origen}' A '{destino}' ---")
    resultado = sistema.buscar_mejor_ruta(origen, destino)
    
    # Mostrar resultados en pantalla
    if isinstance(resultado, dict):
        print(f"Ruta óptima encontrada: {' -> '.join(resultado['ruta'])}")
        print(f"Tiempo total estimado: {resultado['tiempo_estimado_minutos']} minutos.")
    else:
        print(resultado)