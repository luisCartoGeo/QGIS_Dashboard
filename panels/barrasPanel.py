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
from .stylesBarPanel import styleBarPanel
from ..calculations.dataQuery import queriesData
import tempfile

class barrasPanel(QgsHtmlAnnotation):
    def __init__(self,layer,type,title,expression,position='top-left',anchoP=80,altoP=40.0,\
    colorBar="#4db0c3",wordBreak=True,colorTit='black',sizeTitle=12,colorLabels='black',sizeLabels=9,\
    orientation='v',typeColor='palette',palette='contrast'):
        super().__init__()
        self.posicion=position
        self.capa= layer
        self.titulo=title
        self.colorBar=colorBar
        
        self.wordBreak=wordBreak
        self.colorBar=colorBar
        self.colorTit=colorTit
        self.sizeTitle=sizeTitle
        self.colorLabels=colorLabels
        self.sizeLabels=sizeLabels
        self.orientation=orientation
        self.typeColor=typeColor
        self.palette=palette
        
        self.tipo= type
        self.expresion=expression
#        self.canvas = canvas
#        self.setMapLayer(self.capa)
        self.anchop=anchoP
        self.altop=altoP

        self.iniHtml=''
        
        self.tempf=None
        
        
        self.defaultValue=None
        self.firtsTime=True
        self._select=False
    
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
        if self.tipo=='atributo-sum':
            if self.capa.selectedFeatureCount()>0:
                select=True
            else:
                select=False
            estilo=styleBarPanel(self.data,title=self.titulo, estilo='sum_attrib',select=select,\
            wordBreak=self.wordBreak,colorBar=self.colorBar,colorTit=self.colorTit,\
            sizeTitle=self.sizeTitle,colorLabels=self.colorLabels,sizeLabels=self.sizeLabels,\
            orientation=self.orientation,typeColor=self.typeColor,palette=self.palette)
        elif self.tipo=='multiple_fields':
            estilo=styleBarPanel(self.data,title=self.titulo,estilo='multiple_fields',\
            wordBreak=self.wordBreak,colorBar=self.colorBar,colorTit=self.colorTit,\
            sizeTitle=self.sizeTitle,colorLabels=self.colorLabels,sizeLabels=self.sizeLabels,\
            orientation=self.orientation,typeColor=self.typeColor,palette=self.palette)
        estilo.assignStyle(estilo.style)
        return estilo
        
    def defData(self):
        if self.tipo=='atributo-sum':
            campox=self.expresion[0]
            campoy=self.expresion[1]
            if self.firtsTime==True:
                self.firtsTime=False
                if self.capa.selectedFeatureCount()==0:
                    lentidades=self.capa.getFeatures()
                    self.data= [queriesData.summarizeClasses(lentidades,campox,campoy)]
                    self.defaultValue=self.data
                    return self.defaultValue
                else:
                    l1=self.capa.getFeatures()
                    d1=queriesData.summarizeClasses(l1,campox,campoy)
                    self.defaultValue=[d1]
                    l2=self.capa.selectedFeatures()
                    dt=queriesData.summarizeClasses(l2,campox,campoy)
                    d2={i:d1[i] if i in dt else 0 for i in d1}
                    del(dt)
                    self.data=[d1,d2]
                    return self.data
            else:
                if self.capa.selectedFeatureCount()==0:
                    return self.defaultValue
                else:
                    d1=self.defaultValue[0]
                    l2=self.capa.selectedFeatures()
                    dt=queriesData.summarizeClasses(l2,campox,campoy)
                    d2={i:d1[i] if i in dt else 0 for i in d1}
                    del(dt)
                    self.data=[d1,d2]
                    return self.data
                
        elif self.tipo=='multiple_fields':
            campos=self.expresion[0]#Lista con nombre de campos numericos
            if self.firtsTime==True:
                self.firtsTime=False
                if self.capa.selectedFeatureCount()==0:
                    lentidades=self.capa.getFeatures()
                    self.data= [queriesData.summarizeFields(lentidades,campos)]
                    self.defaultValue=self.data
                    return self.defaultValue
                else:
                    self.defaultValue= [queriesData.summarizeFields(self.capa.getFeatures(),campos)]
                    lentidades=self.capa.selectedFeatures()
                    self.data= [queriesData.summarizeFields(lentidades,campos)]
                    return self.data
            else:
                if self.capa.selectedFeatureCount()==0:
                    return self.defaultValue
                else:
                    lentidades=self.capa.selectedFeatures()
                    self.data= [queriesData.summarizeFields(lentidades,campos)]
                    return self.data
                
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
    
    def colorTextTitle(self,color):
        self.style.colorTit(color)
        self.style.update()
        self.update()
    
    def colorTextLabels(self,color):
        self.style.colorLabels(color)
        self.style.update()
        self.update()
    
    def colorBar(self,color):
        self.style.colorBar(color)
        self.style.update()
        self.update()
    
    def borrarHtml(self):
        try:
            os.remove(self.tempf.name)
        except Exception as e:
            print(str(e))
