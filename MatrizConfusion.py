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

class matriz(object):
    def __new__(cls, RESULT_FOLDER_PATH, lmdas, lista_porcentajes):

        #Abrir archivo para leer
        file = open(RESULT_FOLDER_PATH + "Resultados.txt", "r")
        soluciones = open(SOURCES_FOLDER_PATH + "truth.txt", "r")

        # Crear excel para hacer trace
        text_prueba = open(RESULT_FOLDER_PATH + "Trace2.txt", "a")
        text_prueba.write("\n \n Comienzo a revisar en MATRIZ DE CONFUSION. \n")

        # Crear listas de cantidades de verdaderas y falsas por porcentaje analizado
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

        # Crear Excel resultados
        resultadoExcel = xlwt.Workbook()
        resultado1 = resultadoExcel.add_sheet("Hoja1")
        resultado1.write(0, 0, "Carpeta")
        resultado1.write(0, 1, "Solucion Real")
        resultado1.write(0, 2, "Solucion DOCODE")
        resultado1.write(0, 3, "Solucion DOCODE Norm")
        resultado1.write(0, 4, "Solucion DOCODE Norm Segmentos")
        resultado1.write(0, 5, "% DOCODE")
        resultado1.write(0, 6, "% DOCODE NORM")
        resultado1.write(0, 7, "% DOCODE NORM SEGMENTOS")

        i=1
        for line in file:
            line = line.replace("[","")
            line = line.replace("'", "")
            line = line.replace(",", "")
            line = line.replace("-", "")
            line = line.replace("]", "")
            #print(str(line))

            lista= line.split(" ")


            resultado1.write(i, 0, str(lista[0]))
            resultado1.write(i, 1, str(listasolreal[i-1]))
            resultado1.write(i, 2, str(lista[1]))
            resultado1.write(i, 3, str(lista[2]))
            resultado1.write(i, 4, str(lista[3]))
            resultado1.write(i, 5, str(lista[5]))
            resultado1.write(i, 6, str(lista[6]))
            resultado1.write(i, 7, str(lista[7]))
            i=i+1

        resultadoExcel.save(RESULT_FOLDER_PATH + "Resultados.xls")
        file.close()

        ## Tengo todos los documentos para revisar
        ## Revisar Resultados
        data = xlrd.open_workbook(RESULT_FOLDER_PATH+'Resultados.xls')
        table = data.sheets()[0]

        # Crear Excel resultados
        Excel1 = xlwt.Workbook()
        result = Excel1.add_sheet("Hoja1")
        TP_d1=0
        FN_d1=0
        FP_d1=0
        TN_d1=0
        TP_d2 = 0
        FN_d2 = 0
        FP_d2 = 0
        TN_d2 = 0
        TP_d3 = 0
        FN_d3 = 0
        FP_d3 = 0
        TN_d3 = 0

        for filas in range(len(listacarpetas)):
                #print("revisando la fila ------------->"+str(filas))
                solreal = table.cell(filas+1, 1).value
                solreal = solreal.replace("\n","")
                solreal = solreal.replace(" ", "")
                d1 = table.cell(filas+1, 2).value
                d2 = table.cell(filas + 1, 3).value
                d3 = table.cell(filas + 1, 4).value
                #print("sol real: " + str(solreal))
                #print("d1: " + str(d1))
                #if solreal=='Y' or solreal=='T' or solreal=='V':
                if solreal.find("Y") or solreal.find("T") or solreal.find("V"):
                    if d1=='Y' or d1=='T' or d1=='V':
                        TP_d1+=1
                    if d1=='F' or d1=='N':
                        FN_d1+=1
                    if d2=='Y' or d2=='T' or d2=='V':
                        TP_d2+=1
                    if d2=='F' or d2=='N':
                        FN_d2+=1
                    if d3=='Y' or d3=='T' or d3=='V':
                        TP_d3+=1
                    if d3=='F' or d3=='N':
                        FN_d3+=1
                else:
                    if d1=='Y' or d1=='T' or d1=='V':
                        FP_d1 +=1
                    if d1=='F' or d1=='N':
                        TN_d1 += 1
                    if d2=='Y' or d2=='T' or d2=='V':
                        FP_d2 += 1
                    if d2=='F' or d2=='N':
                        TN_d2 += 1
                    if d3=='Y' or d3=='T' or d3=='V':
                        FP_d3 += 1
                    if d3=='F' or d3=='N':
                        TN_d3 += 1

        #print("1 TP: " + str(TP_d1)+"- FP_d "+str(FP_d1)+"- FN "+str(FN_d1)+"- TN "+str(TN_d1))
        #print("2 TP: " + str(TP_d2) + "- FP_d " + str(FP_d2) + "- FN " + str(FN_d2) + "- TN " + str(TN_d2))
        #print("3 TP: " + str(TP_d3) + "- FP_d " + str(FP_d3) + "- FN " + str(FN_d3) + "- TN " + str(TN_d3))
        if TP_d1+FP_d1!=0:
            precision_d1=(mpmath.mpf(TP_d1)/mpmath.mpf(TP_d1+FP_d1))
        else:
            precision_d1=0
        if TP_d1+FN_d1 != 0:
            recall_d1=(mpmath.mpf(TP_d1)/mpmath.mpf(TP_d1+FN_d1))
        else:
            recall_d1=0
        if (precision_d1+recall_d1) !=0:
            F1_d1=2*(mpmath.mpf(precision_d1*recall_d1)/mpmath.mpf(precision_d1+recall_d1))
        else:
            F1_d1=0
        #
        if TP_d2+FP_d2!=0:
            precision_d2=(mpmath.mpf(TP_d2)/mpmath.mpf(TP_d2+FP_d2))
        else:
            precision_d2=0
        if TP_d2+FN_d2 != 0:
            recall_d2=(mpmath.mpf(TP_d2)/mpmath.mpf(TP_d2+FN_d2))
        else:
            recall_d2=0
        if (precision_d2+recall_d2) !=0:
            F1_d2=2*(mpmath.mpf(precision_d2*recall_d2)/mpmath.mpf(precision_d2+recall_d2))
        else:
            F1_d2=0

        if TP_d3+FP_d3!=0:
            precision_d3=(mpmath.mpf(TP_d3)/mpmath.mpf(TP_d3+FP_d3))
        else:
            precision_d3=0
        if TP_d3+FN_d3 != 0:
            recall_d3=(mpmath.mpf(TP_d3)/mpmath.mpf(TP_d3+FN_d3))
        else:
            recall_d3=0
        if (precision_d3+recall_d3) !=0:
            F1_d3=2*(mpmath.mpf(precision_d3*recall_d3)/mpmath.mpf(precision_d3+recall_d3))
        else:
            F1_d3=0
        ## Guardar resultados
        result.write(0, 0, "DOCODE")
        result.write(0, 1, "a=0.075")
        result.write(0, 2, "Precision")
        result.write(1, 2, "Recall")
        result.write(2, 2, "F1")
        result.write(0, 3, str(precision_d1))
        result.write(1, 3, str(recall_d1))
        result.write(2, 3, str(F1_d1))
        #
        result.write(3, 0, "DOCODE NORMALIZADO")
        result.write(3, 1, "a=0.2")
        result.write(3, 2, "Precision")
        result.write(4, 2, "Recall")
        result.write(5, 2, "F1")
        result.write(3, 3, str(precision_d2))
        result.write(4, 3, str(recall_d2))
        result.write(5, 3, str(F1_d2))
        #
        result.write(6, 0, "DOCODE NORMALIZADO POR SEG")
        result.write(6, 1, "a=0.8")
        result.write(6, 2, "Precision")
        result.write(7, 2, "Recall")
        result.write(8, 2, "F1")
        result.write(6, 3, str(precision_d3))
        result.write(7, 3, str(recall_d3))
        result.write(8, 3, str(F1_d3))

        text_prueba.write("DOCODE NORMALIZADO \n")

    # Termino de Resultados Generales
        ##DOCODE
        text_prueba.write(" DOCODE  \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODE.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()
        lista_todosF1 = list()
        for por in lista_porcentajes:
            text_prueba.write("Revisando el porcentaje: " + str(por) + "\n")
            fila = 0
            result2 = Excel1.add_sheet("D-" + str(por))
            lista_true = list()
            lista_false = list()
            lista_total = list()
            lista_F1 = list ()
            for columna in range(len(lmdas)):
                TP_d1 = 0
                FN_d1 = 0
                FP_d1 = 0
                TN_d1 = 0
                cant_true = 0
                cant_false = 0
                cant_total = 0
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
                    if (float(valor) >= float(por)):
                        d1 = "V"
                        text_prueba.write("valor: " + str(valor) + " es >= a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")
                    else:
                        d1 = "F"
                        text_prueba.write(
                            "valor: " + str(valor) + " es < a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")

                    if sol == "T" or sol == "V" or sol == "Y":
                        if d1 == "V":
                            TP_d1 += 1
                            cant_true += 1
                        if d1 == "F":
                            FN_d1 += 1
                    if sol == "F" or sol == "N":
                        if d1 == "V":
                            FP_d1 += 1
                        if d1 == "F":
                            TN_d1 += 1
                            cant_false += 1
                    cant_total = cant_true + cant_false
                text_prueba.write("Cantidad de Verdaderas: " + str(cant_true) + "\n")
                text_prueba.write("Cantidad de Falsas: " + str(cant_false) + "\n")
                lista_true.append(cant_true)
                lista_false.append(cant_false)
                lista_total.append(cant_total)
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

                text_prueba.write("TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
                # print("imprimir en hoja los resultados")
                result2.write(fila, 0, "DOCODE NORMALIZADO POR SEGMENTO")
                result2.write(fila, 1, str(a))
                result2.write(fila, 2, "Precision")
                result2.write(fila + 1, 2, "Recall")
                result2.write(fila + 2, 2, "F1")
                result2.write(fila, 3, str(precision_d1))
                result2.write(fila + 1, 3, str(recall_d1))
                result2.write(fila + 2, 3, str(F1_d1))
                fila += 3

            lista_todosF1.append(lista_F1)
            lista_resultados_true.append(lista_true)
            lista_resultados_false.append(lista_false)
            lista_resultados_total.append(lista_total)

        text_prueba.write("Resumen para cada lamda \n")
        text_prueba.write("Lista de Verdaderas  : " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista de Falsas      : " + str(lista_resultados_false) + "\n")
        text_prueba.write("Lista de Totales     : " + str(lista_resultados_total) + "\n")
        text_prueba.write("Lista de Todos los F1: " + str(lista_todosF1) + "\n")

        lista_resultados_invertidos_true = list()
        for i in range(len(lmdas)):
            invertidos_true = list()
            for por in lista_resultados_true:
                invertidos_true.append(por[i])
            lista_resultados_invertidos_true.append(invertidos_true)

        lista_resultados_invertidos_false = list()
        for i in range(len(lmdas)):
            invertidos_false = list()
            for por in lista_resultados_false:
                invertidos_false.append(por[i])
            lista_resultados_invertidos_false.append(invertidos_false)

        lista_resultados_invertidos_total = list()
        for i in range(len(lmdas)):
            invertidos_total = list()
            for por in lista_resultados_total:
                invertidos_total.append(por[i])
            lista_resultados_invertidos_total.append(invertidos_total)

        lista_resultados_invertidos_F1 = list()
        for i in range(len(lmdas)):
            invertidos_F1 = list()
            for por in lista_todosF1:
                invertidos_F1.append(por[i])
            lista_resultados_invertidos_F1.append(invertidos_F1)

        text_prueba.write("Resumen para cada lamda, matriz invertida \n")
        text_prueba.write("Lista de Verdaderas: " + str(lista_resultados_invertidos_true) + "\n")
        text_prueba.write("Lista de Falsas    : " + str(lista_resultados_invertidos_false) + "\n")
        text_prueba.write("Lista de F1        : " + str(lista_resultados_invertidos_F1) + "\n")

        # Histograma
        intento = list()
        intento2 = list()
        for t in lista_porcentajes:
            intento.append("por-" + str(t))
        for h in lmdas:
            intento2.append("l-" + str(h))

        trace7 = go.Heatmap(
            z=lista_resultados_invertidos_true,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Viridis'
        )
        trace8 = go.Heatmap(
            z=lista_resultados_invertidos_false,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Viridis'
        )

        trace9 = go.Heatmap(
            z=lista_resultados_invertidos_total,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Rainbow'
        )

        trace10 = go.Heatmap(
            z=lista_resultados_invertidos_F1,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cividis'
        )

        ## Revisar DOCODE NORMALIZADO
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()
        lista_todosF1 = list()
        lista_valores = list()
        #text_prueba.write("HISTOGRAMA: \n Lista V: " + str(lista_p_true) + "\n Lista F: " + str(lista_p_false) + "\n")

        for por in lista_porcentajes:
            text_prueba.write("Revisando el porcentaje: " + str(por)+ "\n")
            fila = 0
            result2 = Excel1.add_sheet("DN-"+str(por))
            lista_true = list()
            lista_false = list()
            lista_total = list()
            #lista_t = list()
            #lista_f = list()
            #lista_totalt = list()
            #lista_totalf = list()
            lista_F1 = list()
            for columna in range(len(lmdas)):
                TP_d1 = 0
                FN_d1 = 0
                FP_d1 = 0
                TN_d1 = 0
                cant_true = 0
                cant_false = 0
                cant_total = 0
                #lista_t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #lista_f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for filas in range(len(listacarpetas)):
                    text_prueba.write("Revisando en la columna: " + str(columna) +" la fila: "+str(filas)+ "\n")
                    solreal = table2.cell(filas+1, 1).value
                    a = table2.cell(0, columna+2).value
                    valor = table2.cell(filas+1, columna+2).value
                    valor=valor.replace(" ","")
                    sol = str(solreal).strip()
                    text_prueba.write("sol real: " + str(sol) + "\n")
                    text_prueba.write("lambda:" + str(a) + "\n")
                    text_prueba.write("valor:" + str(valor) + "\n")
                    #if(float(valor)!=1.0):
                    #    arr = int(float(valor) * 10)
                    #else:
                     #   arr = int(float(valor))
                    #text_prueba.write("arr:" + str(arr) + "\n")
                    if (float(valor) >= float(por)):
                        d1="V"
                        text_prueba.write("valor: " + str(valor) + " es >= a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")
                    else:
                        d1="F"
                        text_prueba.write("valor: " + str(valor) + " es < a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")

                    if sol == "T" or sol == "V" or sol == "Y" :
                        if d1=="V":
                            TP_d1+=1
                            cant_true+=1
                        if d1=="F":
                            FN_d1+=1
                        #lista_t[arr] += 1


                    if sol == "F" or sol == "N" :
                        if d1 == "V":
                            FP_d1 +=1
                        if d1=="F":
                            TN_d1 += 1
                            cant_false += 1
                        #lista_f[arr] += 1
                    cant_total=cant_true+cant_false

                #lista_totalt.append(lista_t)
                #lista_totalf.append(lista_f)
                text_prueba.write("Cantidad de Verdaderas: " + str(cant_true) + "\n")
                text_prueba.write("Cantidad de Falsas: " + str(cant_false) + "\n")
                #text_prueba.write("Lista total Verdadera: " + str(lista_totalt) + "\n")
                #text_prueba.write("Lista total Falsas   : " + str(lista_totalf) + "\n")
                lista_true.append(cant_true)
                lista_false.append(cant_false)
                lista_total.append(cant_total)
                if TP_d1 + FP_d1 != 0:
                    precision_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FP_d1))
                else:
                    precision_d1 = 0
                if TP_d1 + FN_d1 != 0:
                    recall_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FN_d1))
                else:
                    recall_d1 = 0
                if (precision_d1 + recall_d1) != 0:
                    F1_d1 = 2 * (mpmath.mpf(precision_d1 * recall_d1) / mpmath.mpf(precision_d1 + recall_d1))
                else:
                    F1_d1 = 0
                lista_F1.append(str(F1_d1))

                text_prueba.write("TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
                #print("imprimir en hoja los resultados")
                result2.write(fila, 0, "DOCODE NORMALIZADO")
                result2.write(fila, 1, str(a))
                result2.write(fila, 2, "Precision")
                result2.write(fila+1, 2, "Recall")
                result2.write(fila+2, 2, "F1")
                result2.write(fila, 3, str(precision_d1))
                result2.write(fila+1, 3, str(recall_d1))
                result2.write(fila+2, 3, str(F1_d1))
                fila+=3

            lista_todosF1.append(lista_F1)
            lista_resultados_true.append(lista_true)
            lista_resultados_false.append(lista_false)
            lista_resultados_total.append(lista_total)

        text_prueba.write("Resumen para cada lamda \n")
        text_prueba.write("Lista de Verdaderas: " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista de Falsas    : " + str(lista_resultados_false) + "\n")
        text_prueba.write("Lista de Totales   : " + str(lista_resultados_total) + "\n")
        text_prueba.write("Lista de Todos los F1: " + str(lista_todosF1) + "\n")


        lista_resultados_invertidos_true = list()
        for i in range(len(lmdas)):
            invertidos_true = list()
            for por in lista_resultados_true:
                invertidos_true.append(por[i])
            lista_resultados_invertidos_true.append(invertidos_true)


        lista_resultados_invertidos_false = list()
        for i in range(len(lmdas)):
            invertidos_false = list()
            for por in lista_resultados_false:
                invertidos_false.append(por[i])
            lista_resultados_invertidos_false.append(invertidos_false)


        lista_resultados_invertidos_total = list()
        for i in range(len(lmdas)):
            invertidos_total = list()
            for por in lista_resultados_total:
                invertidos_total.append(por[i])
            lista_resultados_invertidos_total.append(invertidos_total)

        lista_resultados_invertidos_F1 = list()
        for i in range(len(lmdas)):
            invertidos_F1 = list()
            for por in lista_todosF1:
                invertidos_F1.append(por[i])
            lista_resultados_invertidos_F1.append(invertidos_F1)

        text_prueba.write("Resumen para cada lamda, matriz invertida \n")
        text_prueba.write("Lista de Verdaderas: " + str(lista_resultados_invertidos_true) + "\n")
        text_prueba.write("Lista de Falsas    : " + str(lista_resultados_invertidos_false) + "\n")
        text_prueba.write("Lista de F1        : " + str(lista_resultados_invertidos_F1) + "\n")

        #Histograma

        trace1 = go.Heatmap(
            z=lista_resultados_invertidos_true ,
            x=intento ,
            y=intento2 ,
            zmin = 0,
            zmax=len(listacarpetas),
            colorscale='Viridis'
            )
        trace2 = go.Heatmap(
            z=lista_resultados_invertidos_false ,
            x=intento ,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Viridis' #Cividis
        )

        trace3 = go.Heatmap(
            z=lista_resultados_invertidos_total,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Rainbow'
        )
        trace11 = go.Heatmap(
            z=lista_resultados_invertidos_F1,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cividis'
        )

        ## DOCODE NORMALIZADO POR SEGMENTO
        text_prueba.write(" DOCODE NORMALIZADO POR SEGMENTO \n")
        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'ResultDOCODENORM-POR-SEG.xls')
        table2 = data2.sheets()[0]

        lista_resultados_true = list()
        lista_resultados_false = list()
        lista_resultados_total = list()
        lista_todosF1 = list()
        for por in lista_porcentajes:
            text_prueba.write("Revisando el porcentaje: " + str(por) + "\n")
            fila = 0
            result2 = Excel1.add_sheet("DNS-" + str(por))
            lista_true = list()
            lista_false = list()
            lista_total = list()
            lista_F1 = list()
            for columna in range(len(lmdas)):
                TP_d1 = 0
                FN_d1 = 0
                FP_d1 = 0
                TN_d1 = 0
                cant_true = 0
                cant_false = 0
                cant_total = 0
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
                    if (float(valor) >= float(por)):
                        d1 = "V"
                        text_prueba.write(
                            "valor: " + str(valor) + " es >= a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")
                    else:
                        d1 = "F"
                        text_prueba.write(
                            "valor: " + str(valor) + " es < a porcentaje: " + str(por) + " ==> " + str(d1) + "\n")

                    if sol == "T" or sol == "V" or sol == "Y":
                        if d1 == "V":
                            TP_d1 += 1
                            cant_true += 1
                        if d1 == "F":
                            FN_d1 += 1
                    if sol == "F" or sol == "N":
                        if d1 == "V":
                            FP_d1 += 1
                        if d1 == "F":
                            TN_d1 += 1
                            cant_false += 1
                    cant_total = cant_true + cant_false
                text_prueba.write("Cantidad de Verdaderas: " + str(cant_true) + "\n")
                text_prueba.write("Cantidad de Falsas: " + str(cant_false) + "\n")
                lista_true.append(cant_true)
                lista_false.append(cant_false)
                lista_total.append(cant_total)
                if TP_d1 + FP_d1 != 0:
                    precision_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FP_d1))
                else:
                    precision_d1 = 0
                if TP_d1 + FN_d1 != 0:
                    recall_d1 = (mpmath.mpf(TP_d1) / mpmath.mpf(TP_d1 + FN_d1))
                else:
                    recall_d1 = 0
                if (precision_d1 + recall_d1) != 0:
                    F1_d1 = 2 * (mpmath.mpf(precision_d1 * recall_d1) / mpmath.mpf(precision_d1 + recall_d1))
                else:
                    F1_d1 = 0
                lista_F1.append(str(F1_d1))

                text_prueba.write(
                    "TP: " + str(TP_d1) + "- FP " + str(FP_d1) + "- FN " + str(FN_d1) + "- TN " + str(TN_d1) + "\n")
                # print("imprimir en hoja los resultados")
                result2.write(fila, 0, "DOCODE NORMALIZADO POR SEGMENTO")
                result2.write(fila, 1, str(a))
                result2.write(fila, 2, "Precision")
                result2.write(fila + 1, 2, "Recall")
                result2.write(fila + 2, 2, "F1")
                result2.write(fila, 3, str(precision_d1))
                result2.write(fila + 1, 3, str(recall_d1))
                result2.write(fila + 2, 3, str(F1_d1))
                fila += 3

            lista_todosF1.append(lista_F1)
            lista_resultados_true.append(lista_true)
            lista_resultados_false.append(lista_false)
            lista_resultados_total.append(lista_total)

        text_prueba.write("Resumen para cada lamda \n")
        text_prueba.write("Lista de Verdaderas: " + str(lista_resultados_true) + "\n")
        text_prueba.write("Lista de Falsas    : " + str(lista_resultados_false) + "\n")
        text_prueba.write("Lista de Totales   : " + str(lista_resultados_total) + "\n")
        text_prueba.write("Lista de Todos los F1: " + str(lista_todosF1) + "\n")

        lista_resultados_invertidos_true = list()
        for i in range(len(lmdas)):
            invertidos_true = list()
            for por in lista_resultados_true:
                invertidos_true.append(por[i])
            lista_resultados_invertidos_true.append(invertidos_true)

        lista_resultados_invertidos_false = list()
        for i in range(len(lmdas)):
            invertidos_false = list()
            for por in lista_resultados_false:
                invertidos_false.append(por[i])
            lista_resultados_invertidos_false.append(invertidos_false)

        lista_resultados_invertidos_total = list()
        for i in range(len(lmdas)):
            invertidos_total = list()
            for por in lista_resultados_total:
                invertidos_total.append(por[i])
            lista_resultados_invertidos_total.append(invertidos_total)

        lista_resultados_invertidos_F1 = list()
        for i in range(len(lmdas)):
            invertidos_F1 = list()
            for por in lista_todosF1:
                invertidos_F1.append(por[i])
            lista_resultados_invertidos_F1.append(invertidos_F1)

        text_prueba.write("Resumen para cada lamda, matriz invertida \n")
        text_prueba.write("Lista de Verdaderas: " + str(lista_resultados_invertidos_true) + "\n")
        text_prueba.write("Lista de Falsas    : " + str(lista_resultados_invertidos_false) + "\n")
        text_prueba.write("Lista de F1        : " + str(lista_resultados_invertidos_F1) + "\n")

        # Histograma

        trace4 = go.Heatmap(
            z=lista_resultados_invertidos_true,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Viridis'
        )
        trace5 = go.Heatmap(
            z=lista_resultados_invertidos_false,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Viridis'
        )

        trace6 = go.Heatmap(
            z=lista_resultados_invertidos_total,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=len(listacarpetas),
            colorscale='Rainbow'
        )
        trace12 = go.Heatmap(
            z=lista_resultados_invertidos_F1,
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cividis'
        )


        # colorscale:  Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, Blues, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis, Cividis

        # Graficar
        fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('V-D', 'F-D','V-DNor', 'F-DNor','V_DNSeg', 'F-DNSeg'))
        fig.append_trace(trace7, 1, 1)
        fig.append_trace(trace8, 1, 2)
        fig.append_trace(trace1, 2, 1)
        fig.append_trace(trace2, 2, 2)
        fig.append_trace(trace4, 3, 1)
        fig.append_trace(trace5, 3, 2)
        fig['layout'].update(height=800, width=1200, title='Verdaderos vs Falsos')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'Hist-pertenencia-TODOS.html')

        fig2 = tools.make_subplots(rows=1, cols=3, subplot_titles=('DOCODE','DOCODE-NORM', 'DOCODE-NOR-SEG'))
        fig2.append_trace(trace9, 1, 1)
        fig2.append_trace(trace3, 1, 2)
        fig2.append_trace(trace6, 1, 3)

        fig2['layout'].update(height=600, width=1200, title='Total Aciertos')
        result = plotly.offline.plot(fig2, filename=RESULT_FOLDER_PATH + 'Hist-aciertos-TODOS.html')

        fig3 = tools.make_subplots(rows=1, cols=3, subplot_titles=('DOCODE', 'DOCODE-NORM', 'DOCODE-NOR-SEG'))
        fig3.append_trace(trace10, 1, 1)
        fig3.append_trace(trace11, 1, 2)
        fig3.append_trace(trace12, 1, 3)

        fig3['layout'].update(height=600, width=1200, title='Mejores F1')
        result = plotly.offline.plot(fig3, filename=RESULT_FOLDER_PATH + 'Hist-Mejor-F1-TODOS.html')

        # Guardar Matriz en excel
        Excel1.save(RESULT_FOLDER_PATH + "MatrizConfusion.xls")



