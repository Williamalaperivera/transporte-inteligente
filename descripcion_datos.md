# Descripción del Dataset - Sistema de Transporte Masivo IA

## 1. Contexto y Fuente de Datos
Debido a la ausencia de una API abierta pública con registros masivos históricos en tiempo real para las rutas locales de transporte masivo, se diseñó y estructuró una **muestra sintética de datos históricos** basada en las estaciones reales del sistema.

## 2. Estructura de las Variables (Features)
El dataset cuenta con los siguientes atributos o columnas:
- **origen**: Estación de partida del trayecto (Variable categórica).
- **destino**: Estación de llegada del trayecto (Variable categórica).
- **distancia_km**: Distancia lineal aproximada entre las estaciones en kilómetros (Variable numérica continua).
- **hora_pico**: Indicador binario (1 si el viaje ocurre en hora de alta congestión, 0 en hora valle).
- **clima_lluvioso**: Indicador binario (1 si hay lluvia afectando la velocidad de circulación, 0 si las condiciones son normales).
- **tiempo_real_minutos**: Variable objetivo (*Target*) que representa el tiempo real registrado que toma completar el trayecto.