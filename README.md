# DOCODEx4
Nuevo algoritmo para la atribución de autores basado en n-gramas
Source:

Directorio principal en la cual se dispondrá de todas las carpetas a analizar y el archivo de texto truth.txt si es que se desea analizar las respuestas de dicho análisis. 
    
Result:

Directorio principal que se utilizará para dejar la carpeta de resultados obtenida de una ejecución. Como cada carpeta se identifica con el $n$ utilizado en la prueba, el día con la hora, minutos y segundos de creación, no existirá problema de sobre-escritura al ejecutar los mismos experimentos.
    
Fases
    Directorio que contiene las fuentes de los experimentos descritos en la sección \ref{sec:fases} y sus correspondientes resultados. 
    
VerificacionAutores.py
    Script principal que toma las carpetas de \textbf{Source} y los analiza. De este archivo ejecutaremos todos los demás script. Sus principales características son que, define las direcciones de Source y Result, toma las variables más importantes ($m,n,$,$\lambda$'s, lista de porcentajes y segmento limitante si se desea utilizar uno en específico) definidas al comienzo del archivo y con la cual se realiza el trabajo entre los textos conocidos y desconocidos.
    
text2.py
    Clase que realiza el preprocesamiento al texto a analizar y contiene los métodos docode, docode_normalizado y docode_normalizado_segmento.
    
graficame4.py
    Script que genera un gráfico de distribución con cada punto obtenido de cada segmento analizado, tanto de los documentos conocidos como de los desconocidos, y por cada algoritmo analizado: docode, docode_normalizado y docode_normalizado_segmento.
    
umbrales1.py
    Script que genera 3 archivos excels, uno por cada algoritmo analizado, en los cuales se revisa cada carpeta con cada $\lambda$ para obtener el porcentaje de pertenencia de cada una de ellas. 
    
GraficarResultados.py
    Script que utiliza los archivos generados por umbrales1 para generar la gráfica de cada porcentaje de pertenencia obtenido e identificarlo si se trata de una respuesta positiva (el autor del texto desconocido era quien había escrito los textos conocidos) o no.
    
MatrizCondusion.py
    Script que genera un archivo en excel que dispone de todas las combinaciones de algoritmos, $\lambda$'s y porcentaje de pertenencia utilizado, señalando el $F_1$, Precision y Recall obtenido por cada una de estas combinaciones. También genera los histogramas de $F_1$ y de aciertos, el primero con cada $F_1$ obtenido con el objetivo de identificar claramente las mejores métricas de $F_1$ por algoritmo y el segundo, con cada acierto obtenido (\textit{True Positive} y \textit{True Negative}) con el objetivo de identificar claramente la configuración que obtuvo una mayor cantidad de aciertos considerando todas las carpetas analizadas.  
    
Histograma.py
    Script que genera gráficos de histograma, por cada algoritmo analizado, con la cantidad de carpetas clasificadas como verdaderas y cantidad de carpetas clasificadas como falsas para cada combinación del archivo generado por MatrizCondusion.
    
Histograma2.py
    Script que genera por algoritmo un gráfico que representa por porcentaje de pertenencia y cada $\lambda$'s la cantidad de aciertos y rechazos obtenidos. 
    
B0B1.py
    Script que con carpetas conocidas muestra la mejor configuración de $\lambda$ y segmento limitante que genera un $F_1$ óptimo.Esto lo gráfica mostrando un histograma donde por cada $\lambda$ y segmento limitante nos dirán si el segmento debe considerarse como verdadero(0) o falso(1), considerando verdadero como escrito por el autor. Para carpetas desconocidas se revisará la configuración realizada con el segmento limitante ya fijo y se podrá revisar los valores obtenidos para $F_1$ y el total de aciertos.
