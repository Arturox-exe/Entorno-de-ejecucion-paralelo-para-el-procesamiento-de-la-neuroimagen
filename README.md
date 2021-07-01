# Entorno de ejecución paralelo para el procesamiento de la neuroimagen

Este proyecto es en Proyecto Fin de Grado elaborado en el curso 2020-2021 en la Universidad Carlos III de Madrid. Este programa sirve para la creación de workflows dependiendo de las características del ordenador donde se ejecute, fue testeado para procesamiento de neuroimágenes. Para su ejecución es necesario tener instalado Python 3.

### Librerías necesarias
Para la ejecución de este proyecto son necesarias las siguientes librerías de Python 3:
- json
- os
- time
- threading
- psutil
- pandas
- pathlib
- math

### Como hacer funcionar el programa
Los archivos y carpetas de este proyecto que no sean main.py son ejemplos para hacer funcionar el proyecto, por lo que hay que hay que seguir los siguientes pasos:
- Hay que modificar el archivo "scheme.json" para indicar los programas que se quieren ejecutar y los input y output que generará, siguiendo el ejemplo que hay dentro del mismo archivo.
- En la carpeta "scripts" hay que guardar los archivos que se quieren ejecutar, en un principio se ejecutar con Python 2, si no se quieren ejecutar con este compilador o se quiere ejecutar desde otra carpeta, mirar en el apartado "Otros datos a tener en cuenta".
- En la carpeta "data" hay que guardar los inputs necesarios para ejecutar los programas en carpetas independientes, si no se quieren leer desde otra carpeta, mirar en el apartado "Otros datos a tener en cuenta".
- En el archivo "list.txt", hay que indicar cuales de los archivos guardados en data se quieren utilizar, separados por espacios.
- El archivo "data.csv" se tiene que borrar o cambiar de carpeta cada vez que se quiera realizar la ejecución en un nuevo ordenador o cambiar los programas que se quieren ejecutar.

Los archivos "time_file.txt" y la carpeta "temporal", son ejemplos de lo que generará al terminar la ejecución, por lo que se pueden borrar si se desea.

### Otros datos a tener en cuenta
No es necesario utilizar las carpetas "scripts" y "data" si no se desea, tampoco usar Python 2 para ejecutar los programas. Para cambiar de carpeta o el compilador es necesario modificar el código de "main.py"
- Cambiar la carpeta data - Hay que cambiar la ubicación de la carpeta en la variable "directory" en la línea 96 y en la línea 548.
- Cambiar la carpeta scripts o compilador - Hay que cambiar la viriable "directory_scripts" en la línea 333, primero indicando con que se quiere ejecutar y después la ubicación de la carpeta.
