
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import PercentFormatter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from calendar import month_abbr
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
        "\n[bold blink]Sugerencia:[/bold blink] Cierra la ventana del gráfico para continuar con el programa.")

# Gráfico de sectores(Pie chart) - pastel o torta
# Genera un gráfico circular que muestra la distribución del gasto
# total en salarios por cada departamento de la base de datos HR.


def grafico_pastel():

    conexion = get_conexion()

    cursor = conexion.cursor()

    # Consulta para obtener categorías y sus valores
    cursor.execute("""
                SELECT d.department_name, SUM(e.salary)
                FROM employeess e
                JOIN departmentss d ON e.department_id = d.department_id
                GROUP BY d.department_name
                """)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    titulo = "GRAFICO DE PASTEL: DISTRIBUCION DE GASTOS POR DEPARTAMENTO"
    guia = "El gráfico de pastel muestra la distribución del gasto total en salarios por cada departamento de la base de datos HR."
    printGuia(titulo, guia)

    # Llenar los arreglos dinámicamente
    sistemas = [fila[0] for fila in resultados]         # categorías
    porcentajes = [float(fila[1]) for fila in resultados]  # montos

    # Generar colores aleatorios según cantidad de categorías
    colores = [
        f"#{random.randint(0, 0xFFFFFF):06x}"
        for _ in range(len(sistemas))
    ]

    explode = [0] * len(porcentajes)

    # Crear gráfico de pastel
    plt.figure(figsize=(8, 5))
    plt.pie(porcentajes,
            explode=explode,
            labels=sistemas,
            colors=colores,
            autopct='%1.1f%%',  # Mostrar porcentajes
            )

    # Personalización
    plt.title('Gastos Mayo 2025',
              fontsize=14)
    plt.show()

# Gráfico de barras
# Genera un gráfico de barras comparativo que muestra el salario
# promedio real por departamento, ordenado de mayor a menor.


def grafico_barras():

    conexion = get_conexion()

    # Mejora: Redondeamos a 2 decimales directamente en SQL
    query = """
        SELECT d.department_name, ROUND(AVG(e.salary), 2) AS salario_promedio
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY salario_promedio DESC;
    """

    # Sugerencia: Cargar directamente a DataFrame para simplificar
    df = pd.read_sql(query, conexion)
    conexion.close()

    titulo = "GRAFICO DE BARRAS: SALARIO PROMEDIO POR DEPARTAMENTO"
    guia = "El gráfico de barras muestra el salario promedio real por departamento, ordenado de mayor a menor."
    printGuia(titulo, guia)

    plt.figure(figsize=(10, 6))

    # Mejora visual: Usar un degradado o color sólido profesional
    barras = plt.bar(df["department_name"], df["salario_promedio"],
                     color="steelblue", edgecolor="black")

    # Personalización
    plt.title("Salario Promedio por Departamento",
              fontsize=14, fontweight="bold")
    plt.xlabel("Departamento", fontsize=12)
    plt.ylabel("Salario Promedio (USD)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Opcional: Agregar el valor numérico encima de cada barra
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval, f'${yval}',
                 va='bottom', ha='center', fontsize=9)

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

    # Consulta: Agrupamos por miles para identificar tendencias de pago
    query = """
        SELECT 
            CAST(ROUND(salary, -3) AS INT) AS salario_miles,
            COUNT(*) AS cantidad
        FROM employeess
        GROUP BY ROUND(salary, -3)
        ORDER BY salario_miles;
    """

    # Usamos pandas para una carga más directa
    df = pd.read_sql(query, conexion)
    conexion.close()

    titulo = "GRAFICOS DE PUNTOS: FRECUENCIA DE SALARIOS POR DEPARTAMENTO"
    guia = "El gráfico de puntos muestra la frecuencia de empleados agrupados por rangos salariales redondeados a los mil dolares mas cercanos."
    printGuia(titulo, guia)

    # Preparación de coordenadas para el efecto de "puntos apilados"
    x_coords = np.repeat(df["salario_miles"], df["cantidad"])
    y_coords = np.concatenate([np.arange(1, c + 1) for c in df["cantidad"]])

    plt.figure(figsize=(10, 5))

    # Dibujar los puntos
    plt.scatter(x_coords, y_coords, color="darkblue",
                s=100, alpha=0.6, edgecolors="black")

    # Personalización de ejes
    plt.xticks(df["salario_miles"], rotation=45)

    # Solo mostrar enteros en el eje Y
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.title("Frecuencia de Salarios (Redondeados a miles)",
              fontsize=14, fontweight="bold")
    plt.xlabel("Salario Estimado (USD)", fontsize=12)
    plt.ylabel("Número de Empleados", fontsize=12)
    plt.grid(axis="x", linestyle=":", alpha=0.3)

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

    titulo = "GRAFICOS DE BASTON: SALARIOS DE EMPLEADOS"
    guia = (
        "1. [orange1]Barras (Frecuencia):[/orange1] Cada columna agrupa a los empleados en rangos de $1,000.\n"
        "2. [bold]Eje Horizontal (X):[/bold] Muestra los intervalos salariales (ej. 2000-3000).\n"
        "3. [bold]Eje Vertical (Y):[/bold] Indica cuántos empleados pertenecen a cada rango.\n"
        "4. [cyan]Propósito:[/cyan] Identificar visualmente la 'forma' de la nómina (si hay muchos sueldos bajos o pocos sueldos altos)."
    )
    printGuia(titulo, guia)

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

    # Consulta para obtener el promedio de salarios por mes de contratación
    query = """
        SELECT MONTH(hire_date) AS mes, AVG(salary) AS salario_promedio
        FROM employeess
        WHERE salary IS NOT NULL
        GROUP BY MONTH(hire_date)
        ORDER BY mes
        """
    cursor.execute(query)

    resultados = cursor.fetchall()
    meses = [month_abbr[mes]
             for mes, _ in resultados]  # Nombres abreviados de meses
    salarios_promedio = [float(salario) for _, salario in resultados]

    cursor.close()
    conexion.close()

    titulo = "GRAFICOS DE LÍNEAS: SALARIOS PROMEDIO POR MES DE CONTRATAÇÃO"
    guia = (
        "1. [bold red]Línea de Tendencia:[/bold red] Muestra la evolución del salario promedio según el mes "
        "en que los empleados fueron contratados.\n"
        "2. [bold]Marcadores (Puntos):[/bold] Cada punto representa el valor exacto calculado para ese mes "
        "específico, facilitando la lectura de picos y valles.\n"
        "3. [cyan]Análisis de Estacionalidad:[/cyan] Permite identificar si hubo meses o temporadas de "
        "contratación con perfiles de mayor o menor remuneración.\n"
        "4. [bold]Interpretación:[/bold] Una línea ascendente o descendente indica cambios en las políticas "
        "salariales o en el nivel de senioridad de las nuevas contrataciones a lo largo del año."
    )
    printGuia(titulo, guia)

    plt.figure(figsize=(10, 5))
    plt.plot(meses, salarios_promedio,
             marker='o',
             linestyle='-',
             color='#E74C3C',
             linewidth=2,
             label='Salario Promedio (USD)')

    # Personalización
    plt.title('Salario Promedio por Mes de Contratación',
              fontsize=14, pad=20)
    plt.xlabel('Mes', fontsize=12)
    plt.ylabel('Salario Promedio (USD)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    plt.show()

# Gráfico de líneas(dos grupos)
# Crea un gráfico de líneas que muestra la evolución del salario promedio de los empleados por mes de contratación, agrupados por departamento.


def grafico_evolucion_contrataciones():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta: Cuenta empleados por año de contratación
    query = """
        SELECT YEAR(hire_date) AS anio, COUNT(*) AS total_empleados
        FROM employeess
        WHERE hire_date IS NOT NULL
        GROUP BY YEAR(hire_date)
        ORDER BY anio
        """
    cursor.execute(query)
    resultados = cursor.fetchall()

    if not resultados:
        print("[bold yellow]Aviso:[/bold yellow] No hay datos de contrataciones.")
        cursor.close()
        conexion.close()
        return

    anios = [int(row[0]) for row in resultados]
    totales = [int(row[1]) for row in resultados]

    cursor.close()
    conexion.close()

    titulo = "GRÁFICO DE LÍNEAS: EVOLUCIÓN DE CONTRATACIONES POR AÑO"
    guia = (
        "1. [bold]Crecimiento de la Empresa:[/bold] La línea muestra cuántas personas se unieron "
        "cada año.\n"
        "2. [bold]Picos de Contratación:[/bold] Identifica los años de mayor expansión (ej. 2026).\n"
        "3. [bold]Tendencia:[/bold] Observa si la empresa está contratando cada vez más o si se ha estabilizado."
    )
    printGuia(titulo, guia)

    # --- GRAFICAR ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # Área sombreada bajo la línea para más impacto visual
    ax.plot(anios, totales, marker="o", linestyle="-",
            color="#27ae60", linewidth=2)
    ax.fill_between(anios, totales, color="#27ae60", alpha=0.2)

    # Personalización
    plt.title('Ritmo de Contratación Anual (Total Empresa)',
              fontsize=14, pad=20)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Cantidad de Empleados Nuevos', fontsize=12)

    # Forzar años enteros
    plt.xticks(anios, rotation=45)

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Diagrama de cajas(Box plot)
# Crea un diagrama de cajas que muestra la distribución salarial de los empleados agrupados por departamento.


def grafico_boxplot():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # -------------------------
    dept_it = 1
    dept_sales = 5
    dept_finance = 2
    # -------------------------

    query = f"""
        SELECT e.department_id, e.salary
        FROM employeess e
        WHERE e.department_id IN ({dept_it}, {dept_sales}, {dept_finance}) 
        AND e.salary IS NOT NULL
        ORDER BY e.department_id
        """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Organizar datos por departamento
    salarios_por_depto = {dept_it: [], dept_sales: [], dept_finance: []}
    for dept_id, salary in resultados:
        if dept_id in salarios_por_depto:
            salarios_por_depto[dept_id].append(float(salary))

    # Obtener listas
    it_salarios = salarios_por_depto[dept_it]
    sales_salarios = salarios_por_depto[dept_sales]
    finance_salarios = salarios_por_depto[dept_finance]

    cursor.close()
    conexion.close()

    titulo = "GRAFICOS DE BOXPLOT: DISTRIBUCIÓN DE SALARIOS POR DEPARTAMENTO"

    guia = (
        "1. [bold green]Interpretación de Cajas:[/bold green] Las cajas muestran la dispersión salarial. "
        "Si la caja es muy ancha, hay mucha diferencia de sueldos dentro del departamento.\n"
        "2. [red]Línea Roja (Mediana):[/red] Indica el salario central. En este gráfico, parece que "
        "Finance tiene la mediana más alta, pero Sales tiene más dispersión.\n"
        "3. [orange1]Puntos Naranjas (Outliers):[/orange1] Son salarios excepcionalmente altos o bajos. "
        "Por ejemplo, hay un sueldo muy alto en Finance respecto al resto de su caja.\n"
        "4. [cyan]Comparación:[/cyan] Permite visualizar qué departamentos tienen rangos salariales "
        "más competitivos o equitativos.\n"
        "5. [bold]Datos Actuales:[/bold] El gráfico se basa en los departamentos con IDs "
        f"{dept_it}, {dept_sales}, {dept_finance}."
    )

    printGuia(titulo, guia)

    # --- VALIDACIÓN DE DATOS ---
    # Si alguna lista está vacía, el gráfico falla
    if not it_salarios and not sales_salarios and not finance_salarios:
        print("[bold yellow]Aviso:[/bold yellow] No hay datos salariales para los departamentos seleccionados.")
        return
    # ---------------------------

    plt.figure(figsize=(10, 6))
    box = plt.boxplot([it_salarios, sales_salarios, finance_salarios],
                      labels=["IT", "Sales", "Finance"],
                      vert=False,
                      patch_artist=True,
                      boxprops=dict(facecolor='#4CAF50', color='black'),
                      medianprops=dict(color='red'),
                      whiskerprops=dict(color='black'),
                      capprops=dict(color='black'),
                      flierprops=dict(marker='o', markerfacecolor='orange', markersize=5))

    plt.title("Distribución de Salarios por Departamento",
              fontsize=14, fontweight='bold')
    plt.xlabel("Salario (USD)", fontsize=12)
    plt.ylabel("Departamento", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.4)

    all_salaries = it_salarios + sales_salarios + finance_salarios
    if all_salaries:
        plt.xlim(0, max(all_salaries) * 1.1)

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
