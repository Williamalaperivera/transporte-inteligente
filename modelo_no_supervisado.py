import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("=== 1. CARGANDO Y PREPARANDO LOS DATOS PARA CLUSTERING ===")
df = pd.read_csv("transporte_clustering_dataset.csv")
print(df.head())

# Seleccionamos las variables numéricas para agrupar (excluimos el nombre de la estación)
X = df[['tiempo_espera_promedio_min', 'afluencia_pasajeros_diaria', 'distancia_promedio_km']]

print("\n=== 2. ESCALANDO LOS DATOS ===")
# El clustering por distancia requiere normalizar las escalas de las variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\n=== 3. APLICANDO EL ALGORITMO K-MEANS (APRENDIZAJE NO SUPERVISADO) ===")
# Agruparemos las estaciones en 3 clústeres (ej: Alta, Media y Baja congestión/demanda)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

print("¡Agrupamiento completado exitosamente!")

print("\n=== 4. RESULTADOS DE LOS GRUPOS (CLÚSTERES) ASIGNADOS ===")
print(df[['estacion', 'afluencia_pasajeros_diaria', 'cluster']])

print("\n=== 5. REPRESENTACIÓN VISUAL EN LA TERMINAL ===")
print("-" * 75)
print(f"{'Estación':<15} | {'Pasajeros/Día':<15} | {'Espera (min)':<15} | {'Clúster Asignado'}")
print("-" * 75)

for index, row in df.iterrows():
    # Creamos un indicador visual según el clúster
    indicador = "🔴 Grupo Alto" if row['cluster'] == 2 else ("🟡 Grupo Medio" if row['cluster'] == 1 else "🟢 Grupo Bajo")
    print(f"{row['estacion']:<15} | {row['afluencia_pasajeros_diaria']:<15} | {row['tiempo_espera_promedio_min']:<15} | {indicador}")

print("-" * 75)
print("\n¡El modelo no supervisado ha agrupado automáticamente las estaciones sin intervención humana previa!")