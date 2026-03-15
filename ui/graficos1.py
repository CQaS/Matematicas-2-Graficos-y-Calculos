
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import PercentFormatter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from calendar import month_abbr, month_name
from conexion.conexion import get_conexion

consola = Console()


# Imprime la guía de los gráficos

def printGuia(titulo, guia):
    consola.print(Panel(
        f"[bold yellow]{titulo}[/bold yellow]", expand=False))

    # --- EXPLICACIÓN DESTACADA DEL GRÁFICO ---
    explicacion_texto = (
        "[bold]¿Qué estamos analizando?[/bold]\n\n"
        f"{guia}\n\n"
    )

    consola.print(Panel(explicacion_texto,
                  title="[bold white]Guía de Graficos/Tablas[/bold white]", border_style="bright_blue", expand=False))

    consola.print(
        "\n[bold blink]Sugerencia:[/bold blink] Cierra la ventana del gráfico para continuar con el programa.\n\n")

# Gráfico de sectores(Pie chart) - pastel o torta
# Genera un gráfico circular que muestra la distribución del gasto
# total en salarios por cada departamento de la base de datos HR.


def grafico_pastel():

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT d.department_name, SUM(e.salary) as total_gasto
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY total_gasto DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not resultados:
        consola.print("[yellow]No hay datos disponibles.[/yellow]")
        return

    departamentos = [fila[0] for fila in resultados]
    montos = [float(fila[1]) for fila in resultados]
    total_general = sum(montos)

    tabla = Table(title="Análisis de Frecuencias: Distribución Salarial",
                  header_style="bold magenta")
    tabla.add_column("Departamento", style="cyan", no_wrap=True)
    tabla.add_column("Frec. Absoluta (USD)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Frec. Abs. Acum.", justify="right", style="blue")
    tabla.add_column("Frec. Rel. Acum.", justify="right", style="blue")

    frec_abs_acumulada = 0
    frec_rel_acumulada = 0

    for dep, monto in zip(departamentos, montos):
        porcentaje = (monto / total_general) * 100
        frec_abs_acumulada += monto
        frec_rel_acumulada += porcentaje

        tabla.add_row(
            dep,
            f"{monto:,.2f}",
            f"{porcentaje:.2f}%",
            f"{frec_abs_acumulada:,.2f}",
            f"{frec_rel_acumulada:.2f}%"
        )

    consola.clear()

    titulo = "GRAFICO DE PASTEL: DISTRIBUCIÓN DE GASTOS POR DEPARTAMENTO"
    guia = "El gráfico de pastel muestra el gasto salarial acumulado por departamento, mostrando la proporción de gasto respecto al total."

    printGuia(titulo, guia)

    consola.print(tabla)

    colores = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(
        len(departamentos))]

    plt.figure(figsize=(12, 7))

    patches, texts, autotexts = plt.pie(
        montos,
        autopct='%1.1f%%',
        startangle=140,
        colors=colores,
        pctdistance=0.85,
        textprops={'color': "w", 'weight': 'bold', 'fontsize': 9}
    )

    plt.legend(
        patches,
        departamentos,
        title="Departamentos",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=9
    )

    plt.title('Distribución de Carga Salarial - 2026', fontsize=14, pad=20)
    plt.axis('equal')

    consola.print(
        "\n[bold magenta]Generando gráfico de pastel...[/bold magenta]")
    plt.tight_layout()
    plt.show()


# Gráfico de barras
# Genera un gráfico de barras comparativo que muestra el salario
# promedio real por departamento, ordenado de mayor a menor.


def grafico_barras():

    conexion = get_conexion()
    cursor = conexion.cursor()

    query = """
        SELECT d.department_name, ROUND(AVG(e.salary), 2) AS salario_promedio
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY salario_promedio DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not resultados:
        consola.print(
            "[yellow]No hay datos disponibles para el análisis salarial.[/yellow]")
        return

    nombres_deptos = [fila[0] for fila in resultados]
    promedios = [float(fila[1]) for fila in resultados]
    suma_de_promedios = sum(promedios)

    tabla = Table(title="Análisis de Salarios Promedio por Departamento",
                  header_style="bold magenta")
    tabla.add_column("Departamento", style="cyan", no_wrap=True)
    tabla.add_column("Promedio (USD)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Frec. Abs. Acum.", justify="right", style="blue")
    tabla.add_column("Frec. Rel. Acum.", justify="right", style="blue")

    f_abs_acum = 0
    f_rel_acum = 0

    for depto, prom in zip(nombres_deptos, promedios):
        porcentaje = (prom / suma_de_promedios) * 100
        f_abs_acum += prom
        f_rel_acum += porcentaje

        tabla.add_row(
            depto,
            f"{prom:,.2f}",
            f"{porcentaje:.2f}%",
            f"{f_abs_acum:,.2f}",
            f"{f_rel_acum:.2f}%"
        )

    consola.clear()

    titulo = "GRAFICO DE BARRAS: RANKING DE SALARIOS PROMEDIO POR DEPARTAMENTO"
    guia = "El gráfico de barras muestra el salario promedio real por departamento, mostrando la proporción de salario respecto al total."

    printGuia(titulo, guia)

    consola.print(tabla)

    plt.figure(figsize=(10, 6))
    colores_barras = [
        f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(nombres_deptos))]

    barras = plt.bar(nombres_deptos, promedios,
                     color=colores_barras, edgecolor='black', alpha=0.8)

    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 100, f'${yval:,.0f}',
                 ha='center', va='bottom', fontweight='bold', fontsize=8)

    plt.title('Ranking de Salarios Promedio por Departamento - 2026', fontsize=14)
    plt.ylabel('Salario Promedio (USD)', fontsize=11)
    plt.xticks(rotation=45, ha='right')

    consola.print(
        "\n[bold magenta]Generando gráfico de barras salariales...[/bold magenta]")
    plt.tight_layout()
    plt.show()

# Diagrama de Pareto
# Genera un diagrama de Pareto para analizar qué departamentos
# concentran el mayor gasto salarial en la empresa.


def diagrama_pareto():
    consola = Console()
    conexion = get_conexion()

    consulta_sql = """
        SELECT d.department_name, SUM(e.salary) AS gasto_total
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY gasto_total DESC;
    """

    df_gastos = pd.read_sql(consulta_sql, conexion)
    conexion.close()

    total_nomina = df_gastos['gasto_total'].sum()
    df_gastos['frec_relativa'] = (
        df_gastos['gasto_total'] / total_nomina) * 100
    df_gastos['frec_abs_acumulada'] = df_gastos['gasto_total'].cumsum()
    df_gastos['frec_rel_acumulada'] = (
        df_gastos['frec_abs_acumulada'] / total_nomina) * 100

    titulo = "GRAFICO DE PARETO: DISTRIBUCIÓN DE GASTOS POR DEPARTAMENTO"
    guia = "El diagrama de Pareto muestra el gasto salarial acumulado por departamento, mostrando la proporción de gasto respecto al total."

    printGuia(titulo, guia)

    tabla = Table(title="Tabla de Frecuencias Completa",
                  header_style="bold magenta")
    tabla.add_column("Departamento", style="cyan", no_wrap=True)
    tabla.add_column("Frec. Absoluta (USD)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Frec. Abs. Acum.", justify="right", style="blue")
    tabla.add_column("Frec. Rel. Acum.", justify="right", style="blue")

    for _, fila in df_gastos.iterrows():
        tabla.add_row(
            fila['department_name'],
            f"${fila['gasto_total']:,.2f}",
            f"{fila['frec_relativa']:.2f}%",
            f"${fila['frec_abs_acumulada']:,.2f}",
            f"{fila['frec_rel_acumulada']:.2f}%"
        )

    consola.print(tabla)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(df_gastos['department_name'],
            df_gastos['gasto_total'], color="steelblue", width=0.8)
    ax1.set_ylabel("Gasto Total (USD)", color="steelblue", fontsize=12)
    plt.xticks(rotation=45, ha="right")

    ax2 = ax1.twinx()

    posiciones_x = np.arange(len(df_gastos))

    ax2.plot(posiciones_x, df_gastos['frec_rel_acumulada'],
             color="red", marker="D", ms=7, linestyle='-', label="Acumulado %")

    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel("Porcentaje Acumulado", color="red", fontsize=12)
    ax1.set_xlim([-0.5, len(df_gastos) - 0.5])
    ax2.set_ylim([0, 105])

    plt.title("Diagrama de Pareto: Distribución de Nómina",
              fontsize=14, fontweight="bold")
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

# Grafico de tallo y hoja
# Crea un gráfico de tallo y hoja que muestra la distribución de la edad de los empleados.


def grafico_tallo_y_hoja_porEdad():
    conexion = get_conexion()

    query = """
        SELECT DATEDIFF(YEAR, birth_date, GETDATE()) AS edad
        FROM employeess
        WHERE birth_date IS NOT NULL
        """

    df = pd.read_sql(query, conexion)
    conexion.close()

    if df.empty:
        print(
            "[bold yellow]Aviso:[/bold yellow] No se encontraron datos de fecha de nacimiento.")
        return

    # Ordenamos los datos
    datos_edad = sorted(df['edad'].tolist())

    titulo = "GRÁFICO DE TALLO Y HOJA: DISTRIBUCIÓN POR EDADES"

    guia = (
        "1. [bold]El Tallo:[/bold] Representa la primera cifra de la edad (2 = 20s, 3 = 30s, etc.).\n"
        "2. [bold]La Hoja:[/bold] Representa el último dígito. Si ves '2 | 1 3 5', significa que hay empleados de 21, 23 y 25 años.\n"
        "3. [cyan]Análisis:[/cyan] Este gráfico te permite ver qué tan 'joven' o 'senior' es la plantilla sin perder el detalle exacto de cada edad."
    )

    printGuia(titulo, guia)

    # Lógica de construcción
    tallo_hoja = {}
    for valor in datos_edad:
        tallo = valor // 10
        hoja = valor % 10
        if tallo not in tallo_hoja:
            tallo_hoja[tallo] = []
        tallo_hoja[tallo].append(str(hoja))

    print("\n--- REPRESENTACIÓN DE EDADES ---")
    print("Tallo | Hojas")
    print("-------------------------")
    for tallo in sorted(tallo_hoja.keys()):
        hojas = " ".join(tallo_hoja[tallo])
        print(f"  {tallo}   | {hojas}")
    print("-------------------------\n")

    input("Presiona ENTER para continuar...")


# Gráfico de puntos(Dot Plot)
# Crea un diagrama de puntos que muestra la frecuencia de empleados
# agrupados por rangos salariales redondeados a los mil dólares más cercanos.


def grafico_puntos():

    conexion = get_conexion()
    cursor = conexion.cursor()

    # SQL: Cantidad de empleados por departamento
    query = """
        SELECT d.department_name, COUNT(e.employee_id) AS cantidad_empleados
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY cantidad_empleados DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not resultados:
        consola.print(
            "[yellow]No hay datos disponibles para el gráfico de puntos.[/yellow]")
        return

    departamentos = [fila[0] for fila in resultados]
    cantidades = [int(fila[1]) for fila in resultados]
    total_empleados = sum(cantidades)

    tabla = Table(title="Análisis de Frecuencias: Plantilla por Departamento",
                  header_style="bold magenta")
    tabla.add_column("Departamento", style="cyan", no_wrap=True)
    tabla.add_column("Frec. Absoluta (Emp.)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Frec. Abs. Acum.", justify="right", style="blue")
    tabla.add_column("Frec. Rel. Acum.", justify="right", style="blue")

    f_abs_acum = 0
    f_rel_acum = 0

    for depto, cant in zip(departamentos, cantidades):
        porcentaje = (cant / total_empleados) * 100
        f_abs_acum += cant
        f_rel_acum += porcentaje

        tabla.add_row(
            depto,
            str(cant),
            f"{porcentaje:.2f}%",
            str(f_abs_acum),
            f"{f_rel_acum:.2f}%"
        )

    consola.clear()

    titulo = "GRÁFICO DE PUNTOS: DISTRIBUCIÓN DE EMPLEADOS POR DEPARTAMENTO"
    guia = (
        "1. [bold]Frecuencia Absoluta:[/bold] Representa la cantidad de empleados en un departamento.\n"
        "2. [bold]Frecuencia Relativa:[/bold] Representa el porcentaje de empleados en un departamento respecto al total de empleados.\n"
        "3. [bold]Frecuencia Absoluta Acumulada:[/bold] Representa la cantidad de empleados acumulada en todos los departamentos.\n"
        "4. [bold]Frecuencia Relativa Acumulada:[/bold] Representa el porcentaje de empleados acumulado en todos los departamentos respecto al total de empleados.\n"
    )

    printGuia(titulo, guia)

    consola.print(tabla)

    plt.figure(figsize=(10, 8))

    departamentos_inv = departamentos[::-1]
    cantidades_inv = cantidades[::-1]

    plt.hlines(y=departamentos_inv, xmin=0, xmax=cantidades_inv,
               color='skyblue', alpha=0.5, linewidth=2)

    plt.plot(cantidades_inv, departamentos_inv, "o",
             markersize=10, color='blue', alpha=0.7)

    for i, v in enumerate(cantidades_inv):
        plt.text(v + 0.5, i, str(v), color='blue',
                 va='center', fontweight='bold')

    plt.title('Distribución de Empleados por Departamento - 2026',
              fontsize=14, pad=20)
    plt.xlabel('Cantidad de Empleados', fontsize=11)
    plt.grid(axis='x', linestyle='--', alpha=0.3)

    consola.print(
        "\n[bold magenta]Generando gráfico de puntos (Lollipop)...[/bold magenta]")
    plt.tight_layout()
    plt.show()

# Gráfico de Bastón
# Crea un gráfico de bastón que muestra la distribución de salarios de los empleados.


def grafico_baston():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta: traer salarios de empleados
    query = """
        SELECT salary
        FROM employeess
        ORDER BY salary;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    if not resultados:
        consola.print("[yellow]No hay datos salariales.[/yellow]")
        return

    consola.clear()

    titulo = "GRAFICOS DE BASTON: SALARIOS DE EMPLEADOS"
    guia = (
        "1. [orange1]Barras (Frecuencia):[/orange1] Cada columna agrupa a los empleados en rangos de $1,000.\n"
        "2. [bold]Eje Horizontal (X):[/bold] Muestra los intervalos salariales (ej. 2000-3000).\n"
        "3. [bold]Eje Vertical (Y):[/bold] Indica cuántos empleados pertenecen a cada rango.\n"
        "4. [cyan]Propósito:[/cyan] Identificar visualmente la 'forma' de la nómina (si hay muchos sueldos bajos o pocos sueldos altos)."
    )
    printGuia(titulo, guia)

    datos = [float(fila[0]) for fila in resultados]
    total_emp = len(datos)

    # Creamos rangos de 1000 en 1000 para la tabla
    min_s = int(min(datos) // 1000 * 1000)
    max_s = int(max(datos) // 1000 * 1000) + 1000
    rangos = range(min_s, max_s + 1000, 1000)

    tabla = Table(title="Distribución Salarial por Rangos",
                  header_style="bold magenta")
    tabla.add_column("Rango Salarial (USD)", style="cyan")
    tabla.add_column("Frec. Absoluta (n)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Frec. Abs. Acum.", justify="right", style="blue")
    tabla.add_column("Frec. Rel. Acum.", justify="right", style="blue")

    f_abs_acum = 0
    f_rel_acum = 0

    for i in range(len(rangos)-1):
        inf, sup = rangos[i], rangos[i+1]
        # Contar cuántos empleados caen en este rango
        cant = sum(1 for s in datos if inf <= s < sup)

        if cant > 0:  # Solo mostramos rangos con gente
            porcentaje = (cant / total_emp) * 100
            f_abs_acum += cant
            f_rel_acum += porcentaje

            tabla.add_row(
                f"${inf:,} - ${sup:,}",
                str(cant),
                f"{porcentaje:.2f}%",
                str(f_abs_acum),
                f"{f_rel_acum:.2f}%"
            )

    consola.print(tabla)

    datos = [fila[0] for fila in resultados]

    x = list(range(1, len(datos) + 1))

    plt.figure(figsize=(10, 6))
    markerline, stemlines, baseline = plt.stem(
        x,
        datos,
        linefmt='-',       # formato de las líneas verticales
        markerfmt='',
        basefmt=' '        # oculta la línea base
    )

    plt.setp(markerline, markersize=6)
    plt.setp(stemlines, linewidth=0.8)

    plt.xlabel("Empleado (ordenado por salario)")
    plt.ylabel("Salario (USD)")
    plt.title("Gráfico de Bastón - Salarios de Empleados")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Histograma con rangos de valores
# Crea un gráfico de histograma que muestra la distribución de salarios de los empleados.


def grafico_histograma_rangos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta: obtener todos los salarios
    query = "SELECT salary FROM employeess;"
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    titulo = "GRAFICOS DE HISTOGRAMA: SALARIOS POR RANGOS"
    guia = (
        "1. [orange1]Barras (Bins):[/orange1] Cada columna representa un rango salarial de $1,000.\n"
        "2. [bold]Eje Y (Frecuencia):[/bold] Indica cuántos empleados caen dentro de cada rango.\n"
        "3. [bold]Distribución:[/bold] Permite observar la concentración de la nómina y detectar si existen "
        "sesgos hacia salarios bajos o altos.\n"
        "4. [cyan]Interpretación:[/cyan] Un pico alto indica el salario más común (moda) de la empresa."
    )
    printGuia(titulo, guia)

    salarios = [float(r[0]) for r in resultados if r[0] is not None]

    if not salarios:
        print("No hay datos para graficar.")
        return

    # intervalos (rangos de 1000 en 1000 hasta el máximo salario)
    tam_intervalo = 1000
    bordes = np.arange(0, max(salarios) + tam_intervalo, tam_intervalo)

    # 5. Crear histograma
    plt.figure(figsize=(10, 5))
    plt.hist(
        salarios,
        bins=bordes,
        color="#FFA07A",
        edgecolor="black"
    )

    # Etiquetas en el eje X
    etiquetas = [
        f"{int(bordes[i])}-{int(bordes[i+1])}"
        for i in range(len(bordes)-1)
    ]
    plt.xticks(bordes[:-1] + tam_intervalo/2, etiquetas, rotation=45)

    plt.title("Distribución de Salarios por Rangos",
              fontsize=14, fontweight="bold")
    plt.xlabel("Rango de Salario (USD)", fontsize=12)
    plt.ylabel("Número de Empleados", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

# Histograma con valores discretos
# Crea un gráfico de histograma que muestra la distribución de salarios de los empleados.


def grafico_histograma_discretos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener los salarios de la tabla employeess
    query = "SELECT salary FROM employeess WHERE salary IS NOT NULL"
    cursor.execute(query)

    salarios = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conexion.close()

    titulo = "GRAFICOS DE HISTOGRAMA: SALARIOS DE EMPLEADOS"
    guia = (
        "1. [bold green]Barras (Histograma):[/bold green] Cada barra representa la frecuencia con la que "
        "aparecen ciertos niveles salariales agrupados en 10 intervalos.\n"
        "2. [bold]Distribución Discreta:[/bold] Permite observar la densidad de la nómina: dónde hay "
        "acumulación de personal y dónde hay vacíos salariales.\n"
        "3. [cyan]Tendencia Central:[/cyan] Ayuda a identificar visualmente si los salarios están "
        "concentrados en la parte baja, media o alta de la escala.\n"
        "4. [bold]Eje Y (Frecuencia):[/bold] Indica el conteo exacto de empleados que pertenecen a cada intervalo."
    )
    printGuia(titulo, guia)

    plt.figure(figsize=(10, 6))
    plt.hist(salarios,
             bins=10,
             edgecolor='black',
             color='#4CAF50')

    # Personalización del diagrama
    plt.title('Distribución de Salarios de Empleados',
              fontsize=14, fontweight='bold')
    plt.xlabel('Salario (USD)', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.show()

# Gráfico de líneas(un grupo)
# Crea un gráfico de líneas que muestra la evolución del salario promedio de los empleados por mes de contratación.


def grafico_lineas_un_grupo():

    conexion = get_conexion()
    cursor = conexion.cursor()

    # SQL: Conteo de contrataciones por mes (independiente del año)
    # Esto nos dice en qué meses del año la empresa suele crecer más
    query = """
        SELECT MONTH(hire_date) AS mes_num, 
               COUNT(employee_id) AS cantidad_contrataciones
        FROM employeess
        GROUP BY MONTH(hire_date)
        ORDER BY mes_num
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    if not resultados:
        consola.print(
            "[yellow]No hay datos de fechas de contratación.[/yellow]")
        cursor.close()
        conexion.close()
        return

    meses_nombres = []
    conteos_contrataciones = []
    meses_espanol = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    for mes_num, cantidad in resultados:
        meses_nombres.append(meses_espanol[mes_num].capitalize())
        conteos_contrataciones.append(int(cantidad))

    total_contrataciones = sum(conteos_contrataciones)

    f_abs_acum = 0
    f_rel_acum = 0

    tabla = Table(title="Análisis Estacional de Reclutamiento",
                  header_style="bold magenta")
    tabla.add_column("Mes", style="cyan")
    tabla.add_column("Contrataciones (F. Abs)", justify="right", style="green")
    tabla.add_column("Frec. Relativa (%)", justify="right", style="green")
    tabla.add_column("Total Acumulado", justify="right", style="blue")
    tabla.add_column("Crecimiento Acum. %", justify="right", style="blue")

    for i in range(len(meses_nombres)):
        cant = conteos_contrataciones[i]
        porcentaje = (cant / total_contrataciones) * 100
        f_abs_acum += cant
        f_rel_acum += porcentaje

        tabla.add_row(
            meses_nombres[i],
            str(cant),
            f"{porcentaje:.2f}%",
            str(f_abs_acum),
            f"{f_rel_acum:.2f}%"
        )

    consola.clear()
    consola.print(tabla)

    cursor.close()
    conexion.close()

    titulo = "TENDENCIA DE CONTRATACIONES POR MES"
    guia = (
        "1. [bold red]Línea de Contrataciones:[/bold red] Muestra el volumen de altas en la empresa por mes.\n"
        "2. [bold]Picos de Contratación:[/bold] Identifica las temporadas de mayor crecimiento orgánico.\n"
        "3. [cyan]Propósito:[/cyan] Ayuda a planificar las cargas de trabajo de capacitación e inducción (Onboarding)."
    )
    printGuia(titulo, guia)

    plt.figure(figsize=(10, 5))
    plt.plot(meses_nombres, conteos_contrataciones,
             marker='s',  # Marcador cuadrado para variar
             linestyle='-',
             color='#2980B9',  # Un azul corporativo
             linewidth=3,
             label='Nuevos Empleados')

    plt.fill_between(meses_nombres, conteos_contrataciones,
                     color='#2980B9', alpha=0.2)

    for x, y in zip(meses_nombres, conteos_contrataciones):
        plt.text(x, y + 0.1, str(y), ha='center',
                 va='bottom', fontsize=10, fontweight='bold')

    plt.title('Histórico Estacional de Contrataciones', fontsize=14, pad=20)
    plt.xlabel('Mes del Año', fontsize=12)
    plt.ylabel('Cantidad de Ingresos', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Gráfico de líneas(dos grupos)
# Crea un gráfico de líneas que muestra la evolución del salario promedio de los empleados por mes de contratación.


def gráfico_líneas_dos_grupos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # SQL Server: Comparamos el volumen de contrataciones de IT vs Sales por mes
    query = """
        SELECT 
            MONTH(e.hire_date) AS mes,
            SUM(CASE WHEN d.department_name = 'IT' THEN 1 ELSE 0 END) AS contrataciones_it,
            SUM(CASE WHEN d.department_name = 'Sales' THEN 1 ELSE 0 END) AS contrataciones_ventas
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE d.department_name IN ('IT', 'Sales')
        GROUP BY MONTH(e.hire_date)
        ORDER BY mes;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not resultados:
        consola.print(
            "[yellow]No se encontraron datos para estos departamentos.[/yellow]")
        return

    meses_num = [r[0] for r in resultados]
    datos_it = [int(r[1]) for r in resultados]
    datos_ventas = [int(r[2]) for r in resultados]

    nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    etiquetas_x = [nombres_meses[m-1] for m in meses_num]

    titulo = "COMPARATIVA DE RECLUTAMIENTO POR DEPARTAMENTO"
    guia = (
        "1. [bold blue]Línea IT:[/bold blue] Muestra el ritmo de crecimiento del área tecnológica.\n"
        "2. [bold green]Línea Ventas:[/bold green] Muestra la agresividad comercial en contrataciones.\n"
        "3. [bold]Análisis:[/bold] Observa si los picos de Ventas coinciden con los de IT o si son independientes."
    )
    printGuia(titulo, guia)

    plt.figure(figsize=(12, 6))

    plt.plot(etiquetas_x, datos_it, marker='D',
             linewidth=2.5, label="IT", color='#2980B9')
    plt.plot(etiquetas_x, datos_ventas, marker='o',
             linewidth=2.5, label="Ventas", color='#27AE60')

    plt.title('Tendencia de Contratación: IT vs. Ventas (Histórico)',
              fontsize=14, pad=20)
    plt.xlabel('Meses del Año', fontsize=12)
    plt.ylabel('Nuevos Empleados', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Diagrama de cajas(Box plot)
# Crea un diagrama de cajas que muestra la distribución salarial de los empleados agrupados por departamento.


def grafico_boxplot():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # IDs de los departamentos según tu estructura
    id_ventas = 5
    id_finanzas = 2

    # SQL Server: Solo Finance y Sales
    query = f"""
        SELECT d.department_name, e.salary
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id IN ({id_ventas}, {id_finanzas}) 
        AND e.salary IS NOT NULL
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    datos_por_nombre = {"Sales": [], "Finance": []}
    for nombre_depto, salario in resultados:
        if nombre_depto in datos_por_nombre:
            datos_por_nombre[nombre_depto].append(float(salario))

    ventas_salarios = datos_por_nombre["Sales"]
    finanzas_salarios = datos_por_nombre["Finance"]

    tabla = Table(title="Resumen Estadístico de Salarios",
                  header_style="bold magenta")
    tabla.add_column("Departamento", style="cyan")
    tabla.add_column("Mínimo", justify="right")
    tabla.add_column("C1 (25%)", justify="right")
    tabla.add_column("C2 (50%)", justify="right")
    tabla.add_column("C3 (75%)", justify="right")
    tabla.add_column("Máximo", justify="right")

    def agregar_fila_estadistica(nombre, lista):
        if lista:
            stats = np.percentile(lista, [0, 25, 50, 75, 100])
            tabla.add_row(
                nombre,
                f"{stats[0]:,.2f}",
                f"{stats[1]:,.2f}",
                f"{stats[2]:,.2f}",
                f"{stats[3]:,.2f}",
                f"{stats[4]:,.2f}"
            )

    agregar_fila_estadistica("Sales", ventas_salarios)
    agregar_fila_estadistica("Finance", finanzas_salarios)

    consola.clear()

    consola.print(
        "[bold white]Set de Datos (Salarios ordenados):[/bold white]")

    if ventas_salarios:
        ventas_ordenados = sorted(ventas_salarios)
        consola.print(f"[green]Sales:[/green] {ventas_ordenados}")

    if finanzas_salarios:
        finanzas_ordenados = sorted(finanzas_salarios)
        consola.print(f"[blue]Finance:[/blue] {finanzas_ordenados}")

    consola.print("-" * 50)

    consola.print(tabla)

    titulo = "BOXPLOT: COMPARATIVA FINANCE VS SALES"
    guia = (
        "1. [bold green]Caja (IQR):[/bold green] Representa el 50% central de los empleados. "
        "Si la caja de Sales es más larga, sus sueldos son más desiguales.\n"
        "2. [red]Línea Media:[/red] Es la mediana. Permite ver qué departamento paga mejor 'en el centro'.\n"
        "3. [orange1]Bigotes y Outliers:[/orange1] Muestran los rangos extremos y salarios fuera de lo normal."
    )
    printGuia(titulo, guia)

    if not ventas_salarios and not finanzas_salarios:
        consola.print(
            "[yellow]No hay suficientes datos para graficar.[/yellow]")
        return

    plt.figure(figsize=(10, 5))

    plt.boxplot([ventas_salarios, finanzas_salarios],
                labels=["Sales", "Finance"],
                vert=False,
                patch_artist=True,
                boxprops=dict(facecolor='#AED6F1', color='#2E86C1'),
                medianprops=dict(color='red', linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='orange', markersize=6))

    plt.title("Distribución Salarial: Finance vs Sales",
              fontsize=14, fontweight='bold')
    plt.xlabel("Salario (USD)", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()


# Diagrama de Dispersión(Scatter plot)
# Crea un gráfico de dispersión que muestra la relación entre el salario y la antigüedad de los empleados.

def grafico_dispersion():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener anios y salarios
    query = """
        SELECT YEAR(hire_date) AS anio, salary
        FROM employeess
        WHERE salary IS NOT NULL AND hire_date IS NOT NULL
        ORDER BY anio
        """
    cursor.execute(query)
    resultados = cursor.fetchall()

    anios = [row[0] for row in resultados]
    salarios = [float(row[1]) for row in resultados]

    cursor.close()
    conexion.close()

    titulo = "GRÁFICO DE DISPERSIÓN: RELACIÓN AÑO VS SALARIO (TOTAL EMPRESA)"

    guia = (
        "1. [bold red]Mapa de Talentos:[/bold red] Cada punto representa a un empleado de la empresa.\n"
        "2. [bold]Tendencia Salarial:[/bold] Observa si los salarios aumentan con la antigüedad.\n"
        "3. [cyan]Dispersión:[/cyan] Identifica bandas salariales por año de ingreso."
    )

    printGuia(titulo, guia)

    plt.figure(figsize=(10, 6))

    # Usamos alpha=0.5 para que si hay puntos encima de otros, se vea más oscuro
    plt.scatter(
        anios,
        salarios,
        c='#2980b9',
        s=60,
        alpha=0.5,
        edgecolor='black',
        label='Empleados'
    )

    plt.title('Dispersión Salarial Total por Año de Ingreso',
              fontsize=14, pad=20)
    plt.xlabel('Año de Contratación', fontsize=12)
    plt.ylabel('Salario (USD)', fontsize=12)
    plt.grid(linestyle='--', alpha=0.3)

    plt.legend()
    plt.show()


def grafico_serie_tiempo():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # SQL Server: Obtenemos el gasto total por mes y año cronológicamente
    # Esto nos permite ver si el gasto sube, baja o se estabiliza
    query = """
        SELECT 
            FORMAT(hire_date, 'yyyy-MM') AS periodo,
            SUM(salary) AS gasto_mensual
        FROM employeess
        WHERE hire_date IS NOT NULL
        GROUP BY FORMAT(hire_date, 'yyyy-MM')
        ORDER BY periodo;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not resultados:
        consola.print("[yellow]No hay datos históricos suficientes.[/yellow]")
        return

    periodos = [r[0] for r in resultados]
    gastos = [float(r[1]) for r in resultados]

    consola.clear()

    titulo = "ANÁLISIS DE SERIE DE TIEMPO: GASTO MENSUAL"
    guia = (
        "1. [bold]Eje X (Tiempo):[/bold] Ordenado cronológicamente por Año y Mes.\n"
        "2. [bold green]Tendencia:[/bold green] Si la línea sube, la carga financiera crece.\n"
        "3. [bold cyan]Estacionalidad:[/bold cyan] Permite ver en qué meses de años anteriores hubo picos de inversión."
    )
    printGuia(titulo, guia)

    plt.figure(figsize=(12, 6))
    plt.plot(periodos, gastos, marker='o', color='#8E44AD',
             linewidth=2, label="Gasto en Salarios")

    plt.xticks(rotation=45, fontsize=8)
    plt.title('Evolución del Gasto Salarial Histórico', fontsize=14)
    plt.xlabel('Línea de Tiempo (Año-Mes)')
    plt.ylabel('Dólares (USD)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()
