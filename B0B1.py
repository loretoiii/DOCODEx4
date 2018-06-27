import xlwt
import xlrd
from xlutils.copy import copy
import mpmath
import numpy
import time
import os.path
import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go


SOURCES_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Sources/'

class b0b1(object):
    def __new__(cls, RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes, probar, lista1, lista2, lista3 ):

        # Abrir archivo para leer
        file = open(RESULT_FOLDER_PATH + "Resultados.txt", "r")
        soluciones = open(SOURCES_FOLDER_PATH + "truth.txt", "r")

        # Crear excel para hacer trace
        text_prueba = open(RESULT_FOLDER_PATH + "Trace5.txt", "a")
        text_prueba.write("\n \n Comienzo a revisar B0B1. \n")

        listasolreal = list()
        listacarpetas = list()
        for linea in soluciones.readlines():
            # print linea
            if linea != '':
                carpeta, solucion = linea.split(" ")
                listacarpetas.append(carpeta)
                listasolreal.append(solucion)
        soluciones.close()

        ##DOCODE
        text_prueba.write(" DOCODE  \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODE.xls')
        table2 = data2.sheets()[0]


        lista_todos_vof = list()
        lista_todos_cantidad_vof = list()
        lista_cant_total = list()
        for columna in range(len(lmdas)):
            lista_porcentaje_puntaje_total = list()
            lista_vof = list()
            cantidad_total=0
            for por in lista_porcentajes:

                text_prueba.write("Revisando el porcentaje: " + str(por) + "\n")
                if (por == lista_porcentajes[0]):
                    por_anterior = 0
                    tof_ant = 2
                else:
                    cant_true = 0
                    cant_false = 0
                    cant_total = 0
                    for filas in range(len(listacarpetas)):
                        text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                        solreal = table2.cell(filas + 1, 1).value
                        lmda = table2.cell(0, columna + 2).value
                        valor = table2.cell(filas + 1, columna + 2).value
                        valor = valor.replace(" ", "")
                        sol = str(solreal).strip()
                        text_prueba.write("sol real: " + str(sol) + "\n")
                        text_prueba.write("lambda:" + str(lmda) + "\n")
                        text_prueba.write("valor:" + str(valor) + "\n")
                        text_prueba.write("Revisando  : " + str(por_anterior) + " >= "+str(valor)+" < "+str(por)+"\n")
                        ult = len(lista_porcentajes)
                        if(por!=lista_porcentajes[ult-1]):
                            if (float(por_anterior) <= float(valor) < float(por)):
                                text_prueba.write("Entro al if: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                        else:
                            if (float(por_anterior) <= float(valor)):
                                text_prueba.write("Entro al if del else: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                    text_prueba.write("Cant de Verdaderas  : " + str(cant_true) + "\n")
                    text_prueba.write("Cant de Falsas      : " + str(cant_false) + "\n")
                    if(cant_true > cant_false):
                        cant_total = cant_true
                        tof_ant = 1
                        lista_vof.append(tof_ant)
                    if (cant_true < cant_false):
                        cant_total = cant_false
                        tof_ant = 0
                        lista_vof.append(tof_ant)
                    if (cant_true == cant_false):
                        cant_total = cant_true
                        if (tof_ant==2):
                            tof_ant=1
                        lista_vof.append(tof_ant)

                    text_prueba.write("CantTotal(ganador)    : " + str(cant_total) + " - siendo V(1) o F(0): "+str(tof_ant)+"\n")
                    por_anterior=por
                    cantidad_total=cant_total+cantidad_total
                    lista_porcentaje_puntaje_total.append(cant_total)

            if(tof_ant!=2):
                lista_cant_total.append(cantidad_total)
            text_prueba.write("-------------------------------------------------------------------------------- \n")
            text_prueba.write("Con lamda  : " + str(lmda) + " - se tiene lista: "+str(lista_porcentaje_puntaje_total)+"\n")
            text_prueba.write("Lista VyF  : " + str(lista_vof) + "\n")
            text_prueba.write("Mejor Puntaje  : " + str(lista_cant_total) + "\n")
            lista_todos_vof.append(lista_vof)
            lista_todos_cantidad_vof.append(lista_porcentaje_puntaje_total)

        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("VyF  : " + str(lista_todos_vof) + "\n")
        text_prueba.write("Puntajes VyF  : " + str(lista_todos_cantidad_vof) + "\n")
        text_prueba.write("Mejores ptjes totales  : " + str(lista_cant_total) + "\n")

        intento = list()
        for t in lista_porcentajes:
            if(t==lista_porcentajes[0]):
                intento.append("0-0.1")
                t_ant=0
            else:
                intento.append(str(t_ant)+"-"+str(t))
                t_ant=t

        intento2 = list()

        for h in lmdas:
            intento2.append("lmda-" + str(h))

        i=0
        j_ant1=0
        t1 = 0
        for j in lista_cant_total:
            if i != 0:
                if (j>j_ant1):
                    j_ant1 = j
                    t1=i
            else:
                j_ant1=j
            i+=1

        text_prueba.write("Mejores ptjes de la lista : " + str(j_ant1) +" en lmda: "+str(lmdas[t1])+ "\n")
        trace1 = go.Heatmap(
            z=lista_todos_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas)/2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        trace2 = go.Heatmap(
            z=lista_todos_cantidad_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas)/2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )


        ## Para cada b_x sacar los F1

        lista_vyf =list()
        lista_F1 = list()
        lista_lista_F1 =list()
        for columna in range(len(lmdas)):
            if probar == 1:
                lista_vyf = lista1
            else:
                lista_vyf = lista_todos_vof[columna]

            TP_d1 = 0
            FN_d1 = 0
            FP_d1 = 0
            TN_d1 = 0
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                lmda = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(lmda) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if(float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + " - seria un V(1) o F(0): "+str(lista_vyf[arr])+"\n")
                if(lista_vyf[arr]==1):
                    d1 = "V"
                else:
                    d1 = "F"

                if sol == "T" or sol == "V" or sol == "Y":
                    if d1 == "V":
                        TP_d1 += 1

                    if d1 == "F":
                        FN_d1 += 1
                if sol == "F" or sol == "N":
                    if d1 == "V":
                        FP_d1 += 1
                    if d1 == "F":
                        TN_d1 += 1

            if (TP_d1 + FP_d1) != 0:
                precision_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FP_d1))
            else:
                precision_d1 = 0
            if (TP_d1 + FN_d1) != 0:
                recall_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FN_d1))
            else:
                recall_d1 = 0
            if (precision_d1 + recall_d1) != 0:
                F1_d1 = 2 * (mpmath.mpf(precision_d1 * recall_d1) / mpmath.mpf(precision_d1 + recall_d1))
            else:
                F1_d1 = 0
            lista_F1.append(str(F1_d1))

            lista_lista_F1.append(lista_F1)
            #lista_lista_F1.append(lista_cant_total[columna])
            text_prueba.write("TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
            text_prueba.write("F1: " + str(F1_d1) + "\n")
            #text_prueba.write("Revisando  : " + str(por_anterior) + " >= " + str(valor) + " < " + str(por) + "\n")

        text_prueba.write("F1: "+str(lista_F1)+"\n")

        lista_z = list()
        j = 0
        for i in lista_lista_F1:
            lista_resultados = list()
            lista_resultados.append(float(i[j]))
            cant_aciertos = lista_cant_total[j]
            lista_resultados.append(int(cant_aciertos))
            lista_z.append(lista_resultados)
            j += 1
        text_prueba.write("list z: " + str(lista_z) + "\n")

        trace3 = go.Heatmap(
            z=lista_z,
            x=['F1','#'],
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        #DOCODE NORMALIZADO
        text_prueba.write(" DOCODE NORMALIZADO \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM.xls')
        table2 = data2.sheets()[0]

        lista_todos_vof = list()
        lista_todos_cantidad_vof = list()
        lista_cant_total = list()
        for columna in range(len(lmdas)):
            lista_porcentaje_puntaje_total = list()
            lista_vof = list()
            cantidad_total = 0
            for por in lista_porcentajes:

                text_prueba.write("Revisando el porcentaje: " + str(por) + "\n")
                if (por == lista_porcentajes[0]):
                    por_anterior = 0
                    tof_ant = 2
                else:
                    cant_true = 0
                    cant_false = 0
                    cant_total = 0
                    for filas in range(len(listacarpetas)):
                        text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                        solreal = table2.cell(filas + 1, 1).value
                        lmda = table2.cell(0, columna + 2).value
                        valor = table2.cell(filas + 1, columna + 2).value
                        valor = valor.replace(" ", "")
                        sol = str(solreal).strip()
                        text_prueba.write("sol real: " + str(sol) + "\n")
                        text_prueba.write("lambda:" + str(lmda) + "\n")
                        text_prueba.write("valor:" + str(valor) + "\n")
                        text_prueba.write(
                            "Revisando  : " + str(por_anterior) + " >= " + str(valor) + " < " + str(por) + "\n")
                        ult = len(lista_porcentajes)
                        if (por != lista_porcentajes[ult - 1]):
                            if (float(por_anterior) <= float(valor) < float(por)):
                                text_prueba.write("Entro al if: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                        else:
                            if (float(por_anterior) <= float(valor)):
                                text_prueba.write("Entro al if del else: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                    text_prueba.write("Cant de Verdaderas  : " + str(cant_true) + "\n")
                    text_prueba.write("Cant de Falsas      : " + str(cant_false) + "\n")
                    if (cant_true > cant_false):
                        cant_total = cant_true
                        tof_ant = 1
                        lista_vof.append(tof_ant)
                    if (cant_true < cant_false):
                        cant_total = cant_false
                        tof_ant = 0
                        lista_vof.append(tof_ant)
                    if (cant_true == cant_false):
                        cant_total = cant_true
                        if (tof_ant == 2):
                            tof_ant = 1
                        lista_vof.append(tof_ant)

                    text_prueba.write(
                        "CantTotal(ganador)    : " + str(cant_total) + " - siendo V(1) o F(0): " + str(tof_ant) + "\n")
                    por_anterior = por
                    cantidad_total = cant_total + cantidad_total
                    lista_porcentaje_puntaje_total.append(cant_total)

            if (tof_ant != 2):
                lista_cant_total.append(cantidad_total)
            text_prueba.write("-------------------------------------------------------------------------------- \n")
            text_prueba.write(
                "Con lamda  : " + str(lmda) + " - se tiene lista: " + str(lista_porcentaje_puntaje_total) + "\n")
            text_prueba.write("Lista VyF  : " + str(lista_vof) + "\n")
            text_prueba.write("Mejor Puntaje  : " + str(lista_cant_total) + "\n")
            lista_todos_vof.append(lista_vof)
            lista_todos_cantidad_vof.append(lista_porcentaje_puntaje_total)

        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("VyF  : " + str(lista_todos_vof) + "\n")
        text_prueba.write("Puntajes VyF  : " + str(lista_todos_cantidad_vof) + "\n")
        text_prueba.write("Mejores ptjes totales  : " + str(lista_cant_total) + "\n")

        intento = list()
        for t in lista_porcentajes:
            if (t == lista_porcentajes[0]):
                intento.append("0-0.1")
                t_ant = 0
            else:
                intento.append(str(t_ant) + "-" + str(t))
                t_ant = t

        intento2 = list()

        for h in lmdas:
            intento2.append("lmda-" + str(h))

        i = 0
        t2 = 0
        for j in lista_cant_total:
            if i != 0:
                if (j > j_ant2):
                    j_ant2 = j
                    t2 = i
            else:
                j_ant2 = j
            i += 1

        text_prueba.write("Mejores ptjes de la lista : " + str(j_ant2) + " en lmda: " + str(lmdas[t2]) + "\n")
        trace4 = go.Heatmap(
            z=lista_todos_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        trace5 = go.Heatmap(
            z=lista_todos_cantidad_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        ## Para cada b_x sacar los F1

        lista_vyf = list()
        lista_F1 = list()
        lista_lista_F1 = list()
        for columna in range(len(lmdas)):

            if probar == 1:
                lista_vyf = lista2
            else:
                lista_vyf = lista_todos_vof[columna]
            TP_d1 = 0
            FN_d1 = 0
            FP_d1 = 0
            TN_d1 = 0
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                lmda = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(lmda) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if (float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + " - seria un V(1) o F(0): " + str(lista_vyf[arr]) + "\n")
                if (lista_vyf[arr] == 1):
                    d1 = "V"
                else:
                    d1 = "F"

                if sol == "T" or sol == "V" or sol == "Y":
                    if d1 == "V":
                        TP_d1 += 1

                    if d1 == "F":
                        FN_d1 += 1
                if sol == "F" or sol == "N":
                    if d1 == "V":
                        FP_d1 += 1
                    if d1 == "F":
                        TN_d1 += 1

            if (TP_d1 + FP_d1) != 0:
                precision_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FP_d1))
            else:
                precision_d1 = 0
            if (TP_d1 + FN_d1) != 0:
                recall_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FN_d1))
            else:
                recall_d1 = 0
            if (precision_d1 + recall_d1) != 0:
                F1_d1 = 2 * (mpmath.mpf(precision_d1 * recall_d1) / mpmath.mpf(precision_d1 + recall_d1))
            else:
                F1_d1 = 0
            lista_F1.append(str(F1_d1))

            lista_lista_F1.append(lista_F1)
            # lista_lista_F1.append(lista_cant_total[columna])
            text_prueba.write(
                "TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
            text_prueba.write("F1: " + str(F1_d1) + "\n")
            # text_prueba.write("Revisando  : " + str(por_anterior) + " >= " + str(valor) + " < " + str(por) + "\n")

        text_prueba.write("F1: " + str(lista_F1) + "\n")

        lista_z = list()
        j = 0
        for i in lista_lista_F1:
            lista_resultados = list()
            lista_resultados.append(float(i[j]))
            cant_aciertos = lista_cant_total[j]
            lista_resultados.append(int(cant_aciertos))
            lista_z.append(lista_resultados)
            j += 1
        text_prueba.write("list z: " + str(lista_z) + "\n")

        trace6 = go.Heatmap(
            z=lista_z,
            x=['F1', '#'],
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        #DOCODE NORMALIZADO POR SEGMENTO
        text_prueba.write(" DOCODE NORMALIZADO POR SEGMENTO \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM-POR-SEG.xls')
        table2 = data2.sheets()[0]

        lista_todos_vof = list()
        lista_todos_cantidad_vof = list()
        lista_cant_total = list()
        for columna in range(len(lmdas)):
            lista_porcentaje_puntaje_total = list()
            lista_vof = list()
            cantidad_total = 0
            for por in lista_porcentajes:

                text_prueba.write("Revisando el porcentaje: " + str(por) + "\n")
                if (por == lista_porcentajes[0]):
                    por_anterior = 0
                    tof_ant = 2
                else:
                    cant_true = 0
                    cant_false = 0
                    cant_total = 0
                    for filas in range(len(listacarpetas)):
                        text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                        solreal = table2.cell(filas + 1, 1).value
                        lmda = table2.cell(0, columna + 2).value
                        valor = table2.cell(filas + 1, columna + 2).value
                        valor = valor.replace(" ", "")
                        sol = str(solreal).strip()
                        text_prueba.write("sol real: " + str(sol) + "\n")
                        text_prueba.write("lambda:" + str(lmda) + "\n")
                        text_prueba.write("valor:" + str(valor) + "\n")
                        text_prueba.write(
                            "Revisando  : " + str(por_anterior) + " >= " + str(valor) + " < " + str(por) + "\n")
                        ult = len(lista_porcentajes)
                        if (por != lista_porcentajes[ult - 1]):
                            if (float(por_anterior) <= float(valor) < float(por)):
                                text_prueba.write("Entro al if: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                        else:
                            if (float(por_anterior) <= float(valor)):
                                text_prueba.write("Entro al if del else: \n")
                                if sol == "T" or sol == "V" or sol == "Y":
                                    cant_true += 1
                                if sol == "F" or sol == "N":
                                    cant_false += 1
                    text_prueba.write("Cant de Verdaderas  : " + str(cant_true) + "\n")
                    text_prueba.write("Cant de Falsas      : " + str(cant_false) + "\n")
                    if (cant_true > cant_false):
                        cant_total = cant_true
                        tof_ant = 1
                        lista_vof.append(tof_ant)
                    if (cant_true < cant_false):
                        cant_total = cant_false
                        tof_ant = 0
                        lista_vof.append(tof_ant)
                    if (cant_true == cant_false):
                        cant_total = cant_true
                        if (tof_ant == 2):
                            tof_ant = 1
                        lista_vof.append(tof_ant)

                    text_prueba.write(
                        "CantTotal(ganador)    : " + str(cant_total) + " - siendo V(1) o F(0): " + str(tof_ant) + "\n")
                    por_anterior = por
                    cantidad_total = cant_total + cantidad_total
                    lista_porcentaje_puntaje_total.append(cant_total)

            if (tof_ant != 2):
                lista_cant_total.append(cantidad_total)
            text_prueba.write("-------------------------------------------------------------------------------- \n")
            text_prueba.write(
                "Con lamda  : " + str(lmda) + " - se tiene lista: " + str(lista_porcentaje_puntaje_total) + "\n")
            text_prueba.write("Lista VyF  : " + str(lista_vof) + "\n")
            text_prueba.write("Mejor Puntaje  : " + str(lista_cant_total) + "\n")
            lista_todos_vof.append(lista_vof)
            lista_todos_cantidad_vof.append(lista_porcentaje_puntaje_total)

        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("-------------------------------------------------------------------------------- \n")
        text_prueba.write("VyF  : " + str(lista_todos_vof) + "\n")
        text_prueba.write("Puntajes VyF  : " + str(lista_todos_cantidad_vof) + "\n")
        text_prueba.write("Mejores ptjes totales  : " + str(lista_cant_total) + "\n")

        intento = list()
        for t in lista_porcentajes:
            if (t == lista_porcentajes[0]):
                intento.append("0-0.1")
                t_ant = 0
            else:
                intento.append(str(t_ant) + "-" + str(t))
                t_ant = t

        intento2 = list()

        for h in lmdas:
            intento2.append("lmda-" + str(h))

        i = 0
        t3=0
        for j in lista_cant_total:
            if i != 0:
                if (j > j_ant3):
                    j_ant3 = j
                    t3 = i
            else:
                j_ant3 = j
            i += 1

        text_prueba.write("Mejores ptjes de la lista : " + str(j_ant3) + " en lmda: " + str(lmdas[t3]) + "\n")
        trace7 = go.Heatmap(
            z=lista_todos_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        trace8 = go.Heatmap(
            z=lista_todos_cantidad_vof,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        ## Para cada b_x sacar los F1

        lista_vyf = list()
        lista_F1 = list()
        lista_lista_F1 = list()
        for columna in range(len(lmdas)):
            if probar == 1:
                lista_vyf = lista3
            else:
                lista_vyf = lista_todos_vof[columna]
            TP_d1 = 0
            FN_d1 = 0
            FP_d1 = 0
            TN_d1 = 0
            for filas in range(len(listacarpetas)):
                text_prueba.write("Revisando en la columna: " + str(columna) + " la fila: " + str(filas) + "\n")
                solreal = table2.cell(filas + 1, 1).value
                lmda = table2.cell(0, columna + 2).value
                valor = table2.cell(filas + 1, columna + 2).value
                valor = valor.replace(" ", "")
                sol = str(solreal).strip()
                text_prueba.write("sol real: " + str(sol) + "\n")
                text_prueba.write("lambda:" + str(lmda) + "\n")
                text_prueba.write("valor:" + str(valor) + "\n")
                if (float(valor) > 0 and float(valor) < 1):
                    arr = int(float(valor) * 10)
                if (float(valor) == 0.0):
                    arr = int(float(valor))
                if (float(valor) >= 1):
                    arr = 9
                text_prueba.write("arr:" + str(arr) + " - seria un V(1) o F(0): " + str(lista_vyf[arr]) + "\n")
                if (lista_vyf[arr] == 1):
                    d1 = "V"
                else:
                    d1 = "F"

                if sol == "T" or sol == "V" or sol == "Y":
                    if d1 == "V":
                        TP_d1 += 1

                    if d1 == "F":
                        FN_d1 += 1
                if sol == "F" or sol == "N":
                    if d1 == "V":
                        FP_d1 += 1
                    if d1 == "F":
                        TN_d1 += 1

            if (TP_d1 + FP_d1) != 0:
                precision_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FP_d1))
            else:
                precision_d1 = 0
            if (TP_d1 + FN_d1) != 0:
                recall_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FN_d1))
            else:
                recall_d1 = 0
            if (precision_d1 + recall_d1) != 0:
                F1_d1 = 2 * (mpmath.mpf(precision_d1 * recall_d1) / mpmath.mpf(precision_d1 + recall_d1))
            else:
                F1_d1 = 0
            lista_F1.append(str(F1_d1))

            lista_lista_F1.append(lista_F1)
            # lista_lista_F1.append(lista_cant_total[columna])
            text_prueba.write(
                "TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
            text_prueba.write("F1: " + str(F1_d1) + "\n")
            # text_prueba.write("Revisando  : " + str(por_anterior) + " >= " + str(valor) + " < " + str(por) + "\n")

        text_prueba.write("F1: " + str(lista_F1) + "\n")

        lista_z = list()
        j = 0
        for i in lista_lista_F1:
            lista_resultados = list()
            lista_resultados.append(float(i[j]))
            cant_aciertos = lista_cant_total[j]
            lista_resultados.append(int(cant_aciertos))
            lista_z.append(lista_resultados)
            j += 1
        text_prueba.write("list z: " + str(lista_z) + "\n")

        trace9 = go.Heatmap(
            z=lista_z,
            x=['F1', '#'],
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas) / 2,
            colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'],
                        [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
        )

        # Graficar
        #
        fig = tools.make_subplots(rows=3, cols=3, subplot_titles=('DOC -Mejores V o F', 'DOC-Mejor Lmda:'+str(lmdas[t1])+"/["+str(j_ant1)+"]",'DOC-F1/Cantidad Aciertos',
                                                                  'DOC-NOR-Mejores V o F','DOC-NOR-Mejor Lmda:'+str(lmdas[t2])+"/["+str(j_ant2)+"]",'DOC-NOR-F1/Cantidad Aciertos',
                                                                  'DOC-NOR-SEG-Mejores V o F', 'DOC-NOR-SEG-Mejor Lmda:'+str(lmdas[t3])+"/["+str(j_ant3)+"]",'DOC-NOR-SEG-F1/Cantidad Aciertos'))
        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2, 1, 2)
        fig.append_trace(trace3, 1, 3)
        fig.append_trace(trace4, 2, 1)
        fig.append_trace(trace5, 2, 2)
        fig.append_trace(trace6, 2, 3)
        fig.append_trace(trace7, 3, 1)
        fig.append_trace(trace8, 3, 2)
        fig.append_trace(trace9, 3, 3)
        fig['layout'].update(height=1200, width=1200, title='Bx')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'B0B1.html')

