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

## Respuesta de preguntas:
1)¿Cuál es el modelo de paralelismo más rápido en los 6 escenarios?
 - El modelo de 4 cores y 8 hilos ha demostrado ser el más rápido en la mayoría de los escenarios de prueba, lo que sugiere que un mayor número de hilos puede manejar eficazmente las cargas de trabajo intensivas en datos y computación distribuida.     Este modelo maximiza el uso del hardware disponible para reducir significativamente el tiempo de procesamiento en comparación con configuraciones de menos cores e hilos.
   
2)¿Cuál opción modelo de paralelismo tomaría usted y por qué?
 - Elegiría el modelo con 2 Cores y 4 Hilos (2C4H), ya que ofrece un buen equilibrio entre rendimiento y consumo de recursos. Este modelo proporciona una mejora significativa en el tiempo de procesamiento comparado con el modelo de 1 Core, sin         necesitar una escalabilidad a tantos cores, lo que puede ser más costoso y menos eficiente energéticamente para ciertas aplicaciones.
   
3)¿Recomendaría paralelizar tanto archivos como funciones al mismo tiempo?

- Si bien la paralelización tanto de archivos como de funciones puede maximizar la utilización de los recursos en sistemas con alta disponibilidad de CPU y memoria, generalmente recomendaría paralelizar solo por archivos en la mayoría de los casos prácticos. Esto se debe a que la paralelización por archivos tiende a ofrecer mejoras más consistentes y predecibles sin introducir la complejidad y el posible overhead que puede venir con la paralelización de funciones. Si los recursos no son una limitante, y el entorno soporta eficientemente ambas formas de paralelismo, entonces sí podría considerarse su implementación simultánea.
  
4) ¿Cuál es el factor de mejora de pasar de 1 Core a 2 Core para el proceso que paraleliza los archivos?
    Según los datos proporcionados, el tiempo de procesamiento mejora de 10.4726 segundos con 1 Core y 4 Hilos (1C4H) a 7.3087 segundos con 2 Cores y 4 Hilos (2C4H). El factor de mejora se calcula como:
    Archivos	Funciones	
    1C4H	10.4726	9.4303	
    2C4H	7.3087	9.3301
    Factor Mejora Archivos:	1.43289504		
    Factor Mejora Funciones:	1.01073943
  Esto indica que el rendimiento mejora en un 43% al duplicar el número de cores para el procesamiento de archivos.
  
5) Determine el factor teórico de mejora para el escenario de 2 Core (amdahl's law) al paralelizar por archivo
  Si estimamos que aproximadamente el 70% del proceso es paralelizable, el factor de mejora teórico usando la Ley de Amdahl sería:
  - 1.54
 Esto sugiere que teóricamente, el rendimiento puede mejorar hasta un 54% con 2 cores en comparación con 1, suponiendo una paralelización óptima.

6)Determine el factor teórico de mejora para el escenario de 2 Core (amdahl's law) al paralelizar por función estadística
  - 1.33
Esto indica que teóricamente, el rendimiento puede mejorar hasta un 33% con 2 cores para el procesamiento paralelo de funciones estadísticas, mostrando un beneficio menor comparado con la paralelización por archivos debido a una menor fracción paralelizable.

Keneth Ruiz 20210104
Juan Luis Fernandez 20200112
