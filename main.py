from rich.prompt import Prompt
from ui.menus_opciones import *
from ui.graficos1 import *
from ui.menus_opciones_PyD import *
from ui.calculos_posicionYdispercion import *

op = [
    "Gráfico Estadístico (Pie Chart, Barras, Puntos, Bastón, Histogramas, Líneas, Boxplot, Scatter)",
    "Calculos Estadísticos (Media, Mediana, Moda, Cuartiles, Varianza y Desviación Estándar)",
]

if __name__ == "__main__":
    while True:
        console.clear()
        titulo = "[bold cyan]📊 Menú de Gráficos y Calculos Estadísticos[/bold cyan]"

        tabla = Table(
            title=titulo,
            title_style="bold yellow",
            header_style="bold magenta",
            box=box.ROUNDED,
            show_lines=True
        )
        tabla.add_column("Opción", justify="center", style="bold green")
        tabla.add_column("Gráfico y Calculos", style="white")

        for i, opcion in enumerate(op, 1):
            tabla.add_row(str(i), opcion)

        tabla.add_row("[bold red]0[/bold red]", "[red]Salir del sistema[/red]")

        panel = Panel(tabla, border_style="bright_blue",
                    title="Estadística", subtitle="Selecciona una opción [0-12]")
        console.print(panel, justify="center")  # 👈 centrado en la terminal
        queVer = int(Prompt.ask(
            "[bold yellow]Ingrese una opción[/bold yellow]"))
        
        if queVer == 1:
            while True:
                mostrar_menu()
                try:
                    eleccion = int(Prompt.ask(
                        "[bold yellow]Ingrese una opción[/bold yellow]"))

                    if 1 <= eleccion <= len(opciones):
                        console.print(
                            f"\n[green]✔ Has elegido:[/green] [bold cyan]{opciones[eleccion - 1]}[/bold cyan]\n", justify="center")
                        input("Presiona ENTER para Ejecutar Gráfico...")
                        ejecutar_opcion(eleccion)

                    elif eleccion == 0:
                        console.print(
                            "\n[bold red]Saliendo del sistema. ¡Hasta luego! ⏩[/bold red]\n", justify="center")
                        break
                    else:
                        console.print(
                            "[red]\n⚠ Opción no válida. Intente de nuevo.[/red]\n", justify="center")
                        input("Presiona ENTER para continuar...")

                except ValueError:
                    console.print(
                        "[red]\n⚠ Entrada inválida. Ingrese un número.[/red]\n")
                    input("Presiona ENTER para continuar...")

        elif queVer == 2:
            while True:
                mostrar_menu_PyD()
                try:
                    eleccion = int(Prompt.ask(
                        "[bold yellow]Ingrese una opción[/bold yellow]"))

                    if 1 <= eleccion <= len(opciones_PyD):
                        console.print(
                            f"\n[green]✔ Has elegido:[/green] [bold cyan]{opciones_PyD[eleccion - 1]}[/bold cyan]\n", justify="center")
                        input("Presiona ENTER para Ejecutar Cálculo...")
                        ejecutar_opcion_PyD(eleccion)
                        input("\nPresiona ENTER para continuar...\n")

                    elif eleccion == 0:
                        console.print(
                            "\n[bold red]Saliendo del sistema. ¡Hasta luego! ⏩[/bold red]\n", justify="center")
                        break
                    else:
                        console.print(
                            "[red]\n⚠ Opción no válida. Intente de nuevo.[/red]\n", justify="center")
                        input("Presiona ENTER para continuar...")

                except ValueError:
                    console.print(
                        "[red]\n⚠ Entrada inválida. Ingrese un número.[/red]\n")
                    input("Presiona ENTER para continuar...")

        elif eleccion == 0:
            console.print(
                "\n[bold red]Saliendo del sistema. ¡Hasta luego! ⏩[/bold red]\n", justify="center")
            break

        elif queVer < 0  or queVer > 2:
            console.print(
                "[red]\n⚠ Opción no válida. Intente de nuevo.[/red]\n", justify="center")
            input("Presiona ENTER para continuar...")
