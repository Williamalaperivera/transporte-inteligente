# Informe de Pruebas y Resultados del Modelo No Supervisado (K-Means)

## 1. Objetivo de la Prueba
Agrupar automáticamente las estaciones del sistema de transporte masivo en 3 categorías operativas (baja, media y alta afluencia/congestión) utilizando el algoritmo de agrupamiento **K-Means** basado en características numéricas escaladas.

## 2. Metodología Aplicada
- Se aplicó un escalado de características (`StandardScaler`) para evitar que variables con números grandes (como la afluencia de pasajeros) sesgaran el cálculo de distancias del algoritmo frente a valores pequeños (como los minutos de espera).
- Se configuró el modelo K-Means con $K=3$ centroides.

## 3. Resultados Obtenidos
- El modelo clasificó de forma coherente las estaciones críticas (como *San Antonio* o *Acevedo*) en el grupo de alta exigencia operativa.
- Las estaciones intermedias y de menor flujo fueron segmentadas exitosamente en los otros dos clústeres, demostrando la eficacia del aprendizaje no supervisado para la segmentación urbana.