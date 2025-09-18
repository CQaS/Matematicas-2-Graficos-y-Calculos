import statistics as stat
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
console = Console()


def calcular_media():
    console.clear()
    # Muestra de datos (ejemplo: edades en años)
    datos = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 25, 30, 35, 40]
    media = np.mean(datos)

    panel_titulo = Panel(
        "📊 Cálculo de la Media",
        title="Resultados",
        border_style="cyan",
        title_align="left",
        padding=(1, 4)
    )
    console.print(panel_titulo, justify="center")
    texto_resultado = Text(f"Media: {media:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")


def calcular_mediana():
    console.clear()

    # Muestra de datos (ejemplo: edades en años)

    datos = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 25, 30, 35, 40]

    # Cálculo de estadísticos

    mediana = np.median(datos)

    panel_titulo = Panel(
        "📊 Cálculo de la Mediana",
        title="Resultados",
        border_style="cyan",
        title_align="left",
        padding=(1, 4)
    )
    console.print(panel_titulo, justify="center")
    texto_resultado = Text(f"Mediana: {mediana:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

def calcular_moda():
    console.clear()

    # Muestra de datos (ejemplo: edades en años)

    datos = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 70, 75, 80, 25, 30, 35, 40]

    # Cálculo de estadísticos

    moda = stat.mode(datos)  # devuelve una de las modas

    modas = stat.multimode(datos)  # devuelve un arreglo con todas

    panel_titulo = Panel(
        "📊 Cálculo de la Mediana",
        title="Resultados",
        border_style="cyan",
        title_align="left",
        padding=(1, 4)
    )
    console.print(panel_titulo, justify="center")
    texto_resultado = Text(
        f"Moda: {moda:.2f}. Modas: {', '.join(map(str, modas))}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

def calcular_cuartiles():
    console.clear()
    # Muestra de datos (ejemplo: edades en años)

    datos = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 25, 30, 35, 40]

    # Cálculo de estadísticos

    cuartiles = np.percentile(datos, [25, 50, 75])  # Q1, Q2 (mediana), Q3

    panel_titulo = Panel(
        "📊 Cálculo de la Mediana",
        title="Resultados",
        border_style="cyan",
        title_align="left",
        padding=(1, 4)
    )
    console.print(panel_titulo, justify="center")
    texto_resultado = Text(
        f"Cuartil Q1: {cuartiles[0]:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

    texto_resultado = Text(
        f"Cuartil Q2: {cuartiles[1]:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

    texto_resultado = Text(
        f"Cuartil Q3: {cuartiles[2]:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

#Medidas de Variabilidad
#Varianza y desviación estándar muestral

def calcular_varianza_desviacion():
    console.clear()

    # Muestra de datos (ejemplo: pesos en kg de un grupo de personas)

    datos = [62, 65, 68, 70, 72, 74, 75, 78, 80, 85]

    # Calcular

    varianza_np = np.var(datos, ddof=1)  # ddof=1 para varianza muestral

    desviacion_np = np.std(datos, ddof=1)

    # Resultados

    panel_titulo = Panel(
        "📊 Cálculo de la Varianza y Desviación Estándar",
        title="Resultados",
        border_style="cyan",
        title_align="left",
        padding=(1, 4)
    )
    console.print(panel_titulo, justify="center")
    texto_resultado = Text(
        f"Varianza: {varianza_np:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")

    texto_resultado = Text(
        f"Desviación estándar: {desviacion_np:.2f}", style="bold yellow on black")
    console.print(texto_resultado, justify="center")
