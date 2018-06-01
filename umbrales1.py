import xlwt
import xlrd
from xlutils.copy import copy
import mpmath
#from xlrd import open_workbook
import numpy
import time
import os.path

SOURCES_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Sources/'

class umbral(object):
    def __new__(cls,list_datos_docode, list_datos_normalizados, list_datos_segmentos,identificador, RESULT_FOLDER_PATH,lmdas):

        #print("identificador: " + str(identificador))
        if identificador==1:
            listasolreal = list()
            listacarpetas = list()
            if(os.path.isfile(SOURCES_FOLDER_PATH+"truth.txt")):

                soluciones = open(SOURCES_FOLDER_PATH+"truth.txt","r")
                for linea in soluciones.readlines():
                    #print linea
                    if linea != '':
                        carpeta,solucion=linea.split(" ")
                        listacarpetas.append(carpeta)
                        listasolreal.append(solucion)
                soluciones.close()
                #print("lista carpetas: "+str(listacarpetas))

                # Crear Excel Result General
                resultado = xlwt.Workbook()
                resultado1 = resultado.add_sheet("Hoja1")

                resultado1.write(0, 0, "Carpeta")
                resultado1.write(0, 1, "Solucion Real")
                resultado1.write(0, 2, "Solucion DOCODE")

                for filas in range(len(listacarpetas)):
                    resultado1.write(filas + 1, 0, listacarpetas[filas])
                    resultado1.write(filas + 1, 1, listasolreal[filas])
                # Guardar archivos
                resultado.save(RESULT_FOLDER_PATH + "Result.xls")

                # Crear Excel DOCODE
                resultado = xlwt.Workbook()
                resultado1 = resultado.add_sheet("Hoja1")
                resultado1.write(0, 0, "Carpeta")
                resultado1.write(0, 1, "Solucion Real")
                for fila in range(len(listacarpetas)):
                    resultado1.write(fila + 1, 0, listacarpetas[fila])
                    resultado1.write(fila + 1, 1, listasolreal[fila])

                # Crear Excel DOCODE NORMALIZADO
                resultado = xlwt.Workbook()
                resultado1 = resultado.add_sheet("Hoja1")
                resultado1.write(0, 0, "Carpeta")
                resultado1.write(0, 1, "Solucion Real")
                for fila in range(len(listacarpetas)):
                    resultado1.write(fila + 1, 0, listacarpetas[fila])
                    resultado1.write(fila + 1, 1, listasolreal[fila])


                # Crear Excel DOCODE NORMALIZADO POR SEGMENTO
                resultado = xlwt.Workbook()
                resultado1 = resultado.add_sheet("Hoja1")
                resultado1.write(0, 0, "Carpeta")
                resultado1.write(0, 1, "Solucion Real")
                for fila in range(len(listacarpetas)):
                    resultado1.write(fila + 1, 0, listacarpetas[fila])
                    resultado1.write(fila + 1, 1, listasolreal[fila])

                for a in range(len(lmdas)):
                    resultado1.write(0, a + 2, "a=" + str(lmdas[a]))

                # Guardar archivos
                resultado.save(RESULT_FOLDER_PATH + "ResultDOCODE.xls")
                resultado.save(RESULT_FOLDER_PATH + "ResultDOCODENORM.xls")
                resultado.save(RESULT_FOLDER_PATH + "ResultDOCODENORM-POR-SEG.xls")


            else:
                print("El archivo de soluciones no existe en la carpeta: \n "+SOURCES_FOLDER_PATH)
                # devolver error


        #Crear excel para hacer trace
        text_prueba = open(RESULT_FOLDER_PATH + "Trace2.txt", "a")
        text_prueba.write("\n \n Comienzo a revisar en UMBRALES.\n")
        text_prueba.write("\n DOCODE General.\n")


        # Result General
        ult = 1
        lista_dc_desconocidos = list()
        lista_estilos = list()
        lista_result_porcent = list()
        for lista in list_datos_docode:
            if ult == len(list_datos_docode):
                ult = ult + 1
                lista_dc_desconocidos = lista
            else:
                ult = ult + 1
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)

        lista_result = list()
        delta = 0.075
        #print(str(lista_estilos))
        estilo = numpy.average(lista_estilos)
        #print(str(estilo))
        #print(str(delta))
        umbral = float(estilo) - float(delta)
        #print(str(umbral))

        valores_finales = 0
        for d in lista_dc_desconocidos:
            text_prueba.write("analizando dc: "+str(d) +" > umbral: "+str(umbral)+"\n")
            if (float(d) > float(umbral)):
                valores_finales = valores_finales + 1
            else:
                valores_finales = valores_finales + 0  # solo para dejar comentado la linea anterior

        final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
        text_prueba.write("valor final: " + str(mpmath.mpf(valores_finales)) + "\n")
        text_prueba.write("largo doc: " + str(mpmath.mpf(len(lista_dc_desconocidos))) + "\n")
        text_prueba.write("final: " + str(final) + "\n")
        libro = xlrd.open_workbook(RESULT_FOLDER_PATH + "Result.xls", formatting_info=True)
        wb = copy(libro)
        ws = wb.get_sheet("Hoja1")
        ws.write(identificador, 2, str(final))
        wb.save(RESULT_FOLDER_PATH + "Result.xls")

        # DOCODE NORMALIZADO
        text_prueba.write("\n DOCODE \n")
        ult = 1
        lista_dc_desconocidos = list()
        lista_estilos = list()
        lista_conocidos = list()

        for lista in list_datos_normalizados:

            if ult == len(list_datos_normalizados):
                ult = ult + 1
                lista_dc_desconocidos = lista
            else:
                ult = ult + 1
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)
                for t in lista:
                    lista_conocidos.append(t)

        estilo = numpy.average(lista_estilos)
        text_prueba.write("Lista conocidos: " + str(lista_conocidos) + "\n")
        std = numpy.std(lista_conocidos)
        text_prueba.write("Estilo: " + str(estilo) + "\n")
        text_prueba.write("STD: " + str(std) + "\n")
        for a in range(len(lmdas)):
            result = 0
            text_prueba.write("lmda: " + str(lmdas[a]) + "\n")
            delta = float(lmdas[a]) * float(std)
            text_prueba.write("delta: " + str(delta) + "\n")
            umbral = float(estilo) - float(delta)
            text_prueba.write("umbral: " + str(umbral) + "\n")
            valores_finales = 0
            for d in lista_dc_desconocidos:
                text_prueba.write("Con lambda: " + str(lmdas[a]) + " - analizando dc: " + str(d) + " > umbral: " + str(umbral) + "\n")
                if float(d) > float(umbral):
                    valores_finales = valores_finales + 1
                else:
                    valores_finales = valores_finales + 0  # solo para dejar comentado la linea anterior

            final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
            text_prueba.write("valor final: " + str(mpmath.mpf(valores_finales)) + "\n")
            text_prueba.write("largo doc: " + str(mpmath.mpf(len(lista_dc_desconocidos))) + "\n")
            text_prueba.write("final: " + str(final) + "\n")

            libro = xlrd.open_workbook(RESULT_FOLDER_PATH + "ResultDOCODE.xls", formatting_info=True)
            wb = copy(libro)
            ws = wb.get_sheet("Hoja1")
            ws.write(identificador, a + 2, str(final))
            wb.save(RESULT_FOLDER_PATH + "ResultDOCODE.xls")

        # DOCODE NORMALIZADO
        text_prueba.write("\nDOCODE NORMALIZADO.\n")
        ult = 1
        lista_dc_desconocidos = list()
        lista_estilos = list()
        lista_conocidos = list()

        for lista in list_datos_normalizados:

            if ult == len(list_datos_normalizados):
                ult = ult + 1
                lista_dc_desconocidos = lista
            else:
                ult = ult + 1
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)
                for t in lista:
                    lista_conocidos.append(t)

        estilo = numpy.average(lista_estilos)
        text_prueba.write("Lista conocidos: " + str(lista_conocidos) + "\n")
        std = numpy.std(lista_conocidos)
        text_prueba.write("Estilo: " + str(estilo) + "\n")
        text_prueba.write("STD: " + str(std) + "\n")
        for a in range(len(lmdas)):
            result=0
            text_prueba.write("lmda: " + str(lmdas[a]) + "\n")
            delta=float(lmdas[a]) * float(std)
            text_prueba.write("delta: " + str(delta) + "\n")
            umbral = float(estilo) + float(delta)
            text_prueba.write("umbral: " + str(umbral) + "\n")
            valores_finales = 0
            for d in lista_dc_desconocidos:
                text_prueba.write("Con lambda: "+str(lmdas[a])+" - analizando dc: " + str(d) + " < umbral: " + str(umbral) + "\n")
                if float(d) < float(umbral):
                    valores_finales = valores_finales + 1
                else:
                    valores_finales = valores_finales + 0  # solo para dejar comentado la linea anterior

            final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
            text_prueba.write("valor final: " + str(mpmath.mpf(valores_finales)) + "\n")
            text_prueba.write("largo doc: " + str(mpmath.mpf(len(lista_dc_desconocidos))) + "\n")
            text_prueba.write("final: " + str(final) + "\n")

            libro = xlrd.open_workbook(RESULT_FOLDER_PATH + "ResultDOCODENORM.xls", formatting_info=True)
            wb = copy(libro)
            ws = wb.get_sheet("Hoja1")
            ws.write(identificador, a+2, str(final))
            wb.save(RESULT_FOLDER_PATH + "ResultDOCODENORM.xls")


        # DOCODE NORMALIZADO POR SEGMENTO
        text_prueba.write("\nDOCODE NORMALIZADO POR SEGMENTO.\n")
        ult = 1
        lista_dc_desconocidos = list()
        lista_estilos = list()
        lista_conocidos = list()
        for lista in list_datos_segmentos:
            if ult == len(list_datos_segmentos):
                ult = ult + 1
                lista_dc_desconocidos = lista
            else:
                ult = ult + 1
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)
                for t in lista:
                    lista_conocidos.append(t)

        estilo = numpy.average(lista_estilos)
        std = numpy.std(lista_conocidos)

        for a in range(len(lmdas)):
            result = 0
            delta = float(lmdas[a]) * float(std)
            umbral = estilo + delta
            valores_finales = 0
            for d in lista_dc_desconocidos:
                text_prueba.write("Con lambda: " + str(lmdas[a]) + " - analizando dc: " + str(d) + " < umbral: " + str(umbral) + "\n")
                if float(d) < float(umbral):
                    valores_finales = valores_finales + 1
                else:
                    valores_finales = valores_finales + 0  # solo para dejar comentado la linea anterior
            final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
            text_prueba.write("valor final: " + str(mpmath.mpf(valores_finales)) + "\n")
            text_prueba.write("largo doc: " + str(mpmath.mpf(len(lista_dc_desconocidos))) + "\n")
            text_prueba.write("final: " + str(final) + "\n")

            libro = xlrd.open_workbook(RESULT_FOLDER_PATH + "ResultDOCODENORM-POR-SEG.xls", formatting_info=True)
            wb = copy(libro)
            ws = wb.get_sheet("Hoja1")
            ws.write(identificador, a+2, str(final))
            wb.save(RESULT_FOLDER_PATH + "ResultDOCODENORM-POR-SEG.xls")

        #Cerrar trace
        text_prueba.close()