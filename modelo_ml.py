"""
Modelo de Machine Learning para Predicción de Tiempos de Viaje
==============================================================
Este script implementa un pipeline de aprendizaje supervisado utilizando
el algoritmo Random Forest Regressor (Bosques Aleatorios) para estimar
el tiempo real de viaje en el sistema de transporte en función de variables
como origen, destino, distancia, hora pico y condiciones climáticas.

Incluye visualización de resultados estilo Dashboard / Excel en consola
utilizando la librería 'rich'.
"""

# Configuración de codificación para compatibilidad en terminales Windows
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Importación de librerías para ciencia de datos y machine learning
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Importación de librerías para visualización estética en la terminal (estilo Excel)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich import box
    TIENE_RICH = True
    console = Console(force_terminal=True)
except ImportError:
    TIENE_RICH = False

# ==============================================================================
# 1. CARGA Y PREPROCESAMIENTO DE DATOS
# ==============================================================================
print("=== 1. CARGANDO Y PREPROCESANDO EL DATASET ===")

# Carga del archivo CSV con los registros históricos de viajes
df = pd.read_csv("transporte_dataset.csv")

# Los modelos de Machine Learning requieren datos numéricos.
# Usamos LabelEncoder para transformar los nombres de estaciones (texto) a números enteros.
le_origen = LabelEncoder()
le_destino = LabelEncoder()

# Ajustar y transformar las columnas 'origen' y 'destino'
df['origen_cod'] = le_origen.fit_transform(df['origen'])
df['destino_cod'] = le_destino.fit_transform(df['destino'])

# Definición de las variables predictoras (X) o características (features)
# Incluye: origen codificado, destino codificado, distancia, si es hora pico (1/0) y lluvia (1/0)
X = df[['origen_cod', 'destino_cod', 'distancia_km', 'hora_pico', 'clima_lluvioso']]

# Definición de la variable objetivo (y): lo que queremos predecir (tiempo real en minutos)
y = df['tiempo_real_minutos']

print(f"Total de registros cargados: {len(df)}")

# ==============================================================================
# 2. PARTICIÓN DE DATOS (ENTRENAMIENTO Y EVALUACIÓN)
# ==============================================================================
print("\n=== 2. DIVIDIENDO DATOS (ENTRENAMIENTO Y PRUEBA) ===")

# Se separa el 80% de los datos para entrenar el modelo y el 20% para probar su desempeño.
# random_state=42 asegura que la división sea reproducible cada vez que se ejecute.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================================================================
# 3. ENTRENAMIENTO DEL MODELO (RANDOM FOREST REGRESSOR)
# ==============================================================================
print("\n=== 3. ENTRENANDO EL MODELO DE APRENDIZAJE SUPERVISADO ===")

# Creamos el modelo de regresión con un bosque de 100 árboles de decisión
modelo = RandomForestRegressor(n_estimators=100, random_state=42)

# Entrenamos el modelo ajustando los árboles a los datos de entrenamiento
modelo.fit(X_train, y_train)
print("¡Modelo entrenado exitosamente!")

# ==============================================================================
# 4. EVALUACIÓN DE DESEMPEÑO DEL MODELO
# ==============================================================================
print("\n=== 4. EVALUANDO EL MODELO ===")

# Realizamos las predicciones sobre el conjunto de prueba (datos que el modelo no ha visto)
y_pred = modelo.predict(X_test)

# Métrica 1: Error Cuadrático Medio (MSE) - mide la magnitud promedio del error al cuadrado
mse = mean_squared_error(y_test, y_pred)

# Métrica 2: Coeficiente de Determinación (R²) - indica qué porcentaje de la varianza
# de los tiempos de viaje es explicada por el modelo (más cercano a 1.0 es mejor)
r2 = r2_score(y_test, y_pred)

print(f"Error Cuadrático Medio (MSE): {mse:.2f}")
print(f"Coeficiente de Determinación (R^2 Score): {r2:.2f}")

# ==============================================================================
# 5. VISUALIZACIÓN GRÁFICA COMPARATIVA (ESTILO EXCEL DASHBOARD)
# ==============================================================================
print("\n=== 5. GRÁFICA COMPARATIVA EN LA TERMINAL (TIEMPO REAL VS PREDICCIÓN) ===")

if TIENE_RICH:
    # --- Tarjetas KPI de Resumen Ejecutivo ---
    kpi_mse = Panel(
        f"[bold white]{mse:.2f}[/]\n[dim]minutos²[/]", 
        title="[bold cyan]📉 Error MSE[/]", 
        border_style="cyan"
    )
    kpi_r2 = Panel(
        f"[bold green]{r2:.2f}[/]\n[dim]({r2 * 100:.1f}% precisión)[/]", 
        title="[bold green]🎯 R² Score[/]", 
        border_style="green"
    )
    kpi_samples = Panel(
        f"[bold white]{len(y_test)} casos[/]\n[dim]20% test set[/]", 
        title="[bold yellow]📋 Muestras Test[/]", 
        border_style="yellow"
    )
    console.print(Columns([kpi_mse, kpi_r2, kpi_samples]))

    # --- Tabla Estilo Hoja de Cálculo Excel con Gráfico de Barras Agrupadas ---
    tabla_excel = Table(
        title="[bold white]DASHBOARD DE COMPARACIÓN: TIEMPO REAL VS PREDICCIÓN IA[/bold white]\n[dim]Gráfico de barras dobles comparativas por muestra de prueba[/dim]",
        box=box.ROUNDED,
        header_style="bold white on blue",
        title_justify="center"
    )

    tabla_excel.add_column("Muestra", justify="center", style="bold")
    tabla_excel.add_column("Tiempo Real", justify="right", style="bold cyan")
    tabla_excel.add_column("Predicción IA", justify="right", style="bold green")
    tabla_excel.add_column("Desviación", justify="right")
    tabla_excel.add_column("Gráfico Comparativo de Barras", justify="left", min_width=38)

    # Escala para ajustar la longitud visual de las barras a un máximo de 20 caracteres
    max_val = max(max(y_test), max(y_pred)) if len(y_test) > 0 else 1
    escala = 20.0 / max_val

    for i, (real, pred) in enumerate(zip(y_test, y_pred)):
        desviacion = pred - real
        # Color del error: verde si la diferencia es mínima (< 1 min), amarillo si es mayor
        color_desv = "[green]" if abs(desviacion) < 1.0 else "[yellow]"
        texto_desv = f"{color_desv}{desviacion:+.2f} min[/]"

        # Barras visuales estilo Excel (■ Real en Azul / ■ IA en Verde)
        len_real = max(1, int(round(real * escala)))
        len_pred = max(1, int(round(pred * escala)))
        
        barra_real = f"[cyan]{'█' * len_real}[/] [dim]{real:.1f}m[/]"
        barra_pred = f"[green]{'█' * len_pred}[/] [dim]{pred:.1f}m[/]"
        grafico_doble = f"Real: {barra_real}\nIA:   {barra_pred}"

        tabla_excel.add_row(
            f"Prueba {i+1}", 
            f"{real:5.1f} min", 
            f"{pred:5.1f} min", 
            texto_desv, 
            grafico_doble
        )

    console.print(tabla_excel)
    console.print("  [dim]Leyenda: [cyan]█ Tiempo Real[/]  |  [green]█ Predicción IA[/][/dim]\n")

else:
    # Visualizador clásico en texto plano (en caso de no contar con la librería rich)
    print("-" * 65)
    print(f"{'Muestra':<10} | {'Tiempo Real':<15} | {'Predicción IA':<15} | {'Visualizador':<15}")
    print("-" * 65)
    for i, (real, pred) in enumerate(zip(y_test, y_pred)):
        barra_real = "■" * int(round(real))
        print(f"Prueba {i+1:<3} | {real:11.1f} min | {pred:13.1f} min | {barra_real}")
    print("-" * 65)

# ==============================================================================
# 6. INFERENCIA CON UN NUEVO CASO DE PRUEBA
# ==============================================================================
print("=== 6. PREDICCIÓN DE EJEMPLO NUEVO ===")

# Convertimos los nombres de las estaciones al código numérico que conoce el modelo
origen_prueba = le_origen.transform(['Niquia'])[0]
destino_prueba = le_destino.transform(['Poblado'])[0]

# Creamos un nuevo registro con las mismas columnas que usamos para entrenar:
# [origen, destino, distancia=14.5km, hora_pico=1 (Sí), clima_lluvioso=0 (No)]
nuevo_viaje = pd.DataFrame(
    [[origen_prueba, destino_prueba, 14.5, 1, 0]], 
    columns=['origen_cod', 'destino_cod', 'distancia_km', 'hora_pico', 'clima_lluvioso']
)

# El modelo calcula y predice el tiempo estimado del nuevo viaje
tiempo_predicho = modelo.predict(nuevo_viaje)

if TIENE_RICH:
    panel_prediccion = Panel(
        f"[bold white]Trayecto simulado:[/] [cyan]Niquia -> Poblado[/] (Hora Pico: [red]Sí[/], Clima Lluvioso: [blue]No[/])\n"
        f"[bold white]Tiempo estimado predicho por la IA:[/] [bold green]{tiempo_predicho[0]:.2f} minutos[/]",
        title="[bold green]🚀 Resultado de Simulación en Tiempo Real[/]",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(panel_prediccion)
else:
    print(f"Trayecto simulado: Niquia -> Poblado en Hora Pico")
    print(f"Tiempo estimado predicho por la IA: {tiempo_predicho[0]:.2f} minutos.")