# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISDashboard
                                 A QGIS plugin
 This plugin allows the construction and management of Dashboards on screen.
                              -------------------
        begin                : 2021-06-14
        git sha              : https://github.com/luisCartoGeo/QGIS_Dashboard
        copyright            : (C) 2021 by Luis Eduardo Perez https://www.linkedin.com/in/luisedpg/
        email                : luis3176@yahoo.com
 ***************************************************************************/
 """
import os
import random
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.core import *
from .stylesSeriePanel import styleSeriePanel
from ..calculations.dataQuery import queriesData
from ..myUtils.myUtils import utils
import tempfile

class seriesPanel(QgsHtmlAnnotation):
    def __init__(self,layer,expression,title='',estilo='multiple_fields',nselect=5,\
    wordBreak=False,position='top-left',anchoP=80,altoP=40.0,sizeTitle=12,colorTit='black',\
    colorLabels='black',sizeLabels=9,widthline=1,fill=False):
        super().__init__()
        self.capa=layer
        self.tipo='multiple_fields'
        
        self.title=title
        self.wordBreak=wordBreak
        self.colorTit=colorTit
        self.sizeTitle=sizeTitle
        self.colorLabels=colorLabels
        self.sizeLabels=sizeLabels
        self.widthline=widthline
        self.fill=fill
        self.registerSelect=nselect
        self.select=False
        
        self.posicion=position

        self.expresion=expression
        self.anchop=anchoP
        self.altop=altoP
        #guardamos aqui el ancho y alto luego de considerar 
        #los espacios por los estilos html 
        self.iniHtml=''
        
        self.tempf=None
    
        self.setFrameSizeMm(QSizeF(self.anchop,self.altop))
        self.setFrameOffsetFromReferencePoint(QPointF(0, 0))
        self.conectar()
        self.data=self.defData()
        self.style=self.assignStyle()
        self.cierreHtml()
            
    def conectar(self):
        self.capa.selectionChanged.connect(self.updateValue)
    
    def desconectar(self):
        self.capa.selectionChanged.disconnect(self.conectar)
    
    def assignStyle(self):
        if self.tipo=='multiple_fields':
            estilo=styleSeriePanel(self.data,title=self.title,select=self.select,\
            fill=self.fill,wordBreak=self.wordBreak,colorTit=self.colorTit,\
            sizeTitle=self.sizeTitle,colorLabels=self.colorLabels,\
            sizeLabels=self.sizeLabels,widthline=self.widthline)
        estilo.assignStyle(estilo.style)
        return estilo
    
    def defData(self):
        camposy=self.expresion[0]#Lista con nombre de campos numericos
        campox=self.expresion[1] #Nombre del campo categorico
    
        if self.capa.selectedFeatureCount()==0:
            self.select=False
            result=queriesData.summarizeFields(self.capa.getFeatures(),camposy)
        elif self.capa.selectedFeatureCount()>0:
            self.select=True
            result=queriesData.valuesSelectRegister(self.capa.selectedFeatures(),campox,\
            camposy,self.registerSelect)
        return result
    
    def cierreHtml(self):
        self.tempf=tempfile.NamedTemporaryFile(mode='w+t',prefix='qd',suffix='.html',delete=False)
        self.tempf.seek(0)
        self.tempf.write(self.style.html)
        self.tempf.close()
        if os.path.exists(self.tempf.name):
            self.setSourceFile(self.tempf.name)
        else:
            print('el archivo temporal no existe')
    
    def updateValue(self):    
        self.data=self.defData()
        self.style=self.assignStyle()
        if os.path.exists(self.tempf.name):
            if os.access(self.tempf.name,os.W_OK):
                with open(self.tempf.name,'w+t') as file:
                    file.write(self.style.html)
            else:
                print('no hay acceso de escritura')
        else:
            print('el archivo no existe')
        self.setSourceFile(self.tempf.name)
    
    def update(self):
        if os.path.exists(self.tempf.name):
            if os.access(self.tempf.name,os.W_OK):
                with open(self.tempf.name,'w+t') as file:
                    file.write(self.style.html)
            else:
                print('no hay acceso de escritura')
        else:
            print('el archivo no existe')
        self.setSourceFile(self.tempf.name)
    
    def borrarHtml(self):
        try:
            os.remove(self.tempf.name)
        except Exception as e:
            print(e)
