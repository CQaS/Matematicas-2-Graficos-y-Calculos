import numpy as np
from statistics import mode, multimode
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import mysql.connector
from conexion.conexion import get_conexion
console = Console()


def calcular_media():
    console.clear()

    try:
        console.print(
            "[bold cyan]Cálculo de la Media de Salarios del Departamento 80 (Sales)[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        query = """
        SELECT e.first_name, e.last_name, e.salary
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.salary IS NOT NULL
        ORDER BY e.salary
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Extraer salarios y mostrar datos de empleados
        salarios = []
        paneles = []
        for row in resultados:
            first_name, last_name, salary = row
            salarios.append(float(salary))
            nombre_completo = f"{first_name} {last_name}"
            panel_empleado = Panel(
                f"Nombre: {nombre_completo}\nSalario: {salary:.2f} USD",
                border_style="yellow",
                padding=(0, 2),
                width=30  # Ancho fijo para alinear tarjetas
            )
            paneles.append(panel_empleado)

        # Mostrar paneles en columnas (tarjetas una al lado de la otra)
        console.print(
            "[bold yellow]Lista de Empleados y Salarios:[/bold yellow]\n")
        console.print(Columns(paneles, equal=True,
                      expand=True), justify="center")

        cursor.close()
        conexion.close()

        media = np.mean(salarios)

        console.print()
        panel_titulo = Panel(
            "📊 Cálculo de la Media de Salarios (Sales)",
            title="Resultados",
            border_style="cyan",
            title_align="left",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")
        texto_resultado = Text(
            f"Media: {media:.2f} USD", style="bold yellow on black")
        console.print(texto_resultado, justify="center")

    except mysql.connector.Error as err:
        console.print(
            f"[red]Error al conectar con la base de datos: {err}[/red]")
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_mediana():
    console.clear()

    try:
        # Mostrar mensaje inicial
        console.print(
            "[bold cyan]Cálculo de la Mediana de Salarios del Departamento 80 (Sales)[/bold cyan]\n")

        # Establecer conexión a la base de datos
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Consulta para obtener nombres y salarios del departamento Sales
        query = """
        SELECT e.first_name, e.last_name, e.salary
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.salary IS NOT NULL
        ORDER BY e.salary
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Extraer salarios y preparar paneles para columnas
        salarios = []
        paneles = []
        for row in resultados:
            first_name, last_name, salary = row
            salarios.append(float(salary))
            nombre_completo = f"{first_name} {last_name}"
            panel_empleado = Panel(
                f"Nombre: {nombre_completo}\nSalario: {salary:.2f} USD",
                border_style="yellow",
                padding=(0, 2),
                width=30  # Ancho fijo para alinear tarjetas
            )
            paneles.append(panel_empleado)

        # Mostrar paneles en columnas (tarjetas una al lado de la otra)
        console.print(
            "[bold yellow]Lista de Empleados y Salarios:[/bold yellow]\n")
        console.print(Columns(paneles, equal=True,
                      expand=True), justify="center")

        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

        # Calcular la mediana
        mediana = np.median(salarios)

        # Mostrar resultados con rich
        console.print()  # Espacio para separar
        panel_titulo = Panel(
            "📊 Cálculo de la Mediana de Salarios (Sales)",
            title="Resultados",
            border_style="cyan",
            title_align="left",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")
        texto_resultado = Text(
            f"Mediana: {mediana:.2f} USD", style="bold yellow on black")
        console.print(texto_resultado, justify="center")

    except mysql.connector.Error as err:
        console.print(
            f"[red]Error al conectar con la base de datos: {err}[/red]")
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_moda():
    console.clear()

    try:
        # Mostrar mensaje inicial
        console.print(
            "[bold cyan]Cálculo de la Moda de Salarios del Departamento 80 (Sales)[/bold cyan]\n")

        # Establecer conexión a la base de datos
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Consulta para obtener nombres y salarios del departamento Sales
        query = """
        SELECT e.first_name, e.last_name, e.salary
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.salary IS NOT NULL
        ORDER BY e.salary
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Extraer salarios y mostrar datos de empleados
        salarios = []
        console.print(
            "[bold yellow]Lista de Empleados y Salarios:[/bold yellow]\n")
        for row in resultados:
            first_name, last_name, salary = row
            salarios.append(float(salary))
            nombre_completo = f"{first_name} {last_name}"
            console.print(
                f"Nombre: {nombre_completo}, Salario: {salary:.2f} USD", style="yellow")

        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

        # Calcular la moda
        moda = mode(salarios)  # Devuelve una de las modas
        modas = multimode(salarios)  # Devuelve todas las modas

        # Mostrar resultados con rich
        console.print()  # Espacio para separar
        panel_titulo = Panel(
            "📊 Cálculo de la Moda de Salarios (Sales)",
            title="Resultados",
            border_style="cyan",
            title_align="left",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")
        texto_resultado = Text(
            f"Moda: {moda:.2f}. Modas: {', '.join(f'{m:.2f}' for m in modas)} USD",
            style="bold yellow on black"
        )
        console.print(texto_resultado, justify="center")

    except mysql.connector.Error as err:
        console.print(
            f"[red]Error al conectar con la base de datos: {err}[/red]")
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")


def calcular_cuartiles():
    console.clear()
    console.clear()

    try:
        console.print(
            "[bold cyan]Cálculo de los Cuartiles de Porcentajes de Comisión del Departamento 80 (Sales)[/bold cyan]\n")

        conexion = get_conexion()
        cursor = conexion.cursor()

        # Consulta para obtener nombres y commission_pct del departamento Sales
        query = """
        SELECT e.first_name, e.last_name, e.commission_pct
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.commission_pct IS NOT NULL
        ORDER BY e.commission_pct
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Extraer commission_pct y mostrar datos de empleados
        comisiones = []
        console.print(
            "[bold yellow]Lista de Empleados y Porcentajes de Comisión:[/bold yellow]\n")
        for row in resultados:
            first_name, last_name, commission_pct = row
            comisiones.append(float(commission_pct))
            nombre_completo = f"{first_name} {last_name}"
            console.print(
                f"Nombre: {nombre_completo}, Comisión: {commission_pct:.2f}", style="yellow")

        cursor.close()
        conexion.close()

        cuartiles = np.percentile(
            comisiones, [25, 50, 75])  # Q1, Q2 (mediana), Q3

        console.print()
        panel_titulo = Panel(
            "📊 Cálculo de los Cuartiles de Porcentajes de Comisión (Sales)",
            title="Resultados",
            border_style="cyan",
            title_align="left",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")
        texto_resultado_q1 = Text(
            f"Cuartil Q1: {cuartiles[0]:.2f}", style="bold yellow on black")
        console.print(texto_resultado_q1, justify="center")
        texto_resultado_q2 = Text(
            f"Cuartil Q2 (Mediana): {cuartiles[1]:.2f}", style="bold yellow on black")
        console.print(texto_resultado_q2, justify="center")
        texto_resultado_q3 = Text(
            f"Cuartil Q3: {cuartiles[2]:.2f}", style="bold yellow on black")
        console.print(texto_resultado_q3, justify="center")

    except mysql.connector.Error as err:
        console.print(
            f"[red]Error al conectar con la base de datos: {err}[/red]")
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")

# Medidas de Variabilidad
# Varianza y desviación estándar muestral


def calcular_varianza_desviacion():
    console.clear()

    console.clear()

    try:
        # Mostrar mensaje inicial
        console.print(
            "[bold cyan]Cálculo de la Varianza y Desviación Estándar de Porcentajes de Comisión del Departamento 80 (Sales)[/bold cyan]\n")

        # Establecer conexión a la base de datos
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Consulta para obtener nombres y commission_pct del departamento Sales
        query = """
        SELECT e.first_name, e.last_name, e.commission_pct
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.commission_pct IS NOT NULL
        ORDER BY e.commission_pct
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Extraer commission_pct y mostrar datos de empleados
        comisiones = []
        console.print(
            "[bold yellow]Lista de Empleados y Porcentajes de Comisión:[/bold yellow]\n")
        for row in resultados:
            first_name, last_name, commission_pct = row
            comisiones.append(float(commission_pct))
            nombre_completo = f"{first_name} {last_name}"
            console.print(
                f"Nombre: {nombre_completo}, Comisión: {commission_pct:.2f}", style="yellow")

        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

        # Calcular varianza y desviación estándar muestral
        # ddof=1 para varianza muestral
        varianza_np = np.var(comisiones, ddof=1)
        # ddof=1 para desviación muestral
        desviacion_np = np.std(comisiones, ddof=1)

        # Mostrar resultados con rich
        console.print()  # Espacio para separar
        panel_titulo = Panel(
            "📊 Cálculo de la Varianza y Desviación Estándar de Porcentajes de Comisión (Sales)",
            title="Resultados",
            border_style="cyan",
            title_align="left",
            padding=(1, 4)
        )
        console.print(panel_titulo, justify="center")
        texto_resultado_varianza = Text(
            f"Varianza: {varianza_np:.2f}", style="bold yellow on black")
        console.print(texto_resultado_varianza, justify="center")
        texto_resultado_desviacion = Text(
            f"Desviación Estándar: {desviacion_np:.2f}", style="bold yellow on black")
        console.print(texto_resultado_desviacion, justify="center")

    except mysql.connector.Error as err:
        console.print(
            f"[red]Error al conectar con la base de datos: {err}[/red]")
    except Exception as e:
        console.print(f"[red]Ocurrió un error: {e}[/red]")
