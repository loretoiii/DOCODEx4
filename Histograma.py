import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import xlwt
import xlrd
from xlutils.copy import copy
import glob
import os.path
import time

class histogram(object):
    def __new__(cls, RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes):

        # Crear excel para hacer trace
        text_prueba = open(RESULT_FOLDER_PATH + "Trace3.txt", "a")
        text_prueba.write("\n \n Comienzo a revisar HISTORGRAMA. \n")

        # Crear listas de cantidades de verdaderas y falsas por porcentaje analizado
        soluciones = open(SOURCES_FOLDER_PATH + "truth.txt", "r")
        lista_true = list()
        lista_false = list()

        listasolreal = list()
        listacarpetas = list()
        for linea in soluciones.readlines():
            # print linea
            if linea != '':
                carpeta, solucion = linea.split(" ")
                listacarpetas.append(carpeta)
                listasolreal.append(solucion)
        soluciones.close()

        text_prueba.write(" DOCODE  \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODE.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()

        fila = 0
        lista_true = list()
        lista_false = list()
        lista_total = list()
        for columna in range(len(lmdas)):
            cant_true = 0
            cant_false = 0
            cant_total = 0
            lista_t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            lista_f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                a = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(a) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if(float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + "\n")
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_t[arr] += 1

                if sol == "F" or sol == "N":
                    lista_f[arr] += 1
            lista_true.append(lista_t)
            lista_false.append(lista_f)
            text_prueba.write("Lista total Verdadera: " + str(lista_true) + "\n")
            text_prueba.write("Lista total Falsas   : " + str(lista_false) + "\n")


        # Histograma
        intento = list()
        intento = ['0 - 0.1','0.1 - 0.2','0.2 - 0.3','0.3 - 0.4','0.4 - 0.5','0.5 - 0.6','0.6 - 0.7','0.7 - 0.8','0.8 - 0.9','0.9 - 1']
        intento2 = list()
        for h in lmdas:
            intento2.append("l-" + str(h))

        trace1 = go.Heatmap(
            z=lista_true,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'
        )
        trace2 = go.Heatmap(
            z=lista_false,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'  # Cividis
        )

        text_prueba.write(" DOCODE NORMALIZADO \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()

        fila = 0
        lista_true = list()
        lista_false = list()
        lista_total = list()
        for columna in range(len(lmdas)):
            cant_true = 0
            cant_false = 0
            cant_total = 0
            lista_t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            lista_f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                a = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(a) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if(float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + "\n")
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_t[arr] += 1

                if sol == "F" or sol == "N":
                    lista_f[arr] += 1
            lista_true.append(lista_t)
            lista_false.append(lista_f)
            text_prueba.write("Lista total Verdadera: " + str(lista_true) + "\n")
            text_prueba.write("Lista total Falsas   : " + str(lista_false) + "\n")


        # Histograma
        trace3 = go.Heatmap(
            z=lista_true,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'
        )
        trace4 = go.Heatmap(
            z=lista_false,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'  # Cividis
        )
        text_prueba.write(" DOCODE NORMALIZADO POR SEGMENTO \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM-POR-SEG.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()

        fila = 0
        lista_true = list()
        lista_false = list()
        lista_total = list()
        for columna in range(len(lmdas)):
            cant_true = 0
            cant_false = 0
            cant_total = 0
            lista_t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            lista_f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                a = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(a) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if(float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + "\n")
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_t[arr] += 1

                if sol == "F" or sol == "N":
                    lista_f[arr] += 1
            lista_true.append(lista_t)
            lista_false.append(lista_f)
            text_prueba.write("Lista total Verdadera: " + str(lista_true) + "\n")
            text_prueba.write("Lista total Falsas   : " + str(lista_false) + "\n")


        # Histograma
        trace5 = go.Heatmap(
            z=lista_true,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'
        )
        trace6 = go.Heatmap(
            z=lista_false,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Cold'  # Cividis
        )

        # Graficar
        #
        fig = tools.make_subplots(rows=3, cols=2,subplot_titles=('V-D', 'F-D', 'V-DNor', 'F-DNor', 'V_DNSeg', 'F-DNSeg'))
        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2, 1, 2)
        fig.append_trace(trace3, 2, 1)
        fig.append_trace(trace4, 2, 2)
        fig.append_trace(trace5, 3, 1)
        fig.append_trace(trace6, 3, 2)
        fig['layout'].update(height=1200, width=1200, title='Verdaderos vs Falsos')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'Hist-VvsF-TODOS.html')



