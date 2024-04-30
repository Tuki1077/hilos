# hilos 
Proyecto sobre Hilos para Sistemas Operativos UFM
# Procesador de Estadísticas Descriptivas

Esta aplicación procesa archivos CSV para calcular estadísticas descriptivas utilizando diversos modelos de paralelismo para mejorar el rendimiento. La herramienta ofrece tres modos de operación: procesamiento secuencial, procesamiento paralelo a nivel de archivos y procesamiento paralelo a nivel de funciones.

## Características

- Calcula estadísticas básicas (conteo, media, desviación estándar, mínimo y máximo)
- Ejecución en tres diferentes modelos de paralelismo
- Número configurable de hilos e iteraciones

## Instalación

Para configurar el procesador de estadísticas descriptivas:

1. Clona el repositorio en tu máquina local:

git clone <URL_DEL_REPOSITORIO>
cd <CARPETA_DEL_REPOSITORIO>
Construye la imagen de Docker:

docker build -t descriptive-stats .

## Uso
Ejecuta el contenedor con límites específicos de memoria y CPU:
docker run --rm --memory="<LIMITE_DE_MEMORIA>" --cpus="<LIMITE_DE_CPU>" -v $(pwd)/datos_csv:/app/so_data -v $(pwd)/resultados_csv:/app/outcsv estadisticas-descriptivas <MODELO> <HILOS> <ITERACIONES>
<LIMITE_DE_MEMORIA>: La memoria máxima asignada al contenedor (por ejemplo, "1g" para 1 GB).
<LIMITE_DE_CPU>: La cantidad de núcleos de CPU asignados al contenedor (por ejemplo, "2" para 2 núcleos).
<MODELO>: Modelo de paralelismo (1 para secuencial, 2 para archivos paralelos, 3 para funciones paralelas).
<HILOS>: Número de hilos para el procesamiento paralelo.
<ITERACIONES>: Número de iteraciones a realizar.

## Comando de Ejemplo
Para ejecutar la aplicación con un límite de 1 GB de RAM y 2 núcleos de CPU, procesando en modo paralelo de archivos con 4 hilos durante 10 iteraciones:

docker build -t descriptive-stats .

docker run --rm --memory="1g" --cpus="2" descriptive-stats 2 4 10

asi nos genera el csv esa es la diferencia entre este y el anterior:

docker run --rm --memory="1g" --cpus="2" -v $(pwd)/so_data:/app/so_data -v $(pwd)/outcsv:/app/outcsv descriptive-stats 1 2 10

## Explicación de los Resultados
La aplicación muestra el tiempo de procesamiento para cada iteración, así como el tiempo promedio después de completar todas las iteraciones.


Keneth Ruiz 20210104
Juan Luis Fernandez 20200112
