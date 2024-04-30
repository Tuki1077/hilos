import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import time
import argparse

def calculate_stats(data):
    """
    Calcula estadísticas descriptivas solo de datos numéricos.
    :param data: DataFrame de pandas con los datos a analizar.
    :return: Un diccionario con las estadísticas calculadas.
    """
    numeric_data = data.select_dtypes(include=[np.number])  # Selecciona solo datos numéricos
    return {
        "count": numeric_data.count(),  # Cantidad de valores
        "mean": numeric_data.mean(),    # Media
        "std": numeric_data.std(),      # Desviación estándar
        "min": numeric_data.min(),      # Valor mínimo
        "max": numeric_data.max(),      # Valor máximo
    }

def process_file(file_path, output_dir):
    """
    Procesa un archivo individual y guarda las estadísticas en el directorio de salida.
    :param file_path: Ruta al archivo que se procesará.
    :param output_dir: Directorio de salida donde se guardarán los resultados.
    :return: La ruta al archivo de salida con las estadísticas.
    """
    data = pd.read_csv(file_path)  # Lee el archivo CSV
    stats = calculate_stats(data)  # Calcula las estadísticas
    # Guarda las estadísticas en el directorio de salida
    output_filename = os.path.join(output_dir, os.path.basename(os.path.splitext(file_path)[0]) + "_out.csv")
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename

def run_sequential(input_dir, output_dir):
    """
    Procesa cada archivo de manera secuencial y calcula el tiempo que toma cada uno.
    :param input_dir: Directorio de entrada con archivos CSV.
    :param output_dir: Directorio de salida para los archivos de estadísticas.
    :return: Lista de tiempos de procesamiento de cada archivo.
    """
    times = []  # Lista para almacenar los tiempos de procesamiento
    # Itera sobre cada archivo en el directorio de entrada
    for f in os.listdir(input_dir):
        if f.endswith(".csv"):  # Verifica que el archivo sea un CSV
            start = time.time()  # Comienza a medir el tiempo
            process_file(os.path.join(input_dir, f), output_dir)  # Procesa el archivo
            end = time.time()  # Termina de medir el tiempo
            times.append(end - start)  # Añade el tiempo a la lista
    return times  # Retorna la lista de tiempos

def run_parallel_files(input_dir, output_dir, max_workers):
    """
    Procesa archivos en paralelo utilizando un pool de hilos.
    :param input_dir: Directorio de entrada con archivos CSV.
    :param output_dir: Directorio de salida para los archivos de estadísticas.
    :param max_workers: Número máximo de hilos para el procesamiento paralelo.
    :return: Tiempo total tomado para procesar todos los archivos.
    """
    start_time = time.time()  # Comienza a medir el tiempo total
    # Crea un pool de hilos y somete las tareas de procesamiento de archivos
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, os.path.join(input_dir, f), output_dir) for f in os.listdir(input_dir) if f.endswith(".csv")]
        # Espera a que todas las tareas en el futuro se completen
        for future in as_completed(futures):
            future.result()
    return time.time() - start_time  # Retorna el tiempo total


def run_parallel_stats(input_dir, output_dir, max_workers):
    """
    Procesa estadísticas en paralelo para cada archivo en el directorio de entrada.
    :param input_dir: Directorio de entrada que contiene archivos CSV.
    :param output_dir: Directorio donde se guardarán los archivos de resultados.
    :param max_workers: Número máximo de hilos para el procesamiento paralelo.
    :return: Lista de tiempos que tomó procesar cada archivo.
    """
    times = []  # Lista para almacenar los tiempos de procesamiento de cada archivo
    # Itera sobre cada archivo en el directorio de entrada
    for f in os.listdir(input_dir):
        if f.endswith(".csv"):  # Verifica que el archivo sea un CSV
            file_path = os.path.join(input_dir, f)  # Construye la ruta completa del archivo
            data = pd.read_csv(file_path)  # Lee el archivo CSV
            start = time.time()  # Comienza a medir el tiempo
            # Utiliza un pool de hilos para calcular estadísticas en paralelo
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                stats = {name: executor.submit(func, numeric_only=True).result() for name, func in {
                    'count': data.count,
                    'mean': data.mean,
                    'std': data.std,
                    'min': data.min,
                    'max': data.max,
                }.items()}
            end = time.time()  # Finaliza el tiempo de medición
            times.append(end - start)  # Añade el tiempo a la lista de tiempos
            # Crea y guarda el archivo de salida con las estadísticas calculadas
            output_filename = os.path.join(output_dir, os.path.basename(os.path.splitext(file_path)[0]) + "_out.csv")
            pd.DataFrame(stats).to_csv(output_filename, index=False)
    return times  # Retorna la lista de tiempos

def main(modelo, num_hilos, num_iteraciones):
    """
    Función principal que ejecuta el procesador de estadísticas descriptivas según el modelo seleccionado.
    :param modelo: Modelo de paralelismo a ejecutar.
    :param num_hilos: Número de hilos para el procesamiento paralelo.
    :param num_iteraciones: Número de veces que se ejecutará el procesamiento.
    """
    # Determina el directorio de entrada y salida basado en el entorno de ejecución
    input_dir = "/app/so_data" if os.getenv('RUNNING_IN_DOCKER') == 'true' else "so_data"
    output_dir = "/app/outcsv" if os.getenv('RUNNING_IN_DOCKER') == 'true' else "outcsv"
    os.makedirs(output_dir, exist_ok=True)  # Asegura que el directorio de salida exista

    total_times = []  # Lista para almacenar los tiempos totales de cada iteración

    # Imprime el modelo seleccionado
    if modelo == 1:
        modelo_str = "Todo secuencial"
    elif modelo == 2:
        modelo_str = "Paralelizando archivos (funciones estadísticas secuenciales)"
    elif modelo == 3:
        modelo_str = "Paralelizando funciones (archivos secuenciales)"
    else:
        raise ValueError("Selección de modelo inválida")

    print(f"Ejecutando el modelo '{modelo_str}' con {num_hilos} hilos y {num_iteraciones} iteraciones.")

    # Ejecuta el procesamiento según el modelo seleccionado
    for i in range(num_iteraciones):
        start_iter = time.time()  # Inicia el tiempo para la iteración actual

        if modelo == 1:
            times = run_sequential(input_dir, output_dir)
        elif modelo == 2:
            times = [run_parallel_files(input_dir, output_dir, num_hilos)]
        elif modelo == 3:
            times = run_parallel_stats(input_dir, output_dir, num_hilos)
        else:
            raise ValueError("Modelo no válido")

        # Calcula y muestra el tiempo que tomó la iteración actual
        end_iter = time.time()
        iter_time = end_iter - start_iter
        total_times.append(iter_time)
        print(f"Iteración {i+1}: {iter_time:.4f} segundos")

    # Calcula y muestra el tiempo promedio después de todas las iteraciones
    avg_time = np.mean(total_times)
    print(f"Tiempo promedio por iteración: {avg_time:.4f} segundos en {num_iteraciones} iteraciones.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Procesa estadísticas descriptivas.')
    parser.add_argument('modelo', type=int, choices=[1, 2, 3], help='Elige el modelo de paralelismo a ejecutar: 1 Todo secuencial, 2 archivos paralelos, 3 estadísticas paralelas')
    parser.add_argument('num_hilos', type=int, help='Número de hilos para procesamiento paralelo')
    parser.add_argument('num_iteraciones', type=int, help='Número de iteraciones a ejecutar')
    args = parser.parse_args()

    main(args.modelo, args.num_hilos, args.num_iteraciones)
