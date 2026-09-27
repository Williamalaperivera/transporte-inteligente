import heapq

class SistemaTransporteInteligente:
    def __init__(self):
        # Base de conocimiento: Estaciones y sus conexiones directas (Tiempos en minutos)
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
        
        # Heurística estimada (costo ideal en minutos hacia el destino final)
        self.heuristica_base = {
            "Niquía": 35, "Bello": 31, "Madera": 28, "Acevedo": 25, 
            "Tricentenario": 21, "Caribe": 18, "Universidad": 15, "Hospital": 13, 
            "Prado": 11, "Parque Berrio": 9, "San Antonio": 6, "Alpujarra": 8, 
            "Exposiciones": 10, "Industriales": 12, "Poblado": 16, "Aguacatala": 19, 
            "Ayurá": 22, "Envigado": 25, "Itagüí": 28, "Sabaneta": 32, "La Estrella": 37
        }

    def obtener_heuristica(self, actual, destino):
        return abs(self.heuristica_base.get(actual, 0) - self.heuristica_base.get(destino, 0))

    def buscar_mejor_ruta(self, inicio_input, destino_input):
        # Buscar la estación ignorando si se escribió en mayúsculas o minúsculas
        inicio = next((k for k in self.grafo if k.lower() == inicio_input.strip().lower()), None)
        destino = next((k for k in self.grafo if k.lower() == destino_input.strip().lower()), None)

        if not inicio or not destino:
            return "Error: Una de las estaciones ingresadas no existe en la base de conocimiento."

        pq = [(0, 0, inicio, [inicio])]
        visitados = set()

        while pq:
            f, g, actual, camino = heapq.heappop(pq)

            if actual == destino:
                return {"ruta": camino, "tiempo_estimado_minutos": g}

            if actual in visitados:
                continue
            visitados.add(actual)

            for vecino, peso in self.grafo[actual].items():
                if vecino not in visitados:
                    nuevo_g = g + peso
                    nuevo_h = self.obtener_heuristica(vecino, destino)
                    nuevo_f = nuevo_g + nuevo_h
                    heapq.heappush(pq, (nuevo_f, nuevo_g, vecino, camino + [vecino]))

        return "No se encontró una ruta disponible."

# --- Ejecución Interactiva ---
if __name__ == "__main__":
    sistema = SistemaTransporteInteligente()
    
    print("==================================================")
    print("    SISTEMA INTELIGENTE DE TRANSPORTE MASIVO")
    print("==================================================")
    print("Estaciones disponibles:")
    print(", ".join(sistema.grafo.keys()))
    print("--------------------------------------------------")
    
    origen = input("Ingrese la estación de ORIGEN: ")
    destino = input("Ingrese la estación de DESTINO: ")
    
    print(f"\n--- CALCULANDO MEJOR RUTA DE '{origen}' A '{destino}' ---")
    resultado = sistema.buscar_mejor_ruta(origen, destino)
    
    if isinstance(resultado, dict):
        print(f"Ruta óptima encontrada: {' -> '.join(resultado['ruta'])}")
        print(f"Tiempo total estimado: {resultado['tiempo_estimado_minutos']} minutos.")
    else:
        print(resultado)