from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from ui.calculos_Otros import *

console = Console()
opciones_Otros = [
    "Regresión Lineal Simple",
    "Binomial",
    "Hipergeométrica",
    "Calcular Combinatoria Listarlas",
    "Calcular Teorema de Bayes"
]


def mostrar_menu_Otros():
    console.clear()
    titulo = "[bold cyan]📊 Menú de Combinatoria y Bayes[/bold cyan]"

    tabla = Table(
        title=titulo,
        title_style="bold yellow",
        header_style="bold magenta",
        box=box.ROUNDED,
        show_lines=True
    )
    tabla.add_column("Opción", justify="center", style="bold green")
    tabla.add_column("Cálculo", style="white")

    for i, opcion in enumerate(opciones_Otros, 1):
        tabla.add_row(str(i), opcion)

    tabla.add_row("[bold red]0[/bold red]", "[red]Salir[/red]")

    panel = Panel(tabla, border_style="bright_blue",
                  title="Combinatoria y Bayes", subtitle="Selecciona una opción [0-5]")
    console.print(panel, justify="center")  # 👈 centrado en la terminal


def ejecutar_opcion_Otros(eleccion):
    match eleccion:
        case 1:
            analisis_regresion_salarial()
        case 2:
            analisis_binomial_probabilidad_salarial()
        case 3:
            analisis_hipergeometrica()
