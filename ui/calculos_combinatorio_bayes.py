from itertools import combinations, permutations
import math
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.align import Align

console = Console()


""" ARREGLOS: cantidad """


def arreglos_cantidad():
    console.clear()
    n = 5
    k = 3
    arreglos = math.perm(n, k)

    panel = Panel(
        f"[bold cyan]Número de códigos posibles[/bold cyan]: [bold yellow]{arreglos}[/bold yellow]",
        title="[white on blue] Arreglos - Cantidad [/white on blue]",
        expand=False,
    )
    console.print(Align.center(panel))


""" ARREGLOS: listarlas """


def arreglos_listarlas():
    console.clear()
    palabra = "PYTHON"
    k = 4
    permutaciones = list(permutations(palabra, k))

    table = Table(title="Ejemplos de Permutaciones",
                  box=box.ROUNDED, show_lines=True)
    table.add_column("Índice", justify="center", style="cyan", no_wrap=True)
    table.add_column("Permutación", style="magenta")

    for i, p in enumerate(permutaciones[:5], start=1):
        table.add_row(str(i), "".join(p))

    panel = Panel(
        f"[bold cyan]Total de permutaciones[/bold cyan]: [bold yellow]{len(permutaciones)}[/bold yellow]",
        title="[white on blue] Arreglos - Listar [/white on blue]",
        expand=False,
    )

    console.print(Align.center(panel))
    console.print(Align.center(table))


""" COMBINACIONES: cantidad """


def combinaciones_cantidad():
    console.clear()
    n = 10
    k = 3
    combinaciones = math.comb(n, k)

    panel = Panel(
        f"[bold cyan]Número de equipos posibles[/bold cyan]: [bold yellow]{combinaciones}[/bold yellow]",
        title="[white on green] Combinaciones - Cantidad [/white on green]",
        expand=False,
    )
    console.print(Align.center(panel))


""" COMBINACIONES: listarlas """


def combinaciones_listarlas():
    console.clear()
    numeros = range(1, 51)
    k = 5
    combinaciones = list(combinations(numeros, k))

    table = Table(title="Ejemplo de Combinación",
                  box=box.ROUNDED, show_lines=True)
    table.add_column("Índice", justify="center", style="cyan")
    table.add_column("Combinación", style="magenta")
    table.add_row("1", str(combinaciones[0]))

    panel = Panel(
        f"[bold cyan]Total de combinaciones[/bold cyan]: [bold yellow]{len(combinaciones)}[/bold yellow]",
        title="[white on green] Combinaciones - Listar [/white on green]",
        expand=False,
    )

    console.print(Align.center(panel))
    console.print(Align.center(table))


""" Teorema de Bayes """


def teorema_bayes():
    console.clear()
    P_spam = 0.3
    P_no_spam = 1 - P_spam
    P_oferta_spam = 0.8
    P_oferta_no_spam = 0.1

    P_oferta = (P_oferta_spam * P_spam) + (P_oferta_no_spam * P_no_spam)
    P_spam_oferta = (P_oferta_spam * P_spam) / P_oferta

    panel = Panel(
        f"[bold cyan]Probabilidad de que sea spam si contiene 'Oferta'[/bold cyan]: "
        f"[bold yellow]{P_spam_oferta:.2%}[/bold yellow]",
        title="[white on red] Teorema de Bayes [/white on red]",
        expand=False,
    )
    console.print(Align.center(panel))
