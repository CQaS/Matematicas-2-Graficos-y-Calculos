
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from calendar import month_abbr
from conexion.conexion import get_conexion

# Gráfico de sectores(Pie chart) - pastel o torta


def grafico_pastel():
    """ # Datos
    sistemas = ['Hogar', 'Servicios', 'Comidas', 'Supermercado']  # Categorías
    porcentajes = [73260, 34000, 24000, 123000]         	         # Valores
    colores = ['#fbf989', '#ff9999', '#99ff99', '#99bbff']          # Colores """

    conexion = get_conexion()

    cursor = conexion.cursor()

    # Consulta para obtener categorías y sus valores
    cursor.execute("""
                SELECT job_title, max_salary
                FROM jobss
                """)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

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


def grafico_barras():

    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta SQL: salario promedio por departamento
    query = """
        SELECT d.department_name, AVG(e.salary) AS salario_promedio
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY salario_promedio DESC;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    df = pd.DataFrame(
        [(fila[0], float(fila[1])) for fila in resultados],
        columns=["Departamento", "Salario Promedio"]
    )

    plt.figure(figsize=(10, 6))
    plt.bar(df["Departamento"], df["Salario Promedio"],
            color="skyblue", edgecolor="black")

    plt.title("Salario promedio por Departamento",
              fontsize=14, fontweight="bold")
    plt.xlabel("Departamento", fontsize=12)
    plt.ylabel("Salario Promedio (USD)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


# Gráfico de puntos(Dot Plot)

def grafico_puntos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta: salarios redondeados en miles + frecuencia
    query = """
        SELECT 
            ROUND(salary, -3) AS salario_redondeado,
            COUNT(*) AS cantidad
        FROM employeess
        GROUP BY ROUND(salary, -3)
        ORDER BY ROUND(salary, -3);
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    df = pd.DataFrame(
        [(float(r[0]), r[1]) for r in resultados],
        columns=["Salario Redondeado", "Cantidad"]
    )

    unique_vals = df["Salario Redondeado"].to_numpy()
    counts = df["Cantidad"].to_numpy()
    y_coords = np.concatenate([np.arange(1, c + 1) for c in counts])
    x_coords = np.repeat(unique_vals, counts)

    plt.figure(figsize=(8, 5))
    plt.scatter(x_coords, y_coords, color="blue", alpha=0.7)

    plt.xticks(unique_vals, rotation=45)
    plt.yticks(np.arange(1, max(counts) + 1))
    plt.title("Distribución de Salarios (Redondeados en miles)",
              fontsize=14, fontweight="bold")
    plt.xlabel("Salario (USD)")
    plt.ylabel("Frecuencia")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

# Gráfico de Bastón


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


def grafico_histograma_rangos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta: obtener todos los salarios
    query = "SELECT salary FROM employeess;"
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
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


def grafico_histograma_discretos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener los salarios de la tabla employeess
    query = "SELECT salary FROM employeess WHERE salary IS NOT NULL"
    cursor.execute(query)

    salarios = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conexion.close()

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


def grafico_lineas_dos_grupos():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # La consulta agrupará los salarios promedio por año de contratación para cada departamento, y el gráfico mostrará dos líneas: una para IT y otra para Sales.

    # Consulta para obtener el promedio de salarios por año para IT (department_id = 60)
    query_it = """
        SELECT YEAR(e.hire_date) AS anio, AVG(e.salary) AS salario_promedio
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 60 AND e.salary IS NOT NULL
        GROUP BY YEAR(e.hire_date)
        ORDER BY anio
        """
    cursor.execute(query_it)
    datos_it = cursor.fetchall()
    anios_it = [int(row[0]) for row in datos_it]
    salarios_it = [float(row[1]) for row in datos_it]

    # Consulta para obtener el promedio de salarios por año para Sales (department_id = 80)
    query_sales = """
        SELECT YEAR(e.hire_date) AS anio, AVG(e.salary) AS salario_promedio
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.salary IS NOT NULL
        GROUP BY YEAR(e.hire_date)
        ORDER BY anio
        """
    cursor.execute(query_sales)
    datos_sales = cursor.fetchall()
    anios_sales = [int(row[0]) for row in datos_sales]
    salarios_sales = [float(row[1]) for row in datos_sales]

    cursor.close()
    conexion.close()

    anios = sorted(list(set(anios_it + anios_sales)))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(anios_it, salarios_it, marker="o", label="IT", color="#1f77b4")
    ax.plot(anios_sales, salarios_sales, marker="o",
            label="Sales", color="#ff7f0e")
    ax.legend()

    # Personalización
    plt.title(
        'Salario Promedio por Año de Contratación (IT vs Sales)', fontsize=14, pad=20)
    plt.xlabel('Año de Contratación', fontsize=12)
    plt.ylabel('Salario Promedio (USD)', fontsize=12)
    plt.xticks(np.arange(min(anios), max(anios) + 1, step=1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

# Diagrama de cajas(Box plot)


def grafico_boxplot():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener salarios por departamento (IT, Sales, Finance)
    query = """
        SELECT e.department_id, e.salary
        FROM employeess e
        WHERE e.department_id IN (60, 80, 100) AND e.salary IS NOT NULL
        ORDER BY e.department_id
        """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Organizar datos por departamento
    salarios_por_depto = {60: [], 80: [], 100: []}
    for dept_id, salary in resultados:
        salarios_por_depto[dept_id].append(float(salary))

    # Obtener listas de salarios para cada departamento
    it_salarios = salarios_por_depto[60]
    sales_salarios = salarios_por_depto[80]
    finance_salarios = salarios_por_depto[100]

    cursor.close()
    conexion.close()

    # Crear el boxplot
    plt.figure(figsize=(10, 6))
    box = plt.boxplot([it_salarios, sales_salarios, finance_salarios],
                      labels=["IT", "Sales", "Finance"],
                      patch_artist=True,  # Para colorear las cajas
                      boxprops=dict(facecolor='#4CAF50', color='black'),
                      medianprops=dict(color='red'),
                      whiskerprops=dict(color='black'),
                      capprops=dict(color='black'),
                      flierprops=dict(marker='o', markerfacecolor='orange', markersize=5))

    # Personalización
    plt.title("Distribución de Salarios por Departamento",
              fontsize=14, fontweight='bold')
    plt.ylabel("Salario (USD)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.ylim(0, max(max(it_salarios), max(sales_salarios),
                    max(finance_salarios)) * 1.1)  # Ajuste de eje Y

    plt.show()

# Diagrama de Dispersión(Scatter plot)


def grafico_dispersion():
    conexion = get_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener año de contratación y salario del departamento Sales
    query = """
        SELECT YEAR(e.hire_date) AS anio, e.salary
        FROM employeess e
        JOIN departmentss d ON e.department_id = d.department_id
        WHERE e.department_id = 80 AND e.salary IS NOT NULL AND e.hire_date IS NOT NULL
        ORDER BY anio
        """
    cursor.execute(query)
    resultados = cursor.fetchall()

    anios = [row[0] for row in resultados]
    salarios = [float(row[1]) for row in resultados]

    cursor.close()
    conexion.close()

    plt.figure(figsize=(10, 6))
    plt.scatter(
        anios,
        salarios,
        c='#e74c3c',
        s=80,
        edgecolor='black',
    )

    # Personalización
    plt.title(
        'Relación entre Año de Contratación y Salario (Sales)', fontsize=14, pad=20)
    plt.xlabel('Año de Contratación', fontsize=12)
    plt.ylabel('Salario (USD)', fontsize=12)
    plt.grid(linestyle='--', alpha=0.3)

    plt.legend()
    plt.show()
