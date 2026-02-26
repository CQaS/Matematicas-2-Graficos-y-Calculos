import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.stats import hypergeom
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from conexion.conexion import get_conexion

# Regresión Lineal Simple
# Realiza una regresión lineal sobre la antigüedad vs salario en HR
# y muestra los resultados formateados con Rich.


def analisis_regresion_salarial():

    consola = Console()
    conexion = get_conexion()

    # Consulta: Antigüedad (X) y Salario (Y)
    consulta_sql = """
        SELECT 
            DATEDIFF(YEAR, hire_date, GETDATE()) AS antiguedad_anios,
            salary
        FROM employeess
    """

    df_datos = pd.read_sql(consulta_sql, conexion)
    conexion.close()

    # Preparación de datos
    X = df_datos[['antiguedad_anios']].values
    Y = df_datos['salary'].values

    # Entrenamiento del modelo
    modelo_hiring = LinearRegression()
    modelo_hiring.fit(X, Y)

    # Métricas
    y_pred = modelo_hiring.predict(X)
    r2 = r2_score(Y, y_pred)

    # Análisis de significancia con Statsmodels
    X_con_constante = sm.add_constant(X)
    resultados_ols = sm.OLS(Y, X_con_constante).fit()
    valor_p = resultados_ols.pvalues[1]

    # --- Salida con Rich ---
    consola.print(Panel(
        "[bold blue]Resultados del Análisis de Regresión Lineal (HR)[/bold blue]", expand=False))

    # Tabla de Coeficientes
    tabla = Table(title="Métricas del Modelo")
    tabla.add_column("Parámetro", style="cyan")
    tabla.add_column("Valor", style="magenta")

    tabla.add_row("Intersección (Beta 0)", f"{modelo_hiring.intercept_:.2f}")
    tabla.add_row("Pendiente (Beta 1)", f"{modelo_hiring.coef_[0]:.2f}")
    tabla.add_row("Coeficiente R²", f"{r2:.4f}")
    tabla.add_row("Valor p", f"{valor_p:.12f}")

    consola.print(tabla)

    # Conclusión dinámica
    if valor_p < 0.05:
        color_msj = "green"
        mensaje = "Existe una relación lineal significativa entre la antigüedad y el salario."
    else:
        color_msj = "red"
        mensaje = "No se encontró evidencia de una relación lineal significativa."

    consola.print(Panel(f"[{color_msj}]Conclusión: {mensaje}[/{color_msj}]"))

    # Gráfico (opcional, igual que antes)
    plt.scatter(X, Y, color='teal', alpha=0.5)
    plt.plot(X, y_pred, color='red')
    plt.title(f"Regresión Salarial (R² = {r2:.2f})")
    plt.show()


# Binomial
# Calcula la probabilidad binomial de encontrar empleados con salarios altos
# basándose en la proporción real de la base de datos HR.

def analisis_binomial_probabilidad_salarial():
    consola = Console()
    conexion = get_conexion()

    # 1. Calculamos la probabilidad 'p' real de la base de datos
    # Queremos saber cuántos empleados ganan más de 5000
    query_p = """
        SELECT 
            (SELECT CAST(COUNT(*) AS FLOAT) FROM employeess WHERE salary > 5000) / 
            (SELECT CAST(COUNT(*) AS FLOAT) FROM employeess) as p_real
    """
    p_real = pd.read_sql(query_p, conexion).iloc[0, 0]
    conexion.close()

    # 2. Parámetros del experimento
    n_ensayos = 10  # Si tomamos 10 empleados al azar
    k_exitos = 3    # ¿Cuál es la probabilidad de que exactamente 3 ganen > 5000?

    # PMF: Probabilidad exacta
    prob_exacta = binom.pmf(k_exitos, n_ensayos, p_real)

    # CDF: Probabilidad acumulada (P de que 5 o menos ganen eso)
    prob_acumulada = binom.cdf(5, n_ensayos, p_real)

    # --- Salida con Rich ---
    consola.print(Panel(f"[bold green]Análisis Binomial HR[/bold green]\n"
                        f"Probabilidad base (sueldo > 5000): {p_real:.2%}", expand=False))

    consola.print(f"• Probabilidad de que exactamente [bold]{k_exitos}[/bold] de {n_ensayos} empleados "
                  f"tengan sueldo alto: [cyan]{prob_exacta:.4f}[/cyan]")

    # 3. Gráfico de la distribución
    eje_x = np.arange(0, n_ensayos + 1)
    distribucion_teorica = binom.pmf(eje_x, n_ensayos, p_real)

    plt.figure(figsize=(10, 6))
    plt.bar(eje_x, distribucion_teorica, color='teal', alpha=0.7,
            label=f'Probabilidades para n={n_ensayos}')

    plt.title(
        f'Distribución de Probabilidad: Empleados con Sueldo > $5,000\n(Basado en p={p_real:.2f})')
    plt.xlabel('Cantidad de empleados en la muestra')
    plt.ylabel('Probabilidad')
    plt.xticks(eje_x)
    plt.grid(axis='y', alpha=0.3)
    plt.show()


# Hipergeométrica
# Calcula la probabilidad hipergeométrica de seleccionar empleados de un
# departamento específico al azar, sin reemplazo, desde la nómina total.

def analisis_hipergeometrica():
    consola = Console()
    conexion = get_conexion()

    # Obtenemos los datos reales de la población
    # N = Población total (total de empleados)
    # K = Éxitos en población (empleados del departamento 4 - IT)
    query = """
        SELECT 
            (SELECT COUNT(*) FROM employeess) as total_n,
            (SELECT COUNT(*) FROM employeess WHERE department_id = 4) as exitos_k
    """
    datos = pd.read_sql(query, conexion)
    poblacion_total_N = int(datos.iloc[0, 0])
    exitos_poblacion_K = int(datos.iloc[0, 1])
    conexion.close()

    # Parámetros del experimento
    muestra_n = 8       # Elegimos 8 empleados al azar para un comité
    exitos_deseados_k = 2  # ¿Probabilidad de que exactamente 2 sean de IT?

    # 1. PMF: Probabilidad exacta
    prob_exacta = hypergeom.pmf(
        exitos_deseados_k, poblacion_total_N, exitos_poblacion_K, muestra_n)

    # 2. CDF: Probabilidad de que haya 2 o menos empleados de IT
    prob_acumulada = hypergeom.cdf(
        exitos_deseados_k, poblacion_total_N, exitos_poblacion_K, muestra_n)

    # --- Salida con Rich ---
    consola.print(Panel(f"[bold magenta]Análisis Hipergeométrico HR[/bold magenta]\n"
                        f"Población Total: {poblacion_total_N} | Empleados IT: {exitos_poblacion_K}", expand=False))

    consola.print(
        f"Si seleccionas [bold]{muestra_n}[/bold] empleados sin reemplazo:")
    consola.print(
        f"• P(X = {exitos_deseados_k} de IT) = [yellow]{prob_exacta:.4%}[/yellow]")
    consola.print(
        f"• P(X ≤ {exitos_deseados_k} de IT) = [yellow]{prob_acumulada:.4%}[/yellow]")

    # 3. Gráfico
    x = np.arange(0, min(muestra_n, exitos_poblacion_K) + 1)
    pmf_teorica = hypergeom.pmf(
        x, poblacion_total_N, exitos_poblacion_K, muestra_n)

    plt.figure(figsize=(10, 6))
    plt.bar(x, pmf_teorica, color='orchid',
            alpha=0.7, label='Probabilidad Teórica')
    plt.title(
        f'Probabilidad de encontrar "k" empleados de IT\nen una muestra de {muestra_n}')
    plt.xlabel('Cantidad de empleados de IT en la muestra')
    plt.ylabel('Probabilidad')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.show()
