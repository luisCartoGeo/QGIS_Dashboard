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
import tempfile

class indicadorPanel(QgsHtmlAnnotation):
    def __init__(self,canvas,layer,type,title,expression,puntoCritico,intervalo,position='top-left',anchoP=170,altoP=140,\
    fondTit='black',colorTextTit='white',fondVal='lightblue', colorTextVal='black'):
        super().__init__()
        dir=os.path.dirname(__file__)
        self.dirJs=os.path.join(dir,'plotly-latest.min.js')
        self.posicion=position
        self.capa= layer
        self.titulo=title
        self.umbral=puntoCritico
        self.rango=intervalo
        #CAPA PARA ANALISIS DE CONSULTAS INTERSECCIONES
        self.capa2=None 
        #---------------------------------------------
        #INDICE ESPACIAL
        self.indiceE=None
        #---------------------------------------------
        self.colorTitulo=fondTit
        self.colFontTitulo=colorTextTit
        self.colorValor=fondVal
        self.colFontValor=colorTextVal
        self.tipo= type
        self.expresion=expression
        self.canvas = canvas
        self.setMapLayer(self.capa)
        self.anchop=anchoP
        self.altop=altoP
        #guardamos aqui el ancho y alto luego de considerar 
        #los espacios por los estilos html 
        self.anchoF=anchoP+20
        self.altoF=altoP
        self.iniHtml=''
        self.ahtml=None
        
        self.tempf=None
    
        self.setFrameSize(QSizeF(self.anchop,self.altoF))
        self.setFrameOffsetFromReferencePoint(QPointF(0, 0))
        self.conectar()
        self.iniciarHtml()
        self.defTitulo()
        self.defRango()        
        self.defUmbral()
        self.defValor()
        self.cierreHtml()
        
    def iniciarHtml(self):
        self.iniHtml='<html lang='+"es"+'>'+'\n'+\
        '<!DOCTYPE html>'+'\n'+\
        '<html lang="es">'+'\n'+\
        '<head>'+'\n'+\
        '<style>'+'\n'+\
        '#myDiv {'+'\n'+\
        'height:100%;'+'\n'+\
        'width:100%;'+'\n'+\
        '}'+'\n'+\
        '</style>'+'\n'+\
        '</head>'+'\n'+\
        '<body>'+'\n'+\
        '<script src='+"'file:///"+self.dirJs+"'"+'></script>'+'\n'+\
        '<div  id='+'"myDiv"'+'>'+'\n'+\
        '<script>'+'\n'+\
        'var data = [{'+'\n'+\
            'type: "indicator",'+'\n'+\
            'mode: "gauge+number+delta",'+'\n'+\
            'domain: { x: [0, 1], y: [0, 1] },'+'\n'
    
    def asignarIndEspacial(self, indexS):
        print('asignando indice espacial')
        self.indiceE=indexS
        
    def conectar(self):
        print('actualizar')
        self.capa.selectionChanged.connect(self.update)
    
    def desconectar(self):
        self.capa.selectionChanged.disconnect(self.conectar)
    
    def defRango(self):
        if type(self.rango)==float or type(self.rango)==int:
            ran='gauge: { axis: { range: [0,'+str(self.rango)+'] },'+'\n'+\
            'threshold: {'+'\n'+\
            'steps: ['+'\n'+\
            '{ range: [0,'+str(self.rango/2)+' ], color: '+'"lightgray" },'+'\n'+\
            '{ range: ['+str(self.rango/2)+','+str(self.rango)+'], color:'+'"gray" }],'+'\n'
        else:
            ran='gauge: { axis: { range: ['+str(self.rango[0])+','+str(self.rango[1])+'] },'+'\n'+\
            'steps: ['+'\n'+\
            '{ range: ['+str(self.rango[0])+','+str(self.rango[1]/2)+' ], color: '+'"lightgray" },'+'\n'+\
            '{ range: ['+str(self.rango[1]/2)+','+str(self.rango[1])+'], color:'+'"gray" }],'+'\n'
        detalles= 'threshold: {'+'\n'+\
            'line: { color: "red", width: 4 },'+'\n'+\
            'thickness: 0.75,'+'\n'
        self.iniHtml=self.iniHtml+ran+detalles
    
    def defTitulo(self):
        if self.titulo== None or self.titulo=='':
            tit='title: { text: '+"'<b>"+self.capa.name()+"</b>'"+', font: {size: 14}},'+'\n'
            self.iniHtml=self.iniHtml+tit
        else:
            tit='title: { text: '+"'<b>"+self.titulo+"</b>'"+', font: {size: 14}},'+'\n'
            self.iniHtml=self.iniHtml+tit
    
    def defUmbral(self):
        umbral='value: '+str(self.umbral)+'}},'+'\n'+\
               'delta: { reference: '+str(self.umbral)+' },'+'\n'
        self.iniHtml=self.iniHtml+umbral
    
    def defValor(self):
        if self.tipo=='atributo':
            campo=self.expresion[0]
            if self.capa.selectedFeatureCount()==0:
                calculo=0
                val='value: '+str(calculo)+', }];'+'\n'
            elif self.capa.selectedFeatureCount()==1:
                entidad=list(self.capa.getSelectedFeatures())[0]
                if type(entidad[campo])==int or type(entidad[campo])==float:
                    calculo=entidad[campo]
                else:
                    calculo=0
                val='value: '+str(round(calculo,2))+', }];'+'\n'
            elif self.capa.selectedFeatureCount()>1:
                calculo0=sum([f[campo] for f in self.capa.getSelectedFeatures() if type(f[campo])==int or type(f[campo])==float])
                calculo=calculo0/self.capa.selectedFeatureCount()
                val='value: '+str(round(calculo,2))+', }];'+'\n'
            self.iniHtml=self.iniHtml+val
        elif self.tipo=='entid-selec-intersect':
            pry=QgsProject.instance()
            self.capa2=pry.mapLayersByName(self.expresion[0])[0]
#            print(self.capa2.name())
            campop=self.capa2.fields().field(0).name()
            if self.capa.selectedFeatureCount()==0:
                calculo=0
                val='value: '+str(calculo)+', }];'+'\n'
            if self.capa.selectedFeatureCount()>0:
                #secuencial con bbx
                if self.capa2.featureCount()<1000 or self.indiceE==None:
                    calculo=0
                    for i in self.capa.getSelectedFeatures():
                        for j in self.capa2.getFeatures():
                            if i.geometry().boundingBoxIntersects(j.geometry()):
                                if i.geometry().contains(j.geometry()):
                                    calculo=calculo+1
                    val='value: '+str(calculo)+', }];'+'\n'
                #con indice espacial
                else:
                    print('entro a indice espacial')
                    print(self.indiceE)
                    calculo=0
                    lisIds=[]
                    for i in self.capa.getSelectedFeatures():
                       bbx= i.geometry().boundingBox()
                       listIds=self.indiceE.intersects(bbx)
                       for j in listIds:
                            if i.geometry().contains(self.capa2.getFeature(j).geometry()):
                                calculo=calculo+1
                    val='value: '+str(calculo)+', }];'+'\n'
            self.iniHtml=self.iniHtml+val
        elif self.tipo=='entid-selec-intersect-atrib':
            pry=QgsProject.instance()
            self.capa2=pry.mapLayersByName(self.expresion[0])[0]
            campop=self.expresion[1]
            atributo=self.expresion[2]
            if atributo.isnumeric:
                atributo=int(atributo)
            elif '.' in atributo:
                try:
                    atributo=float(atributo)
                except:
                    pass
#            print(atributo,type(atributo))
            if self.capa.selectedFeatureCount()==0:
                calculo=0
                val='value: '+str(calculo)+', }];'+'\n'
            if self.capa.selectedFeatureCount()>0:
                #secuencial con bbx
                secuencial=True
                print(self.capa2.name(),self.capa2.geometryType()==QgsWkbTypes.PointGeometry)
                if self.capa2.geometryType()==QgsWkbTypes.PointGeometry:
                    secuencial=True
                elif self.capa2.featureCount()>1000 and self.indiceE==None:
                    print('segunda condicional')
                    secuencial=True
                elif self.capa2.featureCount()>1000 and self.indiceE!=None:
                    secuencial=False
                    
                if secuencial==True:
                    print('secuencial')
                    calculo=0
                    for i in self.capa.getSelectedFeatures():
                        for j in self.capa2.getFeatures():
                            if i.geometry().boundingBoxIntersects(j.geometry()):
                                if i.geometry().contains(j.geometry()):
                                    if type(j[campop])==int or type(j[campop])==float or\
                                    type(j[campop])==str:
                                        if j[campop]==atributo:
                                            calculo=calculo+1
                    val='value: '+str(calculo)+', }];'+'\n'
                #con indice espacial
                elif secuencial==False:
                    print('entro a indice espacial')
                    print('indice espacial ',self.indiceE)
                    calculo=0
                    lisIds=[]
                    for i in self.capa.getSelectedFeatures():
                       bbx= i.geometry().boundingBox()
                       engine = QgsGeometry.createGeometryEngine(i.geometry().constGet())
                       engine.prepareGeometry()
#                       print(bbx)
                       listIds=self.indiceE.intersects(bbx)
                       req = QgsFeatureRequest().setFilterFids(listIds)
                       print(len(listIds))
                       for j in self.capa2.getFeatures(req):
                           if engine.contains(j.geometry().constGet()):
                               entidad=j
                               if type(entidad[campop])==int or type(entidad[campop])==float\
                               or type(entidad[campop])==str:
#                                  print(entidad[campop],type(entidad[campop]),atributo,type(atributo))
                                   if entidad[campop]==atributo:
                                       calculo=calculo+1
                    val='value: '+str(calculo)+', }];'+'\n'
            self.iniHtml=self.iniHtml+val
        elif self.tipo=='densidad':
            pry=QgsProject.instance()
            self.capa2=pry.mapLayersByName(self.expresion[0])[0]
            unidad=self.expresion[1]
            #Definimos la unidad de medida
            divisor=1
            if unidad=='hectareas':
                divisor=10000
            elif unidad=='km2':
                divisor=1000000
            
            if self.capa.selectedFeatureCount()==0:
                calculo=0
                val='value: '+str(calculo)+', }];'+'\n'
            if self.capa.selectedFeatureCount()>0:
                print('seleccion mayor de 0')
                #secuencial con bbx
                if self.capa2.featureCount()<1000 or self.indiceE==None:
                    calculo=0
                    area=0
                    for i in self.capa.getSelectedFeatures():
                        area=area+i.geometry().area()
                        print('area radio ',area)
                        for j in self.capa2.getFeatures():
                            if i.geometry().boundingBoxIntersects(j.geometry()):
                                if i.geometry().contains(j.geometry()):
                                    calculo=calculo+1
                    area=area/divisor
                    val='value: '+str(round(calculo/area,3))+', }];'+'\n'
                #con indice espacial
                else:
                    area=0
                    calculo=0
                    lisIds=[]
                    for i in self.capa.getSelectedFeatures():
                       engine = QgsGeometry.createGeometryEngine(i.geometry().constGet())
                       engine.prepareGeometry()
                       area=area+i.geometry().area()
                       bbx= i.geometry().boundingBox()
                       listIds=self.indiceE.intersects(bbx)
                       req = QgsFeatureRequest().setFilterFids(listIds)
                       for j in self.capa2.getFeatures(req):
                           if engine.contains(j.geometry().constGet()):
                                calculo=calculo+1
                    area=area/divisor
                    val='value: '+str(round(calculo/area,3))+', }];'+'\n'
            self.iniHtml=self.iniHtml+val
        
        elif self.tipo=='densidad valor':
            pry=QgsProject.instance()
            self.capa2=pry.mapLayersByName(self.expresion[0])[0]
            unidad=self.expresion[1]
            campov=self.expresion[2]
            #Definimos la unidad de medida
            divisor=1
            if unidad=='hectareas':
                divisor=10000
            elif unidad=='km2':
                divisor=1000000
            
            if self.capa.selectedFeatureCount()==0:
                calculo=0
                val='value: '+str(calculo)+', }];'+'\n'
            if self.capa.selectedFeatureCount()>0:
                print('seleccion mayor de 0')
                #secuencial con bbx
                if self.capa2.featureCount()<1000 or self.indiceE==None:
                    calculo=0
                    area=0
                    for i in self.capa.getSelectedFeatures():
                        area=area+i.geometry().area()
                        print('area radio ',area)
                        for j in self.capa2.getFeatures():
                            if i.geometry().boundingBoxIntersects(j.geometry()):
                                if i.geometry().contains(j.geometry()):
                                    calculo=calculo+j[campov]
                    area=area/divisor
                    val='value: '+str(round(calculo/area,3))+', }];'+'\n'
                #con indice espacial
                else:
                    area=0
                    calculo=0
                    lisIds=[]
                    for i in self.capa.getSelectedFeatures():
                       engine = QgsGeometry.createGeometryEngine(i.geometry().constGet())
                       engine.prepareGeometry()
                       area=area+i.geometry().area()
                       bbx= i.geometry().boundingBox()
                       listIds=self.indiceE.intersects(bbx)
                       req = QgsFeatureRequest().setFilterFids(listIds)
                       for j in self.capa2.getFeatures(req):
                           if engine.contains(j.geometry().constGet()):
                                calculo=calculo+j[campov]
                    area=area/divisor
                    val='value: '+str(round(calculo/area,3))+', }];'+'\n'
            self.iniHtml=self.iniHtml+val
        
    def cierreHtml(self):
        texto="0"
        cierre= 'var layout = { '+'\n'+\
               'autosize: true,'+'\n'+\
               'font: {family: '+"'Arial',"+'\n'+\
               'size: 11, color:'+"'black'},"+'\n'+\
               'margin: { t: 20, b: 0, l: 25,r:30, autoexpand: true}'+'\n'+\
               ' };'+'\n'+\
        'Plotly.newPlot('+"'myDiv'"+', data, layout, {displayModeBar: false});'+'\n'+\
        'window.onresize = function() {'+'\n'+\
            "Plotly.relayout('myDiv', {"+'\n'+\
              "'layout.autosize': true,"+'\n'+\
              "'margin': { t: 20, b: 0, l: 30, r:30, autoexpand: true}"+'\n'+\
            '});'+'\n'+\
        '};'+'\n'+\
        '</script>'+'\n'+\
        '</div>'+'\n'+\
        '</body>'+'\n'+\
        '</html>'
        self.iniHtml=self.iniHtml+cierre
        self.tempf=tempfile.NamedTemporaryFile(mode='w+t',prefix='qd',suffix='.html',delete=False)
        print(self.tempf.name)
        self.tempf.seek(0)
        self.tempf.write(self.iniHtml)
        self.tempf.close()
        if os.path.exists(self.tempf.name):
            self.setSourceFile(self.tempf.name)
        else:
            print('el archivo temporal no existe')
        
#        rutai="E:/indicador0.html"
#        ruta="E:/indicador"
#        if os.path.exists(rutai):
#            random.seed()
#            v=random.randint(0,10000)
#            v1=random.randint(0,10000)
#            texto=str(v)+str(v1)
#        self.ahtml=open(ruta+texto+".html","wt")
#        self.ahtml.write(self.iniHtml)
#        self.ahtml.close()
#        self.setSourceFile(self.ahtml.name)
    
    def update(self):
        print('actualizando')
        self.iniciarHtml()
        self.defTitulo()
        self.defRango()        
        self.defUmbral()
        self.defValor()
        cierre= 'var layout = { '+'\n'+\
               'autosize: true,'+'\n'+\
               'font: {family: '+"'Arial',"+'\n'+\
               'size: 10, color:'+"'black'},"+'\n'+\
               'margin: { t: 20, b: 0, l: 30, r:30, autoexpand: true},'+'\n'+\
               ' };'+'\n'+\
        'Plotly.newPlot('+"'myDiv'"+', data, layout, {displayModeBar: false});'+'\n'+\
        'window.onresize = function() {'+'\n'+\
            "Plotly.relayout('myDiv', {"+'\n'+\
              "'layout.autosize': true,"+'\n'+\
              "'margin': { t: 20, b: 0, l: 30, r:30, autoexpand: true}"+'\n'+\
            '});'+'\n'+\
        '};'+'\n'+\
        '</script>'+'\n'+\
        '</div>'+'\n'+\
        '</body>'+'\n'+\
        '</html>'
        self.iniHtml=self.iniHtml+cierre
        if os.path.exists(self.tempf.name):
            if os.access(self.tempf.name,os.W_OK):
                with open(self.tempf.name,'w+t') as file:
                    file.write(self.iniHtml)
            else:
                print('no hay acceso de escritura')
        else:
            print('el archivo no existe')
        self.setSourceFile(self.tempf.name)
#        self.ahtml=open(self.ahtml.name,"wt")
#        self.ahtml.write(self.iniHtml)
#        self.ahtml.close()
#        self.setSourceFile(self.ahtml.name)
    
    def borrarHtml(self):
        try:
            os.remove(self.tempf.name)
#            os.remove(self.ahtml.name)
        except:
            pass
#    "rgba(255, 0, 0, 0.0)"
#    def colorTextoTitulo(self,color):
#        if type(color)==QColor:
#            c='"rgb('+str(color.red())+','+str(color.green())+','+str(color.blue())+')"'
#            self.colFontTitulo=c
#        elif type(color)==str:
#            self.colFontTitulo=color
#        self.iniciarHtml()
#        self.defTitulo()
#        self.defValor()
#        self.cierreHtml()
#
##    self.colorTitulo=fondTit
##        self.colFontTitulo=colorTextTit
##        self.colorValor=fondVal
##        self.colFontValor=colorTextVal
#    def colorFondoTitulo(self,color):
#        if type(color)==QColor:
#            c='"rgb('+str(color.red())+','+str(color.green())+','+str(color.blue())+')"'
#            self.colorTitulo=c
#        elif type(color)==str:
#            self.colorTitulo=color
#        self.iniciarHtml()
#        self.defTitulo()
#        self.defValor()
#        self.cierreHtml()
#        
#    def colorTextoValor(self,color):
#        pass
#            
#    def colorFondoValor(self,color):
#        pass
#
#