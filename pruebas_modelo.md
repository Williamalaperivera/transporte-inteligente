# Informe de Pruebas y Resultados del Modelo Supervisado

## 1. Objetivo de la Prueba
Evaluar la capacidad del algoritmo de **Random Forest Regressor** para aprender de los patrones históricos de viaje y predecir de forma precisa el tiempo de duración de un trayecto considerando factores externos (hora pico y clima).

## 2. Metodología de Validación
- Se utilizó una partición de datos de **80% para entrenamiento** y **20% para pruebas**.
- Se transformaron las variables categóricas de texto mediante codificación numérica (`LabelEncoder`).

## 3. Resultados Obtenidos
- **Coeficiente R² (Score):** El modelo obtuvo una precisión cercana a valores óptimos de generalización, demostrando baja varianza frente a los datos de prueba no vistos.
- **Predicción de Prueba:** Al consultar un trayecto largo en hora pico (`Niquia` a `Poblado`), el modelo predijo coherentemente un tiempo superior a 25 minutos, ajustándose al impacto del tráfico y la distancia.