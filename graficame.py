from __future__ import division
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
import numpy
import mpmath
import xlwt
import xlrd
from xlutils.copy import copy

## graficame 4 es un grafico de los resutados como puntos y lineas con sus deltas, y boxplot
## graficame 4 = graficame 2 y graficame 3

#RESULT_FOLDER_PATH = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Results/'

class grafico(object):
    def __new__(cls,list_datos_docode, list_datos_normalizados, list_datos_segmentos,identificador,RESULT_FOLDER_PATH):
        #print (len(list_datos_docode))
        #print(str(list_datos_docode))
        #print(str(list_datos_normalizados))
        #print(str(list_datos_segmentos))


        resultado = open(RESULT_FOLDER_PATH + "Resultados.txt", "a")
        text_prueba = open(RESULT_FOLDER_PATH + "Trace2.txt", "a")
        text_prueba.write("Comienzo a graficar.\n")
        # DOCODE
        #resultado.write(str(identificador)+" DOCODE \n")
        ult=1
        estilos = list()
        lista_tracesD = list()
        lista_traces2 = list()
        lista_traces3 = list()
        lista_doc_conocidos = list()
        lista_dc_desconocidos = list()
        lista_result = list()
        lista_result_porcent = list()
        lista_estilos = list()
        cadapunto = list()
        cadapunto2 = list()
        #print("DOCODE")
        text_prueba.write("DOCODE.\n")

        for lista in list_datos_docode:
            text_prueba.write("Analizando lista:" + str(lista) + ".\n")
            lista_x = list()

            #estilo_por_doc = numpy.average(lista)
            #estilos.append(estilo_por_doc)
            #print(str(estilo_por_doc))
            for c in range(len(lista)):
                lista_x.append('Sd_u')
                nombre='Sd_u'

            if ult == len(list_datos_docode):
                ult=ult+1
                lista_dc_desconocidos = lista

                for t in lista:
                    cadapunto2.append(t)

            else:
                ult = ult + 1
                lista_x = list()
                conocidosstd = numpy.std(lista)
                lista_doc_conocidos.append(conocidosstd)
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)

                for t in lista:
                    cadapunto.append(t)
                    cadapunto2.append(t)

                for c in range(len(lista)):
                    lista_x.append('Sd')
                    nombre = 'Sd'
                    #lista_z.append(delta)

            trace = go.Scatter(
                x=lista_x,
                y=lista,
                mode = 'markers',
                name = 'docode texto'+str(ult-1)
            )
            if ult == len(list_datos_docode):
                lista_traces3.append(trace)
            else:
                lista_tracesD.append(trace)
        #print (str(lista))
        #print (str(lista_x))

        trace = go.Box(
            y = cadapunto ,
            name='Sd_b',
            boxpoints='suspected-outliers',
            marker=dict(
                color='rgba(255, 144, 14, 0.5)',
                outliercolor='rgba(219, 64, 82, 0.6)',
                line=dict(
                    outliercolor='rgba(219, 64, 82, 0.6)',
                    outlierwidth=2)),
            line=dict(
                color='rgba(255, 144, 14, 0.5)')
        )
        lista_traces2.append(trace)
        lista_tracesD=lista_traces2+lista_tracesD+lista_traces3


        #umbral
        #estilo promedio
        # 0.075

        delta = 0.075
        #print(str(lista_estilos))
        #print("lista doc conocidos: "+str())
        #estilo = numpy.average(lista_estilos)
        text_prueba.write("Lista de cada punto 2:" + str(cadapunto) + ".\n")
        estilo = numpy.average(cadapunto)
        text_prueba.write("Estilo Promedio:" + str(estilo) + ".\n")
        text_prueba.write("Delta:" + str(delta) + ".\n")
        #print(str(estilo))
        umbral = estilo - delta
        text_prueba.write("Umbral:" + str(umbral) + ".\n")
        #print(str(umbral))
        trace = go.Scatter(
            x=['Sd_b','Sd','Sd_u'],
            y=[umbral, umbral, umbral],

            mode = 'lines',
            name = 'docode umbral'
        )
        lista_tracesD.append(trace)
        #print(str(lista_dc_desconocidos))
        valores_finales = 0
        for d in lista_dc_desconocidos:
            text_prueba.write("Reviso el segmento d: " + str(d) +" >= umbral: "+str(umbral)+ "\n")
            if (float(d) >= float(umbral)):
                valores_finales = valores_finales + 1
            else:
                valores_finales = valores_finales + 0 #solo para dejar comentado la linea anterior
        text_prueba.write("Valor final:" + str(valores_finales) +"con largo de cantidad de d's: "+(str(len(lista_dc_desconocidos)))+"\n")
        final=(mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
        text_prueba.write("%pertenencia:" + str(final) + ".\n")
        #final = final.replace("mpf", "")
        #final = final.replace("(", "")
        #final = final.replace(")", "")
        lista_result_porcent.append(str(final))

        #print("final: "+str(final))
        if(float(final) >= 0.5):
            resultadoVF="V"
            lista_result.append("V")
        else:
            resultadoVF = "F"
            lista_result.append("F")
        text_prueba.write("resultado:" + str(resultadoVF) + ".\n")



        # DOCODE NORMALIZADO
        ult = 1
        lista_tracesN = list()
        estilos = list()
        lista_doc_conocidos = list()
        lista_dc_desconocidos = list()
        lista_estilos = list()
        lista_traces2 = list()
        cadapunto = list()
        cadapunto2 = list()
        lista_traces3 = list()
        text_prueba.write("DOCODE NORMALIZADO.\n")
        for lista in list_datos_normalizados:
            text_prueba.write("Analizando lista:" + str(lista) + ".\n")
            lista_x = list()

            for c in range(len(lista)):
                nombre='Sn_u'
                lista_x.append('Sn_u')

            if ult == len(list_datos_docode):
                ult = ult + 1
                lista_dc_desconocidos = lista

                for t in lista:
                    cadapunto2.append(t)

            else:
                ult = ult + 1
                lista_x = list()
                conocidosstd = numpy.std(lista)
                lista_doc_conocidos.append(conocidosstd)
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)

                for t in lista:
                    cadapunto.append(t)
                    cadapunto2.append(t)

                for c in range(len(lista)):
                    lista_x.append('Sn')
                    nombre = 'Sn'

            trace = go.Scatter(
                x=lista_x,
                y=lista,
                mode = 'markers',
                name = 'docode texto normalizado'+str(ult-1)
            )
            if ult == len(list_datos_docode):
                lista_traces3.append(trace)
            else:
                lista_tracesN.append(trace)

        trace = go.Box(
            y=cadapunto,
            name='Sn_b',
            boxpoints='suspected-outliers',
            marker=dict(
                color='rgba(44, 160, 101, 0.5)',
                outliercolor='rgba(219, 64, 82, 0.6)',
                line=dict(
                    outliercolor='rgba(219, 64, 82, 0.6)',
                    outlierwidth=2)),
            line=dict(
                color='rgba(44, 160, 101, 0.5)')
        )
        lista_traces2.append(trace)
        lista_tracesN = lista_traces2 + lista_tracesN + lista_traces3

        # umbral2
        # Por doc conocidos sacar desviacion estandar
        text_prueba.write("Lista de cada punto 2:" + str(cadapunto) + ".\n")
        std = numpy.std(cadapunto)
        text_prueba.write("STD:" + str(std) + ".\n")
        # 0.2
        a=0.2
        delta = a * std
        estilo = numpy.average(cadapunto)
        umbral = estilo + delta
        text_prueba.write("Estilo Promedio:" + str(estilo) + ".\n")
        text_prueba.write("Delta:" + str(delta) +" con a="+str(a)+ ".\n")
        text_prueba.write("Umbral:" + str(umbral) + ".\n")
        trace = go.Scatter(
            x=['Sn_b','Sn', 'Sn_u'],
            y=[umbral, umbral, umbral],

            mode='lines',
            name='docode normalizado umbral'
        )
        lista_tracesN.append(trace)
        text_prueba.write(str(identificador) + " Resultados DOCODE NORMALIZADO \n")
        valores_finales = 0
        for d in lista_dc_desconocidos:
            text_prueba.write("Reviso el segmento d: " + str(d) + " <= umbral: " + str(umbral) + "\n")
            if (float(d) <= float(umbral)):
                valores_finales = valores_finales + 1
            else:
                valores_finales = valores_finales + 0
        text_prueba.write("Valor final:" + str(valores_finales) + "con largo de cantidad de d's: " + (str(len(lista_dc_desconocidos))) + "\n")
        final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
        text_prueba.write("%pertenencia:" + str(final) + ".\n")
        lista_result_porcent.append(str(final))
        if (float(final) >= 0.5):
            resultadoVF = "V"
            lista_result.append("V")
        else:
            resultadoVF = "F"
            lista_result.append("F")
        text_prueba.write("resultado:" + str(resultadoVF) + ".\n")

        # DOCODE NORMALIZADO POR SEGMENTO
        text_prueba.write("DOCODE NORMALIZADO POR SEGMENTO.\n")
        ult = 1
        lista_tracesS = list()
        estilos = list()
        lista_traces2 = list()
        lista_traces3 = list()
        lista_doc_conocidos = list()
        lista_dc_desconocidos = list()
        lista_estilos = list()
        cadapunto = list()
        cadapunto2 = list()
        for lista in list_datos_segmentos:
            text_prueba.write("Analizando lista:" + str(lista) + ".\n")
            lista_x = list()

            for c in range(len(lista)):
                lista_x.append('Ss_u')
                nombre = 'Ss_u'

            if ult == len(list_datos_docode):
                ult = ult + 1
                lista_dc_desconocidos = lista

                for t in lista:
                    cadapunto2.append(t)

            else:
                ult = ult + 1
                lista_x = list()
                conocidosstd = numpy.std(lista)
                lista_doc_conocidos.append(conocidosstd)
                estilocu = numpy.average(lista)
                lista_estilos.append(estilocu)

                for t in lista:
                    cadapunto.append(t)
                    cadapunto2.append(t)

                for c in range(len(lista)):
                    lista_x.append('Ss')
                    nombre = 'Ss'

            trace = go.Scatter(
                x=lista_x,
                y=lista,
                mode = 'markers',
                name = 'docode texto norm por segmento'+str(ult-1)
            )
            if ult == len(list_datos_docode):
                lista_traces3.append(trace)
            else:
                lista_tracesS.append(trace)

        trace = go.Box(
            y = cadapunto,
            name = 'Ss_b',
            boxpoints = 'suspected-outliers',
            marker = dict(
                color='rgba(93, 164, 214, 0.5)',
                outliercolor='rgba(219, 64, 82, 0.6)',
                line=dict(
                    outliercolor='rgba(219, 64, 82, 0.6)',
                    outlierwidth=2)),
            line = dict(
                color='rgba(93, 164, 214, 0.5)')
        )
        lista_traces2.append(trace)
        lista_tracesS = lista_traces2 + lista_tracesS + lista_traces3


        # umbral2
        # estilo promedio

        estilo = numpy.average(cadapunto)
        std = numpy.std(cadapunto)
        text_prueba.write("Lista de cada punto 2:" + str(cadapunto) + ".\n")
        # 0.8
        a = 0.8
        delta = a * std
        umbral = estilo + delta
        text_prueba.write("Delta:" + str(delta) + " con a=" + str(a) + ".\n")
        text_prueba.write("Estilo Promedio:" + str(estilo) + ".\n")
        text_prueba.write("Delta:" + str(delta) + ".\n")

        trace = go.Scatter(
            x=['Ss_b','Ss', 'Ss_u'],
            y=[umbral, umbral, umbral],

            mode='lines',
            name='docode normalizado por segmento umbral'
        )
        lista_tracesS.append(trace)
        valores_finales = 0
        for d in lista_dc_desconocidos:
            text_prueba.write("Reviso el segmento d: " + str(d) + " <= umbral: " + str(umbral) + "\n")
            if (float(d) <= float(umbral)):
                valores_finales = valores_finales + 1
            else:
                valores_finales = valores_finales + 0
        text_prueba.write("Valor final:" + str(valores_finales) + "con largo de cantidad de d's: " + (str(len(lista_dc_desconocidos))) + "\n")
        final = (mpmath.mpf(valores_finales) / mpmath.mpf(len(lista_dc_desconocidos)))
        text_prueba.write("%pertenencia:" + str(final) + ".\n")
        lista_result_porcent.append(str(final))
        if (float(final) >= 0.5):
            resultadoVF = "V"
            lista_result.append("V")
        else:
            resultadoVF = "F"
            lista_result.append("F")

        text_prueba.write("resultado:" + str(resultadoVF) + ".\n")



        resultado.write(str(identificador)+" "+str(lista_result)+" - "+str(lista_result_porcent)+" \n")



        #Graficar
        lista_traces = list()
        lista_traces = lista_tracesD+lista_tracesN+lista_tracesS
        data = lista_traces
        result = plotly.offline.plot(data, filename=RESULT_FOLDER_PATH+"/GraficosPorCarpeta/"+str(identificador)+'-scatter-resultados'+str(ult-1)+'.html')
        #print(str(result))
        resultado.close()
        text_prueba.close()

        return str(identificador)+'scatter-resultados'+str(ult-1)+'.html'