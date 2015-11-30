# Ejemplo de multiprocessing #

El script abre un fichero csv de entrada y para cada una de las filas extrae el nombre de domino almacenado en la sexta columna. Para cada uno de estos valores hace una comprobación, solicitando el recurso tanto por http como por https, y almacena los resultados de las consultas en un fichero csv de salida.

El script `check_domains_1.py` ejecuta el proceso de forma secuencial, es decir, un dominio después de otro. En el peor de los casos la espera de la respuesta se demorará 5 segundos tras lo que devolverá un error de timeout y continuará con el siguiente.

El script `check_domains_2.py` ejecuta el proceso lanzando tantas consultas paralelas como núcleos tenga la maquina en que se ejecuta el script. Para ello primero lee el fichero csv y genera una *queue* con los dominios a comprobar y otra *queue* para los resultados obtenidos. Una vez almacenados todos los valores en memoria los procesos van extrayendo los datos de la queue de entrada y almacenando los resultados en la queue de salida; cuando todos los elementos han sido procesados se escriben los resultados.

La mejora de la segunda versión (que utiliza multiprocessing) con respecto a la primera (que se ejecuta secuencialmente) es bastante notable :-)

**Referencias:**

[Multiprocessing with Python](http://www.ibm.com/developerworks/aix/library/au-multiprocessing/ "Multiprocessing with Python")

[http://stackoverflow.com/questions/2359253/solving-embarassingly-parallel-problems-using-python-multiprocessing](http://stackoverflow.com/questions/2359253/solving-embarassingly-parallel-problems-using-python-multiprocessing "Solving embarassingly parallel problems using Python multiprocessing")
 