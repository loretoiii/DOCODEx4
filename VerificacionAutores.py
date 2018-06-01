import numpy
import glob
import sys
import os
from text2 import TEXT
from graficame import grafico
from umbrales1 import umbral
from GraficarResultados import grafresultados
from MatrizConfusion import matriz
from Histograma import histogram
from Histograma2 import histogram2
from Histograma3 import histogram3
from Histograma4 import histogram4
from B0B1 import b0b1
import shutil
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout

#VARIABLES GLOBALES
SOURCES_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEx4/Sources/'
SOURCES_GRAF_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEx4/'
RESULT_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEx4/Results/'


if __name__ == "__main__":
    numero_carpetas=len(glob.glob(SOURCES_FOLDER_PATH+"*"))
    files_1 = glob.glob(SOURCES_FOLDER_PATH+'*')
    #Se definen los segmentos largos m-palabras
    m = 400 #Ventana
    n = 1 #n-grama
    probar = 0 
	# 0 = Carpeta de training, no hay segmento limintante. 
	# 1 = Carpeta de test, hay segmento y se debe cambiar las listas: lista1 para docode, lista2 docode normalizado y lista3 docode norm por segmento
 
    lista1 = list()
    lista2 = list()
    lista3 = list()
    if probar == 1:
        lista1 = [0,1,1,0,0,1,1,1,1,1]
        lista2 = [0,0,0,0,0,1,1,1,0,1]
        lista3 = [0,0,0,0,0,1,1,1,0,1]
    else:
        lista1 = [0]
        lista2 = [0]
        lista3 = [0]
	# lambdas a revisar
    lmdas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
             2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
    lista_porcentajes = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
	# Entrar en cada una de las carpetas que tengo y revisar los documentos
    path_folder = list()
    for i in files_1:
        if os.path.isdir(i):
            path_folder.append(i)

    dir_files = list()

    os.makedirs(RESULT_FOLDER_PATH+"n-"+str(n)+"-"+time.strftime("%d-%m-%y-%H-%M-%S")+"/")
    os.makedirs(RESULT_FOLDER_PATH +"n-"+str(n)+"-"+ time.strftime("%d-%m-%y-%H-%M-%S") + "/GraficosPorCarpeta")
    RESULT_FOLDER_PATH=RESULT_FOLDER_PATH+"n-"+str(n)+"-"+time.strftime("%d-%m-%y-%H-%M-%S")+"/"
    text_prueba=open(RESULT_FOLDER_PATH+ "Trace.txt","a")
    text_excel = open(RESULT_FOLDER_PATH + "Excel-detalle.txt", "w")
    text_prueba.write("Comienza prueba.\n")
    text_prueba.write("m:"+str(m)+" n:"+str(n)+"\n")

    for folder in path_folder:
        path_files = glob.glob(folder+'/*.txt')
        dir_files.append(path_files)

    identificador = 1
    for folder in dir_files:
        data_unknown = list()
        data_known = list()
        data_unknown_norm = list()
        data_known_norm = list()
        data_unknown_seg = list()
        data_known_seg = list()
        numero_columnas=len(folder)
        num_entradas = 1
        datos_analisis = list()

        for file in folder:
            filename = file.split('/')[-1]
            parent_dir = file.split('/')[-2]
            text_prueba.write("Revisando el archivo:"+str(filename)+".\n")
            if 'known' in filename and not 'part' in parent_dir:
                text_prueba.write("El archivo:" + str(filename) + " se revisara.\n")
                if num_entradas==1:
                    num_entradas=num_entradas+1
                text = TEXT(file, m, n)
                text_prueba.write("Palabras:"+str(text.total_words) + " en texto: " +str(filename)+"\n")
                text_excel.write(str(parent_dir)+" "+str(filename)+"\n")
                docode = text.docode(m)
                docode_normalizado = text.docode_normalizado(m)
                docode_normalizado_segmento=text.docode_normalizado_segmento(m)
                if not 'unknown' in filename:
                    data_known.append(docode)
                    data_known_norm.append(docode_normalizado)
                    data_known_seg.append(docode_normalizado_segmento)
                else:
                    data_unknown.append(docode)
                    data_unknown_norm.append(docode_normalizado)
                    data_unknown_seg.append(docode_normalizado_segmento)
                #print "Segmentos: %s" % (len(docode['segments']))
                #print "Estilo: %f" % docode['style']

        # DOCODE
        # Data Conocida
        d_aux = []
        d_count = 0
        d_num = 1  # solo visible en archivo excel
        text_prueba.write("DOCODE \n")
        text_excel.write("DOCODE \n")
        lista_estilos_conocidos = list()
        matriz_docode = list()
        colum=1
        for i in data_known:
            # print 'estilo documento: %f' % i['style']
            text_prueba.write('DATA CONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            # print 'd de segmentos: '+str(i['differences'])
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            d_aux += i['differences']
            #print("colum-> "+str(colum-1)+" fila-> 0")
            #print(str(i['differences']))
            matriz_docode.append(i['differences'])
            #matriz_dif[colum-1][0]=i['differences']
            lista_estilos_conocidos.append(i['style'])
            #print "lista estilo --> "+str(lista_estilos_conocidos)
            text_excel.write("archivo" + str(colum) + ", ," + str(i['style']) + "," + str(i['differences']) + "\n")
            d_num = d_num + 1
            colum = colum + 1

        if len(d_aux):
            #print "lista estilo --> " + str(lista_estilos_conocidos)
            #datos_analisis.append(lista_estilos_conocidos.append(i['style']))
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            std = numpy.std(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + '- promedio: ' + str(promedio) + " -")
            text_prueba.write(' desv: ' + str(std) + "\n")

        d_aux = []
        d_num = 1
        # Para la data del documento desconocido

        for i in data_unknown:
            # print 'estilo documento: %f' % i['style']
            # print 'd de segmentos: '+str(i['differences'])
            text_prueba.write('DATA DESCONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            text_excel.write("archivo" + str(d_num) + "," + str(i['style']) + ", ," + str(i['differences']) + "\n")
            d_aux += i['differences']
            #matriz_dif[colum - 1][0] = i['differences']
            matriz_docode.append(i['differences'])
            estilo_todos = numpy.average(lista_estilos_conocidos)
            # print "estilo todos --> "+str(estilo_todos)
            text_excel.write("archivo" + str(colum) +"," + str(estilo_todos) + ", " + str(i['style']) + "\n")
            lista_estilos_conocidos = list()

        if len(d_aux):
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + ' -estilo doc desconocido: ' + str(promedio) + "\n")

        #print(str(matriz_dif))
        #for c in range(colum):
         #   print(str(c))


        # DOCODE NORMALIZADO
        # Data Conocida
        d_aux = []
        d_count = 0
        d_num = 1  # solo visible en archivo excel
        text_prueba.write("DOCODE NORMALIZADO \n")
        text_excel.write("DOCODE NORMALIZADO \n")
        lista_estilos_conocidos = list()
        matriz_docode_norm = list()
        colum = 1
        for i in data_known_norm:
            text_prueba.write('DATA CONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            d_aux += i['differences']
            matriz_docode_norm.append(i['differences'])
            lista_estilos_conocidos.append(i['style'])
            text_excel.write("archivo" + str(colum) + ", ," + str(i['style']) + "," + str(i['differences']) + "\n")
            d_num = d_num + 1
            colum = colum + 1

        if len(d_aux):
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            std = numpy.std(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + '- promedio: ' + str(promedio) + " -")
            text_prueba.write('desv: ' + str(std) + "\n")

        d_aux = []
        d_num = 1
        # Para la data del documento desconocido
        for i in data_unknown_norm:
            text_prueba.write('DATA DESCONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            text_excel.write("archivo" + str(colum) + "," + str(i['style']) + ", ," + str(i['differences']) + "\n")
            d_aux += i['differences']
            matriz_docode_norm.append(i['differences'])
            estilo_todos = numpy.average(lista_estilos_conocidos)
            text_excel.write("archivo" + str(colum) + "," + str(estilo_todos) + ", " + str(i['style']) + "\n")
            lista_estilos_conocidos = list()

        if len(d_aux):
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + ' -promedio doc desconocido: ' + str(promedio) + "\n")


        # DOCODE NORMALIZADO POR SEGMENTO
        # Data Conocida
        d_aux = []
        d_count = 0
        d_num = 1  # solo visible en archivo excel
        text_prueba.write("DOCODE NORMALIZADO POR SEGMENTO \n")
        text_excel.write("DOCODE NORMALIZADO POR SEGMENTO \n")
        lista_estilos_conocidos = list()
        matriz_docode_seg = list()
        colum = 1
        for i in data_known_seg:
            text_prueba.write('DATA CONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            d_aux += i['differences']
            matriz_docode_seg.append(i['differences'])
            lista_estilos_conocidos.append(i['style'])
            text_excel.write(
                "archivo" + str(colum) + ", ," + str(i['style']) + "," + str(i['differences']) + "\n")
            d_num = d_num + 1
            colum = colum + 1

        if len(d_aux):
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            std = numpy.std(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + '- promedio: ' + str(promedio) + " -")
            text_prueba.write('desv: ' + str(std) + "\n")

        d_aux = []
        d_num = 1
        # Para la data del documento desconocido
        for i in data_unknown_seg:
            text_prueba.write('DATA DESCONOCIDA - estilo documento: ' + str(i['style']) + "\n")
            text_prueba.write('d de segmentos: ' + str(i['differences']) + "\n")
            text_excel.write("archivo" + str(colum) + "," + str(i['style']) + ", ," + str(i['differences']) + "\n")
            d_aux += i['differences']
            matriz_docode_seg.append(i['differences'])
            estilo_todos = numpy.average(lista_estilos_conocidos)
            text_excel.write("archivo" + str(colum) + "," + str(estilo_todos) + ", " + str(i['style']) + "\n")
            lista_estilos_conocidos = list()

        if len(d_aux):
            promedio = numpy.average(d_aux)
            mediana = numpy.median(d_aux)
            text_prueba.write('mediana: ' + str(mediana) + ' -promedio doc desconocido: ' + str(promedio) + "\n")

        #print(str(matriz_docode))
        #print(str(matriz_docode_norm))
        #print(str(matriz_docode_seg))

        #Si la matriz existe, ninguna de las 3 estara vacia
        text_prueba.write('\n Matriz DOCODE: ' + str(matriz_docode) + "\n")
        if matriz_docode:
            #print(str(parent_dir))
            #print(str(identificador))
            text_prueba.write("Hare grafico ... ir a Trace 2 :\n")
            nombre_archivo = grafico(matriz_docode, matriz_docode_norm, matriz_docode_seg,str(parent_dir),RESULT_FOLDER_PATH)
            umbral(matriz_docode, matriz_docode_norm, matriz_docode_seg, identificador, RESULT_FOLDER_PATH, lmdas)
            print("OK "+str(nombre_archivo))
        #print(str(identificador))
        identificador = identificador + 1

    text_excel.close()
    text_prueba.close()
    ## Llamar a graficar resultados
    grafresultados(RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH,lmdas)
    matriz(RESULT_FOLDER_PATH, lmdas, lista_porcentajes)
    histogram(RESULT_FOLDER_PATH,SOURCES_FOLDER_PATH, lmdas, lista_porcentajes)
    histogram2(RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes)
    #histogram3(RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes)
    #histogram4(RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes)

    b0b1(RESULT_FOLDER_PATH, lmdas, lista_porcentajes, probar, lista1,lista2,lista3)

    sys.exit()