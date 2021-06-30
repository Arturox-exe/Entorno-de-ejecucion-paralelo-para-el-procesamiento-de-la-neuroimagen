import json
import os
import time
import threading
import psutil
import pandas as pd
from pathlib import Path
import math

inicio_de_tiempo_total = time.time()


#Los ordena por numero de correlaciones
def selectionFirst(aList):
	for i in range(len(aList)):
		least = i
		for k in range(i+1, len(aList)):

			checker1 = "no"
			checker2 = "no"

			for l in range(0, counter_script):
				if(aList[least] == matriz[l][0]):
					aux1 = matriz[l][counter_script]
					checker1 = "yes"

				if(aList[k] == matriz[l][0]):
					aux2 = matriz[l][counter_script]
					checker2 = "yes"

				if(checker1 == "yes" and checker2 == "yes"):
					checker1 = "no"
					checker2 = "no"
					if(aux1 > aux2):
						
						least = k

		swap(aList, least, i)

#Los ordena dependiendo de si estan correlacionados unos con otros

def selectionSort(aList):
	for i in range(len(aList)):
		least = i
		for k in range(i+1, len(aList)):

			for l in range(0, counter_script):
				if(aList[least] == matriz[l][0]):
					
					
					for m in range(1, counter_script):

						
						
						if(aList[k] == matriz[l][m]):
							
							least = k

		swap(aList, least, i)

#Cambio de valores 

def swap(A, x, y):
    temp = A[x]
    A[x] = A[y]
    A[y] = temp

#Ejecucion serial

def serial_execution(serial_array):

	for i in range(len(serial_array)):
		
		script(i)

#Iniciar Script

def script(i):



	total_input_split_united = ""
	total_output_split_united = ""

	for j in range (len(ex_inputstuff[i])):
		input_split_united = ""
		
		input_split = ex_inputstuff[i][j].split("/")
		if(ex_inputstuff[i][j].startswith('temporal')):
			directory = ""
			input_split[1] = lista_split[0]
		else:

			"""                               INDICAR EN LA VARIABLE directory DONDE SE ENCUENTRAN LOS DATOS QUE LOS PROGRAMAS VAN A UTILIZAR                                   """

			directory = "data/"
			
			input_split[0] = lista_split[0]
		for k in range(len(input_split)):
			if(k ==0):
				input_split_united = directory + input_split_united + input_split[k]
			else:
				input_split_united =   input_split_united + "/" + input_split[k]

		total_input_split_united = total_input_split_united + input_split_united + " "

	for j in range (len(ex_outputstuff[i])):
		output_split_united = ""
		
		output_split = ex_outputstuff[i][j].split("/")
					
		output_split[1] = lista_split[0]
		
		for k in range(len(output_split)):
			if(k ==0):
				output_split_united =  output_split_united + output_split[k]
			else:
				output_split_united =   output_split_united + "/" + output_split[k]

		total_output_split_united = total_output_split_united + output_split_united + " "


	print()
	print("**************************************EJECUTANDO***************************************: " + str(array_sort[i]) + " - " + lista_split[0])
	print()
	os.system(directory_scripts +  str(array_sort[i]) + " " + total_input_split_united + total_output_split_united)
	print()
	print("**************************************TERMINADO***************************************: " + str(array_sort[i])+ " - " + lista_split[0])
	print()

#Ejecucion pararela

def pararel_execution(pararel_array):

	global bloque
	bloque = 0
	threads = list()

	
	counter_pararela = 0

	#Se cogen todos menos uno para ver CPUs porcentajes 
	number_cores = psutil.cpu_count() - 1
	
	counter_aux_pararela = 0
	done_0 = 0
	

	if(not os.path.isdir('temporal/' + lista_split[0])):
		os.makedirs('temporal/' + lista_split[0])	

	

	for i in range(len(pararel_array)):


		done_x = 0
		first_script = 0
		first_script_counter = 0
		aux_number_cores = 0
		aux_counter_pararela = 0
		


		#Solo ejecuta las que no tienen ninguna correlacion
		while(done_0 == 0 and aux_number_cores == 0):
				
			for j in range(len(pararel_array)):
				#Comprobar si se estan usando todos los hilos
				if(aux_counter_pararela < number_cores):
					if(pararel_array[counter_pararela] == matriz[j][0] and matriz[j][counter_script] == 0):
						
						

						if(counter_pararela < counter_script):
							counter_pararela = counter_pararela + 1
							aux_counter_pararela = aux_counter_pararela + 1
						else:
							done_0 = 1
							done_x = 1						
					else:
						done_0 = 1
						done_x = 1

				else: 
					aux_number_cores = 1

		#Ejecucion de los que tienen al menos una correlacion
		while(done_0 == 1 and done_x == 0 and aux_number_cores == 0):
			

			#Si es el primer script que cogemos de esta ejecucion
			if(first_script_counter == 0):

				if(counter_pararela < counter_script):
					first_script = pararel_array[counter_pararela]
					counter_first_script = counter_pararela			
					counter_pararela = counter_pararela + 1
					aux_counter_pararela = aux_counter_pararela + 1
					

				else:
					done_x = 1

				first_script_counter = 1
	
		
			#Mirar las correlaciones del first_script con el siguiente script, si no tienen relacion
			# miran la correlacion del first_scritp con el tercero y el segundo con el tercero,
			# si no tienen relacion...	
			if(first_script_counter == 1):
				#Comprobar si se estan usando todos los hilos
				if(aux_counter_pararela < number_cores):
					if(counter_pararela < counter_script):

						aux_counter_first_script = counter_first_script
						se_puede = 0

						while(aux_counter_first_script < counter_pararela):
							for l in range(0, counter_script):
								if(pararel_array[counter_pararela] == matriz[l][0]):
											
									for m in range(1, counter_script):
										
										if(pararel_array[aux_counter_first_script] == matriz[l][m]):
											
											se_puede = 1

							aux_counter_first_script = aux_counter_first_script + 1

						if(se_puede == 0):
							
							counter_pararela = counter_pararela + 1
							aux_counter_pararela = aux_counter_pararela + 1
							

						else:
							
							done_x = 1

					else:
						
						done_x = 1

				else:
					aux_number_cores = 1





		scripts_threads = []

		

		#Va a ir ejecutando cada script en un hilo diferente dependiendo del bloque
		while(counter_aux_pararela < counter_pararela):
			t = threading.Thread(target = script, args=(counter_aux_pararela,) )
			threads.append(t)
			t.start()
			
			scripts_threads.append(array_sort[counter_aux_pararela])

			counter_aux_pararela = counter_aux_pararela + 1

			if(counter_aux_pararela == counter_pararela):
				thread_checker = 1


		#Cuando estan todo los scripts ejecutandose, se empieza a ejecutar el monitoreo
		if(thread_checker == 1):
			thread_checker = 0
			
			d = threading.Thread(target = monitoring, args=( scripts_threads, ) )
	
			
		
			d.start()

			


			

		for t in threads:
			t.join()
		

				
		if(t.is_alive() == False):
			global stop_threads_global
			stop_threads_global = True
			
			
			



			
		d.join()
		
#Guarda la informacion de los scripts que se han ejecutado

def monitoring(lista_monitores ):

	global bloque
	global stop_threads_global
	global counter_csv_global
	stop_threads_global = False
	 

		

	while(True):
		
		timestamp = int(time.time())

		porcentaje = psutil.cpu_percent(interval=1)

		ram_porcentaje = psutil.virtual_memory().percent
		
		df.loc[counter_csv_global]=[ timestamp , porcentaje,  lista_monitores ,  len(lista_monitores), bloque, ram_porcentaje]
			
		counter_csv_global = counter_csv_global + 1
		

		if stop_threads_global:
			bloque = bloque + 1
			break

"""                          INDICAR EN VARIABLE directory_scripts CON QUE COMPILIDAR SE VAN A EJECUTAR Y DONDE SE ENCUENTRAN LOS PROGRAMAS QUE SE VAN A UTILIZAR                             """

directory_scripts = "python2 scripts/"
fileName = 'data.csv'
fileObj = Path(fileName)



e = open ('list.txt','r')
lista = e.read()
lista_split = lista.split()

# Opening JSON file 
with open('scheme.json', ) as f:
	data = json.load(f) 
global inputstuff
scriptsuff = []
inputstuff = []
outputstuff = []

for i in data:
	scriptsuff.append(i['script'])
	inputstuff.append(i['input_files'])
	outputstuff.append(i['output_files'])

#Si es la primera ejecución, y no hay un archivo csv

if(not fileObj.is_file()):		

	#Creacion de la matriz
	counter_script = len(scriptsuff)
	matriz = []
	for i in range(counter_script):
		matriz.append([0] * (counter_script+1))
		matriz[i][0] = scriptsuff[i]


	"""Comprobar si estos fors se les pueden hacer mas pequeños"""

	#Mete todos los scripts en la matriz ademas de crear el grafo

	for i in range(0, len(outputstuff)):
		for j in range(0, len(outputstuff[i])):
			for k in range(0, len(inputstuff)):
				for l in range(0, len(inputstuff[k])):
					outputtext = outputstuff[i][j]
					inputtext = inputstuff[k][l]
					
					

					if inputtext == outputtext:


						#Añadir relaciones a la matriz
						for m in range(0, counter_script):
							
							if (matriz [m][0] == scriptsuff[k]):

								while_counter = 1
								while_checker = 0
								
								while( while_counter < counter_script and while_checker == 0):

									if(scriptsuff[i] == matriz[m][while_counter]):
										while_checker = 1

									elif(matriz[m][while_counter] == 0):
										matriz[m][while_counter] = scriptsuff[i]
										while_checker = 1

									while_counter = while_counter + 1


	array_sort = []
	counter_sort = 0

	#Mete los scripts en una matriz diciendo su correlacion y poniendo a final de cada fila en numero de correlaciones con ese script
	#El primer valor sera el script y los siguientes los scripts necesarios para su ejecucion

	for i in range(0, counter_script):
		
		while_counter = 1
		while_checker = 0

		while(while_counter < counter_script  and while_checker == 0):

			if(matriz[i][while_counter] == 0):

				matriz[i][counter_script] = while_counter - 1

				array_sort.append(matriz[i][0])
				counter_sort = counter_sort + 1

				while_checker = 1

			while_counter = while_counter + 1


	df = pd.DataFrame( columns = ['Time' , 'CPU_Percentage', 'Scripts', 'Number_scripts', 'Bloque', 'RAM_Percentage'])
		

	stop_threads_global = False
	counter_csv_global = 1

	#Ordenamos el array
	selectionFirst(array_sort)
	selectionSort(array_sort)

	#Ordenamos los input y los output respecto array_sort
	ex_inputstuff = []
	ex_outputstuff = []

	for i in range(len(array_sort)):
		for j in range(len(scriptsuff)):
			if(scriptsuff[j] == array_sort[i]):
				ex_inputstuff.append(inputstuff[j])
				ex_outputstuff.append(outputstuff[j])





	#Ejecutarlo en paralelo

	inicio_de_tiempo = time.time()
	pararel_execution(array_sort)
	tiempo_final = time.time() 
	tiempo_transcurrido = tiempo_final - inicio_de_tiempo
	print ("\nEjecutarlo en pararelo fueron %d segundos." % (tiempo_transcurrido))




	df.to_csv('data.csv')
	
	
	#Quitando el primer elemento de la lista
	lista_split.pop(0)

	# Closing file 
	f.close() 

#Calcula las ejecuciones que se tienen que realizar en cada momento

def execution_number():

	data_csv = pd.read_csv(fileName)

	bloque_csv = data_csv.iloc[:, 5]
	indice_csv = data_csv.iloc[:, 0]
	cpu_csv = data_csv.iloc[:, 2]
	script_csv = data_csv.iloc[:, 3]
	ram_csv = data_csv.iloc[:, 6]

	global scipts_ejecutar
	indice = 0
	posible_ejecucion = []
	max_bloque = bloque_csv[len(data_csv.index)-1]
	scipts_ejecutar = []

	for i in range(max_bloque + 1):
		aux_csv = True
		total_cpu = 0
		total_ram = 0
		aux_bloque = bloque_csv[indice]
		first_indice = indice
		scipts_ejecutar.append(script_csv[indice])

		while(aux_csv):
			if(aux_bloque < bloque_csv[indice] or indice > (len(data_csv.index) - 2)):
				aux_csv = False
				media = total_cpu / (indice - first_indice + 1)
				posible_ejecucion_cpu_aux = 100 / media				
				posible_ejecucion_cpu_aux = 23
				media_ram = total_ram / (indice - first_indice + 1)
				posible_ejecucion_ram_aux = 100 / media_ram
				

				
				time_file.write(str(bloque_csv[indice]) + ": " + str(posible_ejecucion_cpu_aux) + " - " + str(posible_ejecucion_ram_aux) + "\n" )

				if(posible_ejecucion_cpu_aux < posible_ejecucion_ram_aux):
					posible_ejecucion_aux = posible_ejecucion_cpu_aux
				else:
					posible_ejecucion_aux = posible_ejecucion_ram_aux

				posible_ejecucion.append(math.floor(posible_ejecucion_aux))
			
			else:
				

				total_ram = total_ram + ram_csv[indice]
				total_cpu = total_cpu + cpu_csv[indice]
			
			
			indice = indice + 1
		

	return posible_ejecucion

#Ejecutar la lista que se ha generado

def execution_list(i, z):
	
	total_input_split_united = ""
	total_output_split_united = ""

	for j in range (len(inputstuff[i])):
		input_split_united = ""
		
		input_split = inputstuff[i][j].split("/")
		if(inputstuff[i][j].startswith('temporal')):
			directory = ""
			input_split[1] = aux_lista[z]
		else:
			"""                               INDICAR EN LA VARIABLE directory DONDE SE ENCUENTRAN LOS DATOS QUE LOS PROGRAMAS VAN A UTILIZAR                                   """

			directory = "data/"
			
			input_split[0] = aux_lista[z]
		for k in range(len(input_split)):
			if(k ==0):
				input_split_united = directory + input_split_united + input_split[k]
			else:
				input_split_united =   input_split_united + "/" + input_split[k]

		total_input_split_united = total_input_split_united + input_split_united + " "

	for j in range (len(outputstuff[i])):
		output_split_united = ""
		
		output_split = outputstuff[i][j].split("/")
					
		output_split[1] = aux_lista[z]
		
		for k in range(len(output_split)):
			if(k ==0):
				output_split_united =  output_split_united + output_split[k]
			else:
				output_split_united =   output_split_united + "/" + output_split[k]

		total_output_split_united = total_output_split_united + output_split_united + " "



	print()
	print("**************************************EJECUTANDO***************************************: " + str(scriptsuff[i]) + " - " + str(aux_lista[z]) )
	print()
	os.system(directory_scripts + str(scriptsuff[i]) + " " + total_input_split_united + total_output_split_united)
	print()
	print("**************************************TERMINADO***************************************: " + str(scriptsuff[i])+ " - " + str(aux_lista[z]))
	print()

#Crea un archivo que dira el tiempo de ejecucion
time_file = open("time_file.txt", "w")

numero_ejecuciones = execution_number()
time_file.write(str(numero_ejecuciones) + "\n")
global scipts_ejecutar


aux_lista = []

number_cores = psutil.cpu_count()

#A partir del archivo CSV lo interpreta para recoger los scripts a ejecutar
for i in range(len(numero_ejecuciones)):


	
	
	scipts_ejecutar[i] = scipts_ejecutar[i].replace('[', '')
	scipts_ejecutar[i] = scipts_ejecutar[i].replace(']', '')
	scipts_ejecutar[i] = scipts_ejecutar[i].replace(' ', '')
	scipts_ejecutar[i] = scipts_ejecutar[i].replace("'", '')

	scipts_ejecutars = scipts_ejecutar[i].split(",")

	



	indice_core = 0
	j = 0
	n_ejecucion = numero_ejecuciones[i]
	
	#Comprobacion de si hay suficientes nucleos
	while (j < len(lista_split)):
		if(number_cores > len(lista_split) and n_ejecucion > len(lista_split)):
			j = len(lista_split)
			aux_lista = lista_split

		else:	
			aux_lista.append(lista_split[j])
			indice_core = indice_core + 1
			j = j + 1
			

		if(indice_core >= number_cores or indice_core >= n_ejecucion or j == len(lista_split)):
			
			indice_core = 0
						
	

			time_file.write("\n" + str(scipts_ejecutars) + ": " + str(aux_lista) + " " +  str(numero_ejecuciones[i]))

			#Un thread para cada script a ejecutar
			threads = list()
			for k in range(len(aux_lista)):

				if(not os.path.isdir('temporal/' + aux_lista[k])):
					os.makedirs('temporal/' + aux_lista[k])	
					
				for l in range(len(scipts_ejecutars)):
					for m in range(len(scriptsuff)):
						if(scipts_ejecutars[l] == scriptsuff[m]):
							n = m
															
					t = threading.Thread(target = execution_list, args=(n,k,) )
					threads.append(t)
					t.start()

			#Se cierran los threads
			for t in threads:
				t.join()
			
				
			aux_lista = []

			tiempo_bloque = time.time() 
			tiempo_transcurrido_total = tiempo_bloque - inicio_de_tiempo_total
			time_file.write("\n" + "La ejecución hasta ahora fueron %d segundos." % (tiempo_transcurrido_total) + "\n")
		



tiempo_final_total = time.time() 
tiempo_transcurrido_total = tiempo_final_total - inicio_de_tiempo_total
time_file.write("\n" + "\n" + "La Ejecución total fueron %d segundos." % (tiempo_transcurrido_total))

time_file.close()

print ("\nLa Ejecución total fueron %d segundos." % (tiempo_transcurrido_total))

