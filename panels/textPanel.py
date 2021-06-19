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
from qgis import PyQt
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.core import *
import random
import os
from .operations import operations
from .stylesTextPanel import styleTextPanel
from ..calculations.dataQuery import queriesData
from ..calculations.spatialQuery import spatialQueries
import tempfile

class textPanel(QgsHtmlAnnotation):
    def __init__(self,canvas,layer,type,title,expression,position='top-left',anchoP=150,altoP=100,\
    fondTit='black',colorTextTit='white',fondVal='lightblue', colorTextVal='black',\
    suavizado=0,estilo='cuadrado',icono=False,rutaIcono=None,toolTip=False,\
    direccionIcono='center',colorIcono=0):
        super().__init__()
        self.posicion=position
        self.capa= layer
        
        self.spatialOperation='processing'
        self.tipo= type
        self.expresion=expression
        self.canvas = canvas
        
        self.title=title
        self.estilo=estilo
        self.fondTit=fondTit
        self.colorTextTit=colorTextTit
        self.fondVal=fondVal
        self.colorTextVal=colorTextVal
        self.suavizado=suavizado
        self.icono=icono
        self.rutaIcono=rutaIcono
        self.direccionIcono=direccionIcono
        self.colorIcono=colorIcono
        
        self.setMapLayer(self.capa)
        self.anchop=anchoP
        self.altop=altoP
        
        #CAPA PARA ANALISIS DE CONSULTAS INTERSECCIONES
        self.capa2=None 
        #---------------------------------------------
        #INDICE ESPACIAL
        self.indiceE=None
        
        self.anchoF=anchoP
        self.altoF=altoP
        self.valor=self.defValor()
        self.style=styleTextPanel(title=self.title,fondTit=self.fondTit,colorTextTit=self.colorTextTit,\
                fondVal=self.fondVal,colorTextVal=self.colorTextVal,estilo=self.estilo, icono=self.icono,\
                suavizado=self.suavizado,rutaIcono=self.rutaIcono,direccionIcono=self.direccionIcono,colorIcono=self.colorIcono)
        self.style.value=self.valor
        self.asignarEstilo()
        self.ahtml=None
        self.anchoF=self.anchop+15
        self.altoF=self.altop+25
        self.setFrameSize(QSizeF(self.anchoF,self.altoF))
        self.tempf=None
        self.setFrameOffsetFromReferencePoint(QPointF(0, 0))
        self.conectar()
        self.cierreHtml()
    
    #temporal 
    def asignarEstilo(self):
        self.style.assignStyle(self.estilo)
    
    def asignarIndEspacial(self, indexS):
#        print('asignando indice espacial')
        self.indiceE=indexS
        
    def conectar(self):
        print('actualizar')
        self.capa.selectionChanged.connect(self.updateValue)
    
    def desconectar(self):
        self.capa.selectionChanged.disconnect(self.conectar)
    
    def defValor(self):
        calculador=operations(self,self.tipo)
        val=calculador.listOperations[self.tipo]()
        return val
        
    def cierreHtml(self):
        texto="0"
        self.tempf=tempfile.NamedTemporaryFile(mode='w+t',prefix='qd',suffix='.html',delete=False)
        print(self.tempf.name)
        self.tempf.seek(0)
        self.tempf.write(self.style.html)
        self.tempf.close()
        if os.path.exists(self.tempf.name):
            self.setSourceFile(self.tempf.name)
        else:
            print('el archivo temporal no existe')

    def updateValue(self):
        valor=self.defValor()
        self.valor=valor
        self.style.value=self.valor
        self.style.assignStyle(self.style.style)
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
        except:
            pass

    def colorTextTitle(self,color):
        self.style.colorFontTitle=color
        self.style.update()
        self.update()

    def colorBackTitle(self,color):
        self.style.colorTitle=color
        self.style.update()
        self.update()
        
    def colorTextValue(self,color):
        self.style.colorFontValue(color)
        self.style.update()
        self.update()
            
    def colorBackValue(self,color):
        self.style.colorValue(color)
        self.style.update()
        self.update()
        
            