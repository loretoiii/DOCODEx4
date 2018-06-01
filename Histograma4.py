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

class histogram4(object):
    def __new__(cls, RESULT_FOLDER_PATH, SOURCES_FOLDER_PATH, lmdas, lista_porcentajes):

        data2 = xlrd.open_workbook(RESULT_FOLDER_PATH + 'MatrizConfusion.xls')
        j=2
        lista_F1 = list()
        lista_todos_f1 = list()
        #for j in range(93)
        for lista in range(3*len(lista_porcentajes)):
            print(str(lista))
            #print("Posicion j,i: ("+str(j)+",3)")
            if(lista ==11 or lista==22):
                lista_todos_f1.append(lista_F1)
                lista_F1 = list()
            xl_sheet = data2.sheet_by_index(lista+1)
            f1=xl_sheet.cell(j, 3).value
            #print(str(f1))
            lista_F1.append(str(f1))
            #print(str(lista_F1))
        j+=3
        lista_todos_f1.append(lista_F1)
        #print(str(lista_todos_f1))

        intento = list()
        for t in lista_porcentajes:
            intento.append("por-" + str(t))

        intento2 = list()
        for h in lmdas:
            intento2.append("lmda-" + str(h))
        trace1 = go.Heatmap(
            z=lista_todos_f1[0],
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cold'
        )
        trace2 = go.Heatmap(
            z=lista_todos_f1[1],
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cold'  # Cividis
        )
        trace3 = go.Heatmap(
            z=lista_todos_f1[2],
            x=intento,
            y=intento2,
            zmin=0,
            zmax=1,
            colorscale='Cold'  # Cividis
        )

        # Graficar
        #
        fig = tools.make_subplots(rows=1, cols=3,subplot_titles=('DOCODE', 'DOCODE-NORM', 'DOCODE-NOR-SEG'))
        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2, 1, 2)
        fig.append_trace(trace3, 1, 3)

        fig['layout'].update(height=1200, width=1200, title='F1')
        result = plotly.offline.plot(fig, filename=RESULT_FOLDER_PATH + 'F1.html')

