#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Algoritmo para clasificar los textos sospechosos contenidos en 
#el corpus de pruebas del concurso PAN @ CLEF 2011 según el 
#porcentaje de plagio.

import glob
import xmltodict
from shutil import copyfile

SOURCES_FOLDER = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Sources/'
PARTS = ['part1/','part2/','part3/','part4/','part5/',
         'part6/','part7/','part8/','part9/','part10/',
         'part11/','part12/','part13/','part14/','part15/',
         'part16/','part17/','part18/','part19/','part20/',
         'part21/','part22/','part23/','part24/','part25/',
         'part26/','part27/','part28/','part29/','part30/',
         'part31/','part32/']
ANNOTATIONS_FOLDER = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Annotations/'
ANNOTATIONS_FOLDER_2 = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Annotations2/'
DETECTIONS_FOLDER = '/home/loretoi/MEMORIA/Memoria-DOCODEx3-master/DOCODEX3/Detections/'

POCO_PLAGIO = 10.0
MEDIO_PLAGIO = 25.0

#-- --------------------------------------------------------------

def fileList(path, extension):
  return glob.glob(path+'*.'+extension)

#-- --------------------------------------------------------------

def xml(file_path):
  t = open(file_path,"r").read()
  xml_dict = xmltodict.parse(t)
  return xml_dict

#-- --------------------------------------------------------------

def copy_file(filename, part, clasification):
  copyfile(ANNOTATIONS_FOLDER+part+filename, ANNOTATIONS_FOLDER+clasification+filename)
  copyfile(ANNOTATIONS_FOLDER_2+part+filename, ANNOTATIONS_FOLDER_2+clasification+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_1/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_1/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_2/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_2/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_3/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_3/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_4/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_4/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_5/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_5/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_6/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_6/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_7/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_7/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_8/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_8/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_9/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_9/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_10/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_10/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_11/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_11/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_12/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_12/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_13/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_13/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_14/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_14/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_15/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_15/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_16/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_16/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_17/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_17/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_18/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_18/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_19/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_19/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_20/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_20/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_21/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_21/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_22/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_22/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_23/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_23/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_24/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_24/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_25/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_25/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_26/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_26/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_27/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_27/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_28/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_28/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_29/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_29/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO/lambda_30/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO/lambda_30/'+filename)
  #DOCODE NORMALIZADO X SEGMENTO
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_1/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_1/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_2/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_2/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_3/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_3/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_4/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_4/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_5/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_5/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_6/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_6/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_7/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_7/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_8/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_8/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_9/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_9/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_10/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_10/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_11/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_11/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_12/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_12/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_13/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_13/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_14/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_14/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_15/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_15/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_16/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_16/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_17/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_17/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_18/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_18/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_19/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_19/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_20/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_20/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_21/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_21/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_22/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_22/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_23/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_23/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_24/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_24/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_25/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_25/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_26/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_26/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_27/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_27/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_28/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_28/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_29/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_29/'+filename)
  copyfile(DETECTIONS_FOLDER+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_30/'+filename, DETECTIONS_FOLDER+clasification+'DOCODE_NORMALIZADO_SEGMENTO/lambda_30/'+filename)

#-- --------------------------------------------------------------

def clasificador():
  for part in PARTS:
    print SOURCES_FOLDER+part
    file_list = fileList(SOURCES_FOLDER+part, 'xml')
    files = []

    for xml_file in file_list:
      filename = xml_file.replace(SOURCES_FOLDER+part,'').replace('.xml/','')
      txt_file = xml_file.replace('xml','txt')
      words = len(open(txt_file,"r").read())
      
      plagiarism = 0
      xml_dict = xml(xml_file)
      for f in xml_dict['document']['feature'] :
        if f['@name'] == 'plagiarism':
          plagiarism += int(f['@this_length'])
      percentage = (float(plagiarism)/float(words))*100.0
      #Movemos a la carpeta correspondiente
      if percentage < POCO_PLAGIO:
        print filename
        copy_file(filename, part, 'poco/')
      elif percentage < MEDIO_PLAGIO:
        copy_file(filename, part, 'medio/')
      else:
        copy_file(filename, part, 'mucho/')

#-- --------------------------------------------------------------
#-- --------------------------------------------------------------
#-- --------------------------------------------------------------
if __name__ == "__main__":
  clasificador()
