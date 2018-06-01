#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import xmltodict
import numpy as np
from gramas import ngramas

from collections import Counter
import sys
class TEXT:
  r = re.compile(r"[^a-z]", re.IGNORECASE)

  def __init__(self, txt_path, m, n):
    self.tt, self.tti, self.pv = [], [], []
    self.txt_path = txt_path
    self.m = m
    with open(self.txt_path,'r') as f:
        self.text = f.read()
    self.lower_text = self.text.lower()
    self.re_text = self.r.sub(' ', self.lower_text)
    self.split_text = self.re_text.split(' ')

    #cantidad de caracteres
    largo_txt=len(self.text)
    i = 0
    #texto limpio
    #print(str(self.r.sub(' ',self.text[i:len(self.lower_text)])))
    self.preprocess_segment(self.r.sub(' ',self.text[i:len(self.lower_text)]), self.tt, self.tti, self.pv, 0, i, n)
    #Sacamos las palabras repetidas
    self.vocabulary = list(set(self.tt))
    #Expresamos el texto como conjunto de numeros, a todas las palabras del diccionario las enumeramos
    self.vocabulary_dict = {value: key for key, value in enumerate(self.vocabulary)}
    # Enumera todas las palabras del vocabulario dandole la posicion a cada una
    self.ptt = [self.vocabulary_dict[w] for w in self.tt]


    #palabras totales
    self.total_words = len(self.ptt)
    #cuantas veces aparece la palabra de nuestro vocabulario
    self.frequency = Counter(self.ptt)
    #hace un vector con la frecuencia de las palabras del vocabulario
    self.frequency_vector = self.frequency.values()

    #normaliza el vector por su frecuencia por el numero total de palabras
    self.normalized_frequency_vector = [float(x)/self.total_words for x in self.frequency_vector]


  def preprocess_segment(self, segment, tt, tti, pv, plagio_state, index, n):
    #segment = texto limpio, sin caracteres raros y en lowercase
    # tt, tti, pv son listas vacias
    #plagios_state
    aux_tt = []
    aux_tti = []
    #Texto en una lista (aun con espacios)
    st = segment.split(' ')
    #Se le sacan los espacios
    for w in st:
        if w != '':
            aux_tt.append(w)
            aux_tti.append(index)
            index += len(w)+1 #+1 asume el corrimiento necesario para considerar el espacio eliminado por el split()
        else:
            index += 1
    #print("Lista de todas las palabras")

    textito = ngramas(aux_tt, n)
    #print("lista ngramas-->")
    #print(str(textito))

    #no se debiese ocupar en verificacion de autores
    #pv += [plagio_state]*len(aux_tt)
    #lista de todas las palabras
    #tt += aux_tt
    tt += textito
    #lista de index, nos da la posicion de cada palabra en el texto
    tti += aux_tti


  def segment_style(self, fulltext_vector, segment_vector, sl):
      d = [np.abs(float(fulltext_vector[j] - segment_vector[j]))/np.abs(float(fulltext_vector[j] + segment_vector[j]))/sl for j in range(0, len(segment_vector)) ]
      return sum(d), d

  def docode(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1

    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m - 1 if i*m - 1 < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]

      #Algoritmo 1 - DOCODE NORMAL
      sv_values = [float(x) for x in s_frecuency.values()]
      #calculamos diferencias
      s_style, d = self.segment_style(s_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": s_ftv, "differences": d, "plagio": False})
      #print '[SIMPLE] segmento: %s, valor d: %f' % (str(i), s_style)
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}


  def docode_normalizado(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1

    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m if i*m < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]

      N = float(len(s))
      sv_values = [float(x)/N for x in s_frecuency.values()]
      #calculamos diferencias
      s_style, d = self.segment_style(s_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": s_ftv, "differences": d, "plagio": False})
      #print '[NORM] segmento: %s, valor d: %f' % (str(i), s_style)
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}


  def docode_normalizado_segmento(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1

    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m if i*m < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]

      Ns = float(len(s))
      sv_values = [float(x)/Ns for x in s_frecuency.values()]
      #Normalizamos el vector generado anteriormente
      Nsftv = float(sum(s_ftv))
      ns_ftv = [float(x)/Nsftv for x in s_ftv ]
      #calculamos diferencias
      s_style, d = self.segment_style(ns_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": ns_ftv, "differences": d, "plagio": False})
      #print '[NORMSEG] segmento: %s, valor d: %f' % (str(i), s_style)
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}