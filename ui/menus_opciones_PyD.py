from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from ui.calculos_posicionYdispercion import *

console = Console()

opciones_PyD = [
    "Calcular Media",
    "Calcular Mediana",
    "Calcular Moda",
    "Calcular Cuartiles",
    "Calcular Varianza y Desviación Estándar"
]


def mostrar_menu_PyD():
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

    for i, opcion in enumerate(opciones_PyD, 1):
        tabla.add_row(str(i), opcion)

    tabla.add_row("[bold red]0[/bold red]", "[red]Salir del sistema[/red]")

    panel = Panel(tabla, border_style="bright_blue",
                  title="Estadística", subtitle="Selecciona una opción [0-12]")
    console.print(panel, justify="center")  # 👈 centrado en la terminal


def ejecutar_opcion_PyD(eleccion):
    match eleccion:
        case 1:
            calcular_media()
        case 2:
            calcular_mediana()
        case 3:
            calcular_moda()
        case 4:
            calcular_cuartiles()
        case 5:
            calcular_varianza_desviacion()
