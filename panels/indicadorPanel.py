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
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
import os
from .operations import operations
from .stylesIndicadorPanel import styleIndicadorPanel
from ..calculations.dataQuery import queriesData
from ..calculations.spatialQuery import spatialQueries
import tempfile

class indicadorPanel(QgsHtmlAnnotation):
    def __init__(self,layer,type,title,expression,threshold,range,estilo='angular',anchoP=80,altoP=40.0,\
    colorBar="blue",colorBackground='white',colorTit='black',sizeTitle=10,colorValue='black',\
    colorBase='lightgray',colorLine='red',sizeLabel=10,colorFinal='#B31101',\
    colorMark='red',relative=False):
        super().__init__()
        
        self.capa= layer
        self.title=title
        print(self.title)
        self.threshold=threshold
        self.range=range
        #CAPA PARA ANALISIS DE CONSULTAS INTERSECCIONES
        self.capa2=None 
        #---------------------------------------------

        self.colorTit=colorTit
        self.colorBar=colorBar
        self.colorBackground=colorBackground
        self.colorTit=colorTit
        self.colorBase=colorBase
        self.sizeTitle=sizeTitle
        self.colorLine=colorLine
        self.sizeLabel=sizeLabel
        self.colorFinal=colorFinal
        self.colorMark=colorMark
        self.colorValue=colorValue
        self.relative=relative
        
        self.tipo= type
        self.estilo=estilo
        self.expresion=expression
        
        self.anchop=anchoP
        self.altop=altoP

        self.iniHtml=''
        self.ahtml=None
        
        self.tempf=None
        
        self.setFrameSizeMm(QSizeF(self.anchop,self.altop))
        self.setFrameOffsetFromReferencePoint(QPointF(0, 0))
        self.conectar()
        self.data=self.defData()
        print('en indicador ',self.estilo,self.data)
        
        self.assignStyle()
        self.cierreHtml()
        
    def conectar(self):
        self.capa.selectionChanged.connect(self.updateValue)
    
    def desconectar(self):
        self.capa.selectionChanged.disconnect(self.updateValue)
    
    def assignStyle(self):
        self.style=styleIndicadorPanel(self.data,self.threshold,self.range,title=self.title,\
            colorTit=self.colorTit,sizeTitle=self.sizeTitle,colorBar=self.colorBar,\
            estilo=self.estilo,colorBackground=self.colorBackground,colorBase=self.colorBase,\
            colorLine=self.colorLine,sizeLabel=self.sizeLabel,colorFinal=self.colorFinal,\
            colorValue=self.colorValue,colorMark=self.colorMark,relative=self.relative)
        self.style.assignStyle(self.estilo)
    
    def defData(self):
        calculador=operations(self,self.tipo)
        val=calculador.listOperations[self.tipo]()
        print('en indicador defdata ',val,self.tipo)
        return str(val)
    
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
        self.assignStyle()
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
    
    
    
    