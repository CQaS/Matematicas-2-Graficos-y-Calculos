from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from ui.graficos1 import *

console = Console()

opciones = [
    "Gráfico Sectores (Pie Chart)",
    "Gráfico de Barras",
    "Diagrama de Pareto",
    "Gráfico de Tallo y Hoja",
    "Gráfico de Puntos (Dot Plot)",
    "Gráfico de Bastón",
    "Histograma con rangos de valores",
    "Histograma con valores discretos",
    "Gráfico de Líneas (Un Grupo)",
    "Gráfico de Líneas (Evolucion de contrataciones)",
    "Boxplot (Diagrama de Cajas)",
    "Gráfico de Dispersión (Scatter)"
]


def mostrar_menu():
    console.clear()
    titulo = "[bold cyan]📊 Menú de Gráficos Estadísticos[/bold cyan]"

    tabla = Table(
        title=titulo,
        title_style="bold yellow",
        header_style="bold magenta",
        box=box.ROUNDED,
        show_lines=True
    )
    tabla.add_column("Opción", justify="center", style="bold green")
    tabla.add_column("Gráfico", style="white")

    for i, opcion in enumerate(opciones, 1):
        tabla.add_row(str(i), opcion)

    tabla.add_row("[bold red]0[/bold red]", "[red]Volver atras[/red]")

    panel = Panel(tabla, border_style="bright_blue",
                  title="Estadística", subtitle="Selecciona una opción [0-{}]".format(len(opciones)))
    console.print(panel, justify="center")  # 👈 centrado en la terminal


def ejecutar_opcion(eleccion):
    match eleccion:
        case 1:

            grafico_pastel()
        case 2:

            grafico_barras()
        case 3:

            diagrama_pareto()
        case 4:

            grafico_tallo_y_hoja_porEdad()
        case 5:

            grafico_puntos()
        case 6:

            grafico_baston()
        case 7:

            grafico_histograma_rangos()
        case 8:

            grafico_histograma_discretos()
        case 9:

            grafico_lineas_un_grupo()
        case 10:

            grafico_evolucion_contrataciones()
        case 11:

            grafico_boxplot()
        case 12:

            grafico_dispersion()
