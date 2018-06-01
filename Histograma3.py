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

class histogram3(object):
    def __new__(cls, RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes):

        # Crear excel para hacer trace
        text_prueba = open(RESULT_FOLDER_PATH + "Trace4.txt", "a")
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
        colors = ['rgba(0, 0, 255, 1)','rgba(200, 0, 0, 1)', 'rgba(0, 0, 255, 0.8)','rgba(200, 0, 0, 0.8)','rgba(0, 0, 255, 0.6)','rgba(200, 0, 0, 0.6)', 'rgba(0, 0, 255, 0.4)','rgba(200, 0, 0, 0.4)','rgba(0, 0, 255, 0.2)','rgba(200, 0, 0, 0.2)']

        lista_resultados_total = list()
        fila = 0
        lista_total = list()
        lista_resultados_true = list()
        lista_resultados_false = list()
        traces1=[]
        intento2 = list()
        for h in lmdas:
            intento2.append("lmda-" + str(h))
            #intento2.append(int(h))

        i = 0
        for columna in range(len(lmdas)):
            lista_true = list()
            lista_false = list()

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
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_true.append(valor)
                if sol == "F" or sol == "N":
                    lista_false.append(valor)

            traces1.append(go.Scatter(
                y=lista_true,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-'+str(a),
                line=dict(color=colors[i], shape='spline')

            ))
            traces1.append(go.Scatter(
                y=lista_false,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-' + str(a),
                line=dict(color=colors[i+1], shape='linear', dash='dashdot')
            ))
            i += 1
            if (i == 9):
                i = 0


        lista_resultados_true.append(lista_true)
        lista_resultados_false.append(lista_false)
        text_prueba.write("Lista total Verdadera: " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista total Falsas   : " + str(lista_resultados_false) + "\n")


        # Graficar
        fig = go.Figure(data=traces1)
        fig['layout'].update(height=1200, width=1200, title='Pertencia Verdaderos vs Falsos')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'DOCODE-PuntosVyF.html')

        text_prueba.write(" DOCODE NORMALIZADO  \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM.xls')
        table2 = data2.sheets()[0]
        colors = ['rgba(0, 0, 255, 1)','rgba(200, 0, 0, 1)', 'rgba(0, 0, 255, 0.8)','rgba(200, 0, 0, 0.8)','rgba(0, 0, 255, 0.6)','rgba(200, 0, 0, 0.6)', 'rgba(0, 0, 255, 0.4)','rgba(200, 0, 0, 0.4)','rgba(0, 0, 255, 0.2)','rgba(200, 0, 0, 0.2)']

        lista_resultados_total = list()
        fila = 0
        lista_total = list()
        lista_resultados_true = list()
        lista_resultados_false = list()
        traces1=[]
        intento2 = list()
        for h in lmdas:
            intento2.append("lmda-" + str(h))
            #intento2.append(int(h))

        i = 0
        for columna in range(len(lmdas)):
            lista_true = list()
            lista_false = list()

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
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_true.append(valor)
                if sol == "F" or sol == "N":
                    lista_false.append(valor)

            traces1.append(go.Scatter(
                y=lista_true,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-'+str(a),
                line=dict(color=colors[i], shape='spline')

            ))
            traces1.append(go.Scatter(
                y=lista_false,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-' + str(a),
                line=dict(color=colors[i+1], shape='linear', dash='dashdot')
            ))
            i += 1
            if (i == 9):
                i = 0


        lista_resultados_true.append(lista_true)
        lista_resultados_false.append(lista_false)
        text_prueba.write("Lista total Verdadera: " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista total Falsas   : " + str(lista_resultados_false) + "\n")


        # Graficar
        fig = go.Figure(data=traces1)
        fig['layout'].update(height=1200, width=1200, title='Pertencia Verdaderos vs Falsos')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'DOCODE-NOR-PuntosVyF.html')

        text_prueba.write(" DOCODE NORMALIZADO POR SEGMENTO  \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM-POR-SEG.xls')
        table2 = data2.sheets()[0]
        colors = ['rgba(0, 0, 255, 1)','rgba(200, 0, 0, 1)', 'rgba(0, 0, 255, 0.8)','rgba(200, 0, 0, 0.8)','rgba(0, 0, 255, 0.6)','rgba(200, 0, 0, 0.6)', 'rgba(0, 0, 255, 0.4)','rgba(200, 0, 0, 0.4)','rgba(0, 0, 255, 0.2)','rgba(200, 0, 0, 0.2)']

        lista_resultados_total = list()
        fila = 0
        lista_total = list()
        lista_resultados_true = list()
        lista_resultados_false = list()
        traces1=[]
        intento2 = list()
        for h in lmdas:
            intento2.append("lmda-" + str(h))
            #intento2.append(int(h))

        i = 0
        for columna in range(len(lmdas)):
            lista_true = list()
            lista_false = list()

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
                if sol == "T" or sol == "V" or sol == "Y":
                    lista_true.append(valor)
                if sol == "F" or sol == "N":
                    lista_false.append(valor)

            traces1.append(go.Scatter(
                y=lista_true,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-'+str(a),
                line=dict(color=colors[i], shape='spline')

            ))
            traces1.append(go.Scatter(
                y=lista_false,
                #x=intento2,
                mode='lines+markers',
                name='lmdas-' + str(a),
                line=dict(color=colors[i+1], shape='linear', dash='dashdot')
            ))
            i += 1
            if (i == 9):
                i = 0


        lista_resultados_true.append(lista_true)
        lista_resultados_false.append(lista_false)
        text_prueba.write("Lista total Verdadera: " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista total Falsas   : " + str(lista_resultados_false) + "\n")


        # Graficar
        fig = go.Figure(data=traces1)
        fig['layout'].update(height=1200, width=1200, title='Pertencia Verdaderos vs Falsos')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'DOCODE-NOR-SEG-PuntosVyF.html')