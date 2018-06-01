import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import xlwt
import xlrd
from xlutils.copy import copy
import glob
import os.path
import time



class grafresultados(object):
    def __new__(cls, RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas):

        if (os.path.isfile(SOURCES_FOLDER_PATH + "truth.txt")):
            listasolreal = list()
            listacarpetas = list()
            soluciones = open(SOURCES_FOLDER_PATH + "truth.txt", "r")
            for linea in soluciones.readlines():
                # print linea
                if linea != '':
                    carpeta, solucion = linea.split(" ")
                    listacarpetas.append(carpeta)
                    listasolreal.append(solucion)
            soluciones.close()
        else:
            print("El archivo de soluciones no existe en la carpeta: \n " + SOURCES_FOLDER_PATH)
            # devolver error

        identificador=len(listacarpetas)
        dataDOCODE = xlrd.open_workbook(RESULT_FOLDER_PATH +'ResultDOCODE.xls')
        dataDOCODE_NORM = xlrd.open_workbook(RESULT_FOLDER_PATH +'ResultDOCODENORM.xls')
        dataDOCODE_SEG = xlrd.open_workbook(RESULT_FOLDER_PATH +'ResultDOCODENORM-POR-SEG.xls')

        table1 = dataDOCODE.sheets()[0]
        table2 = dataDOCODE_NORM.sheets()[0]
        table3 = dataDOCODE_SEG.sheets()[0]
        #print("table1: "+str(table1))


        #lmdas filas i
        #identificador columnas j

        lista_trace = list()
        lista_x = list()
        lista_y = list()
        for j in range(identificador):
            #print("revisando fila: "+str(j+1)+" con columna: "+str(3))
            solucion=table1.cell(j+1,1).value
            solucion = solucion.rstrip('\n')
            solucion=solucion.replace(" ","")
            valor = table1.cell(j+1, 2).value
            #print(str(valor))
            sol=str(solucion).strip()
            if sol == 'Y' or sol == 'T':
                lista_y.append("V")
            if sol == 'N' or sol == 'F':
                lista_y.append("F")
            lista_x.append(valor)

        #print(str(lista_y))
        trace = go.Scatter(

            x=lista_x,
            y=lista_y,
            mode ='markers'
        )
        lista_trace.append(trace)
        #print(str(lista_trace))
        data=lista_trace
        result = plotly.offline.plot(data, filename=RESULT_FOLDER_PATH+'DOCODE-pertenencia'+time.strftime("%d-%m-%y-%H-%M-%S") + '.html')
        print(str(result))

        # DOCODE NORMALIZADO

        lista_trace = list()

        for i in range(len(lmdas)):
            lista_x = list()
            lista_y = list()
            #print("lmdas: " + str(lmdas[i]))
            for j in range(identificador):
                #print("revisando fila: " + str(j+1) + " con columna: " + str(i+2))
                solucion = table2.cell(j + 1, 1).value
                solucion = solucion.rstrip('\n')
                solucion = solucion.replace(" ", "")
                valor = table2.cell(j+1, i+2).value

                sol = str(solucion).strip()
                if sol == 'Y' or sol == 'T':
                    lista_y.append("V")
                if sol == 'N' or sol == 'F':
                    lista_y.append("F")
                lista_x.append(valor)

            #print(str(lista_y))
            trace = go.Scatter(
                name='lmda '+str(lmdas[i]),
                x=lista_x,
                y=lista_y,
                mode='markers'
            )
            lista_trace.append(trace)

        data = lista_trace
        result = plotly.offline.plot(data, filename=RESULT_FOLDER_PATH + 'DOCODE-NORM-pertenencia' + time.strftime("%d-%m-%y-%H-%M-%S") + '.html')
        print(str(result))

        # DOCODE NORMALIZADO POR SEGMENTO

        lista_trace = list()

        for i in range(len(lmdas)):
            lista_x = list()
            lista_y = list()
            #print("lmdas: " + str(lmdas[i]))
            for j in range(identificador):
                # print("revisando fila: " + str(j+1) + " con columna: " + str(i+2))
                solucion = table3.cell(j + 1, 1).value
                solucion = solucion.rstrip('\n')
                solucion = solucion.replace(" ", "")
                valor = table3.cell(j + 1, i + 2).value

                sol = str(solucion).strip()
                if sol == 'Y' or sol == 'T':
                    lista_y.append("V")
                if sol == 'N' or sol == 'F':
                    lista_y.append("F")
                lista_x.append(valor)

            #print(str(lista_y))
            trace = go.Scatter(
                name='lmda ' + str(lmdas[i]),
                x=lista_x,
                y=lista_y,
                mode='markers'
            )
            lista_trace.append(trace)

        data = lista_trace
        result = plotly.offline.plot(data, filename=RESULT_FOLDER_PATH + 'DOCODE-NORM-SEG-pertenencia' + time.strftime("%d-%m-%y-%H-%M-%S") + '.html')
        print(str(result))

