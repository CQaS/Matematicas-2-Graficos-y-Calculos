import numpy as np
from statistics import mode, multimode
import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
import mysql.connector
from conexion.conexion import get_conexion
console = Console()


console = Console()


def calcular_media():
    console.clear()

    try:

        console.print(
            "\n\n[bold cyan]Cálculo de la Media de Horas Extra Anuales (2025) - Dept. IT(4)[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        id_departamento = 4

        query = f"""
        SELECT e.first_name, e.last_name, AVG(CAST(a.overtime_hours AS FLOAT)) as promedio_individual
        FROM employeess e
        JOIN attendances a ON e.employee_id = a.employee_id
        WHERE e.department_id = {id_departamento} 
          AND a.attendance_year = 2025
        GROUP BY e.first_name, e.last_name
        ORDER BY promedio_individual DESC
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

        if not resultados:
            console.print(
                "[yellow]No se encontraron datos para este departamento en 2025.[/yellow]")
            return

        lista_promedios = []
        paneles = []

        for row in resultados:
            first_name, last_name, promedio_ind = row
            lista_promedios.append(promedio_ind)

            nombre_completo = f"{first_name} {last_name}"

            estilo_borde = "red" if promedio_ind > 15 else "green"

            panel_empleado = Panel(
                f"[bold]{nombre_completo}[/bold]\nPromedio: [cyan]{promedio_ind:.1f} hs/mes[/cyan]",
                border_style=estilo_borde,
                padding=(0, 2),
                width=35
            )
            paneles.append(panel_empleado)

        console.print(
            "[bold yellow]Promedio Mensual Individual por Empleado:[/bold yellow]\n")
        console.print(Columns(paneles, equal=True,
                      expand=True), justify="center")

        texto_valores = ", ".join([f"{v:.1f}" for v in lista_promedios])
        console.print(
            f"\n[bold white]Valores utilizados para el cálculo:[/bold white]")
        console.print(
            f"[italic white]{texto_valores}[/italic white]", justify="center", width=80)

        media_general = np.mean(lista_promedios)

        console.print()
        panel_resultado = Panel(
            f"📊 [bold white]MEDIA DE HORAS EXTRA DEL DEPARTAMENTO[/bold white]\n\n"
            f"[bold yellow]Resultado(MEDIA): {media_general:.2f} horas mensuales[/bold yellow]",
            title="HR Analytics 2025",
            border_style="bright_magenta",
            title_align="center",
            padding=(1, 4)
        )
        console.print(panel_resultado, justify="center")

    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_mediana():
    console.clear()

    try:
        console.print(
            "[bold cyan]Cálculo de la Mediana de Desempeño (2025) - Dept. IT(4)[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        id_departamento = 4

        query = f"""
        SELECT e.first_name, e.last_name, AVG(CAST(p.score AS FLOAT)) as puntaje_anual
        FROM employeess e
        JOIN performances p ON e.employee_id = p.employee_id
        WHERE e.department_id = {id_departamento} 
          AND YEAR(p.evaluation_date) = 2025
        GROUP BY e.first_name, e.last_name
        ORDER BY puntaje_anual ASC  -- Importante ordenar para visualizar la mediana
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            console.print(
                "[yellow]No se encontraron evaluaciones para este departamento en 2025.[/yellow]")
            return

        lista_puntajes = []
        paneles = []
        for row in resultados:
            first_name, last_name, score = row
            lista_puntajes.append(float(score))
            nombre_completo = f"{first_name} {last_name}"

            color_borde = "green" if score >= 80 else "yellow" if score >= 60 else "red"

            panel_empleado = Panel(
                f"Nombre: {nombre_completo}\nScore: [bold]{score:.1f}[/bold]",
                border_style=color_borde,
                padding=(0, 2),
                width=30
            )
            paneles.append(panel_empleado)

        console.print(
            "[bold yellow]Lista de Empleados y su Desempeño Promedio Anual:[/bold yellow]\n")
        console.print(Columns(paneles, equal=True,
                      expand=True), justify="center")

        texto_valores = ", ".join([f"{v:.1f}" for v in lista_puntajes])
        console.print(
            f"\n[bold white]Valores ordenados para el cálculo:[/bold white]")
        console.print(
            f"[italic white]{texto_valores}[/italic white]", justify="center", width=80)

        cursor.close()
        conexion.close()

        mediana = np.median(lista_puntajes)

        console.print()
        panel_resultado = Panel(
            f"📊 [bold white]MEDIANA DE DESEMPEÑO DEL DEPARTAMENTO[/bold white]\n\n"
            f"[bold yellow]Resultado(MEDIANA): {mediana:.1f}[/bold yellow]",
            title="HR Analytics 2025",
            border_style="cyan",
            title_align="center",
            padding=(1, 4)
        )
        console.print(panel_resultado, justify="center")

    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_moda():
    console.clear()

    try:
        console.print(
            "[bold cyan]Cálculo de la Moda de Días de Ausencia (2025) - Dept. ID 4[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        id_departamento = 4

        query = f"""
        SELECT e.first_name, e.last_name, SUM(a.absence_days) as total_faltas
        FROM employeess e
        JOIN attendances a ON e.employee_id = a.employee_id
        WHERE e.department_id = {id_departamento} 
          AND a.attendance_year = 2025
        GROUP BY e.first_name, e.last_name
        ORDER BY total_faltas
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            console.print(
                "[yellow]No se encontraron datos de asistencia para este departamento.[/yellow]")
            return

        lista_faltas = []
        paneles = []

        console.print(
            "[bold yellow]Días de Ausencia Totales por Empleado en 2025:[/bold yellow]\n")

        for row in resultados:
            first_name, last_name, faltas = row
            lista_faltas.append(int(faltas))
            nombre_completo = f"{first_name} {last_name}"

            panel_empleado = Panel(
                f"{nombre_completo}\n[bold]Faltas: {faltas}[/bold]",
                border_style="red" if faltas > 5 else "green",
                width=30
            )
            paneles.append(panel_empleado)

        console.print(Columns(paneles, equal=True,
                      expand=True), justify="center")

        texto_valores = ", ".join([str(f) for f in lista_faltas])
        console.print(f"\n[bold white]Serie de datos analizada:[/bold white]")
        console.print(
            f"[italic white]{texto_valores}[/italic white]", justify="center", width=80)

        cursor.close()
        conexion.close()

        valor_moda = mode(lista_faltas)
        todas_las_modas = multimode(lista_faltas)

        console.print()
        panel_resultado = Panel(
            f"📊 [bold white]ANÁLISIS DE MODA (Frecuencia de Inasistencias)[/bold white]\n\n"
            f"El número de faltas que más se repite es: [bold yellow]{valor_moda} días[/bold yellow]\n"
            f"Modas detectadas: [bold cyan]{', '.join(map(str, todas_las_modas))}[/bold cyan]",
            title="HR Analytics 2025",
            border_style="bright_blue",
            title_align="center",
            padding=(1, 4)
        )
        console.print(panel_resultado, justify="center")

        # Interpretación rápida
        """ if valor_moda == 0:
            console.print(
                "[green]Excelente: La tendencia más común en el equipo es la asistencia perfecta.[/green]", justify="center")
        else:
            console.print(
                f"[yellow]Ojo: La mayoría de los empleados tiende a faltar {valor_moda} días al año.[/yellow]", justify="center")
        """
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_cuartiles():
    console.clear()

    try:
        console.print(
            "[bold cyan]Cálculo de Cuartiles: Índice de Satisfacción Laboral (2025) - Dept. ID 4[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        id_departamento = 4
        query = f"""
        SELECT e.first_name, e.last_name, AVG(CAST(a.satisfaction_score AS FLOAT)) as sat_promedio
        FROM employeess e
        JOIN attendances a ON e.employee_id = a.employee_id
        WHERE e.department_id = {id_departamento} 
          AND a.attendance_year = 2025
        GROUP BY e.first_name, e.last_name
        ORDER BY sat_promedio
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            console.print(
                "[yellow]No se encontraron datos de satisfacción para este periodo.[/yellow]")
            return

        satisfacciones = []
        console.print(
            "[bold yellow]Distribución de Satisfacción por Empleado:[/bold yellow]\n")

        for row in resultados:
            first_name, last_name, sat_score = row
            satisfacciones.append(float(sat_score))
            nombre_completo = f"{first_name} {last_name}"

            color = "red" if sat_score < 5 else "yellow" if sat_score < 8 else "green"
            console.print(
                f"• {nombre_completo:<25} | Satisfacción: [bold {color}]{sat_score:.2f}[/bold {color}]")

        cursor.close()
        conexion.close()

        cuartiles = np.percentile(satisfacciones, [25, 50, 75])

        console.print()
        panel_titulo = Panel(
            "📊 [bold white]ANÁLISIS ESTRATÉGICO DE CUARTILES[/bold white]",
            title="Resultados HR 2025",
            border_style="magenta",
            title_align="center",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")

        # Visualización de los 3 cuartiles
        console.print(Text(
            f"Cuartil C1 (25%): {cuartiles[0]:.2f}", style="bold red on black"), justify="center")
        console.print(Text(
            f"Cuartil C2 (Mediana): {cuartiles[1]:.2f}", style="bold yellow on black"), justify="center")
        console.print(Text(
            f"Cuartil C3 (75%): {cuartiles[2]:.2f}", style="bold green on black"), justify="center")

        # Nota interpretativa
        console.print(
            f"\n[italic white]Interpretación: El 25% de tu equipo tiene una satisfacción menor a {cuartiles[0]:.2f}.[/italic white]", justify="center")

    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


# Medidas de Variabilidad
# Varianza y desviación estándar muestral

def calcular_analisis_dispersion():
    console.clear()

    try:
        console.print(
            "[bold cyan]Reporte Estadístico Integral: Desempeño (2025) - Dept. ID 4[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        id_departamento = 4
        query = f"""
        SELECT e.first_name, e.last_name, AVG(CAST(p.goals_reached_pct AS FLOAT)) as promedio_metas
        FROM employeess e
        JOIN performances p ON e.employee_id = p.employee_id
        WHERE e.department_id = {id_departamento} 
          AND YEAR(p.evaluation_date) = 2025
        GROUP BY e.first_name, e.last_name
        ORDER BY promedio_metas ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

        if not resultados:
            console.print("[yellow]No hay datos disponibles.[/yellow]")
            return

        datos_metas = [float(row[2]) for row in resultados]
        muestra_texto = ", ".join([f"{m:.0f}" for m in datos_metas])

        console.print(Panel(
            f"[bold yellow]Datos analizados (n={len(datos_metas)}):[/bold yellow]\n[italic white][{muestra_texto}][/italic white]",
            title="Muestra", border_style="bright_blue"
        ))

        media = np.mean(datos_metas)
        mediana = np.median(datos_metas)

        datos_redondeados = [int(round(d)) for d in datos_metas]
        modas = multimode(datos_redondeados)

        if len(modas) == 1:
            tipo_moda = "Unimodal"
            resultado_moda = f"{modas[0]}"
        elif len(modas) > 1:
            tipo_moda = f"Multimodal ({len(modas)} valores)"
            resultado_moda = ", ".join([f"{m}" for m in modas])
        else:
            tipo_moda = "N/A"
            resultado_moda = "Sin moda"

        c1, c2, c3 = np.percentile(datos_metas, [25, 50, 75])

        rango = np.max(datos_metas) - np.min(datos_metas)
        iqr = c3 - c1
        varianza = np.var(datos_metas, ddof=1)
        desviacion = np.std(datos_metas, ddof=1)
        cv = (desviacion / media) * 100 if media != 0 else 0

        tabla_stats = Table(
            show_header=True, header_style="bold magenta", border_style="cyan", box=None)
        tabla_stats.add_column("Categoría", style="dim")
        tabla_stats.add_column("Medida", style="bold cyan")
        tabla_stats.add_column("Valor", style="bold yellow", justify="right")
        tabla_stats.add_column("Interpretación", style="italic white")

        tabla_stats.add_row("POSICIÓN", "Media (Promedio)",
                            f"{media:.2f}%", "Centro de gravedad de los datos.")
        tabla_stats.add_row(
            "POSICIÓN", "Mediana", f"{mediana:.2f}%", "El 50% de los empleados supera este valor.")
        tabla_stats.add_row(
            "POSICIÓN", f"Moda ({tipo_moda})", resultado_moda, "Valor o valores de cumplimiento más frecuentes.")
        tabla_stats.add_row("POSICIÓN", "Cuartil C1 / C2 / C3",
                            f"{c1:.1f} / {c2:.1f} / {c3:.1f}", "EL 25%, 50% y 75% de la muestra.")

        tabla_stats.add_section()

        tabla_stats.add_row("DISPERSIÓN", "Rango Total",
                            f"{rango:.2f}%", "Brecha absoluta entre el mejor y el peor.")
        tabla_stats.add_row("DISPERSIÓN", "Rango Intercuartil (IQR)",
                            f"{iqr:.2f}%", "Dispersión del núcleo central (50%).")
        tabla_stats.add_row("DISPERSIÓN", "Varianza",
                            f"{varianza:.2f}", "Dispersión cuadrática media.")
        tabla_stats.add_row("DISPERSIÓN", "Desviación Estándar",
                            f"{desviacion:.2f}%", "Promedio de desvío del rendimiento.")
        tabla_stats.add_row("DISPERSIÓN", "Coef. de Variación",
                            f"{cv:.2f}%", "Nivel de inestabilidad del departamento.")

        console.print(Panel(
            tabla_stats, title="📊 CALCULOS INTEGRALES", border_style="bright_magenta"))

        """
        Genera un gráfico de caja horizontal para visualizar la dispersión
        del cumplimiento de metas.
        """
        try:
            datos = np.array(datos_metas, dtype=float)
            datos = datos[~np.isnan(datos)]  # Eliminar valores nulos (NaN)

            if len(datos) < 2:
                console.print(
                    "[yellow]⚠️ No hay suficientes datos para generar un boxplot significativo.[/yellow]")
                return

            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(12, 6))

            bp = ax.boxplot(datos, vert=False, notch=True, patch_artist=True,
                            whis=1.5,
                            flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 8, 'markeredgecolor': 'black'})

            for box in bp['boxes']:
                box.set(facecolor='#ffea00', edgecolor='purple', linewidth=2)

            for median in bp['medians']:
                median.set(color='purple', linewidth=3)

            for whisker in bp['whiskers']:
                whisker.set(color='purple', linewidth=1.5)
            for cap in bp['caps']:
                cap.set(color='purple', linewidth=2)

            c1, c2, c3 = np.percentile(datos, [25, 50, 75])

            ax.text(c1, 0.6, 'C1',
                    color='purple', ha='center', fontsize=9)
            ax.text(c2, 0.6, 'C2',
                    color='purple', ha='center', fontsize=9)
            ax.text(c3, 0.6, 'C3',
                    color='purple', ha='center', fontsize=9)

            ax.set_title('Análisis de Distribución',
                         fontsize=14, weight='bold', pad=20)
            ax.set_xlabel('Porcentaje (%)', fontsize=11)

            ax.get_yaxis().set_visible(False)

            ax.set_xlim(np.min(datos) - 5, np.max(datos) + 5)

            ax.grid(axis='x', color='gray', linestyle='--', alpha=0.3)

            console.print(
                "\n[bold magenta]Generando visualización detallada de Boxplot...[/bold magenta]")
            plt.tight_layout()
            plt.show()

        except Exception as e:
            console.print(f"[red]Error al generar el Boxplot: {e}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
