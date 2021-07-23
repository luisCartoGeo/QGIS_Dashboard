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
from qgis import PyQt
from qgis.PyQt.QtGui import QColor
import os
from ..myUtils.myUtils import utils

class styleSeriePanel():
    typeStyles=('multiple_fields')
    def __init__(self,data,estilo='multiple_fields',title='',select=False,fill=False,\
    wordBreak=False,colorTit='black',sizeTitle=12,colorLabels='black',sizeLabels=9,widthline=1):
        self.styles={'multiple_fields':self.multipleFields}
        dir=os.path.dirname(__file__)
        self.dirJs=os.path.join(dir,'plotly-latest.min.js')
        self.title=title
        self.wordBreak=wordBreak
        self.colorTit=colorTit
        self.sizeTitle=sizeTitle
        self.colorLabels=colorLabels
        self.sizeLabels=sizeLabels
        self.widthline=widthline
        self.fill=fill
        self.select=select
 
        self.data=data
        self.style=estilo
        self.relleno='none'

        self.html=''
        self.html0='<html lang='+"es"+'>'+'\n'+\
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
        '<script src='+"'file:///"+ self.dirJs+"'"+'></script>'+'\n'+\
        '<div  id='+'"myDiv"'+'>'+'\n'+\
        '<script>'+'\n'
        self._database=None
    
    @classmethod
    def getTypeStyles(estilo):
        tipos=estilo.typeStyles
        return tipos
    
    def defFill(self):
        if self.fill==True:
            self.relleno='tonexty'
        else:
            self.relleno='none'
    
    def assignStyle(self,estilo):
        if estilo in self.styles:
            self.styles[estilo]()
    
    def evalColors(self):
        colors=[self.colorTit,self.colorLabels]
        lc=map(lambda x:'rgb('+str(x.red())+','+str(x.green())+','+str(x.blue())+')'\
        if type(x)==QColor else x,colors)
        self.colorTit,self.colorLabels=lc
    
    def multipleFields(self):
        self.evalColors()
        self.html=self.html0
        data=self.data#DEBE LLEGAR UN DICCIONARIO ORDENADO
        self.defFill()
        if self.select==False:               
            if self.wordBreak==True:
                labels=utils.splitText(data.keys())
            else:
                labels=data.keys()
            valores=list(self.data.values())
            val='['+','.join(str(i) for i in valores)+']'
            #ESCRIBIR CAMPOX EN UN STRING LOS VALORES
            xv="['"+"','".join(labels)+"']"
            #ESCRIBIR CAMPOY EN UN STRING LOS VALORES
            yv='['+','.join(str(i) for i in valores)+']'
            self.defData([xv,yv])
        elif self.select==True:
            data=self.data
            labels=data[0][1].keys()
            self._database=[]
            if self.wordBreak==True:
                labels=utils.splitText(labels)
            for i in data:
                categoria=i[0]
                y=i[1]
                xv="['"+"','".join(labels)+"']"
                yv="["+','.join(str(n) for n in y.values())+']'
                self._database.append([categoria,(xv,yv)])
            self.defData(self._database)
        self.defTitle()
        self.close()
          
    def defData(self,data):
        if self.select==False:
           xv=data[0]
           yv=data[1]
           size=self.widthline+5
           text1='var yv='+yv+';'+'\n'+\
            'var trace={'+'\n'+\
            '  x:'+xv+','+'\n'+\
            '  y: yv,'+'\n'+\
            '  type:'+"'scatter',"+'\n'+\
            '  mode:'+"'lines+markers+text',"+'\n'+\
            '  fill:'+"'"+self.relleno+"',"+'\n'+\
            '  text: yv.map(String),'+'\n'+\
            "  textposition:'top',"+'\n'+\
            '  line:{width:'+str(self.widthline)+'},'+'\n'+\
            '  marker:{size:'+str(size)+'},'+'\n'+\
            '};'+'\n'+\
            'var data=[trace];'+'\n'
           self.html=self.html+text1
        elif self.select==True:
            for e,i in enumerate(data):
                categoria=i[0]
                categoria=utils.splitSentence(categoria,20)
                x=i[1][0]
                y=i[1][1]
                text1='y'+str(e)+"="+y+';'+'\n'+\
                'var trace'+str(e)+'={'+'\n'+\
                '  x:'+x+','+'\n'+\
                '  y: y'+str(e)+',\n'+\
                '  type:'+"'scatter',"+'\n'+\
                '  mode:'+"'lines+markers+text',"+'\n'+\
                '  fill:'+"'"+self.relleno+"',"+'\n'+\
                '  text: y'+str(e)+'.map(String),'+'\n'+\
                '  textposition:'+"'top right',"+'\n'+\
                '  line:{width:'+str(self.widthline)+'},'+'\n'+\
                '  marker:{size:'+str(self.widthline+5)+'},'+'\n'+\
                '  name:'"'"+categoria+"'"+','+'\n'+\
                '};'+'\n'
                self.html=self.html+text1
                
            closeDat='var data=['+','.join('trace'+str(i) for i in range(len(data)))+'];\n'
            self.html=self.html+closeDat
        
        if type(self.data)==dict:
            n=len(self.data)+0.5
        else:
            n=len(self.data[0][1])+0.5
        axe='var layout = {'+'\n'+\
            '   xaxis:{range:[0,'+str(n)+']},'+'\n'
        self.html=self.html+axe
    
    def defTitle(self):
        if self.title== None or self.title=='':
            tit1='   title: '+"'<b>"+'Grafico de Lineas/areas'+"</b>'"+', titlefont:{size:'+\
            str(self.sizeTitle)+',color:'+"'"+self.colorTit+"'"+'},'+'\n'
        else:
            tit1='   title: '+"'<b>"+self.title+"</b>'"+', titlefont:{size:'+\
            str(self.sizeTitle)+',color:'+"'"+self.colorTit+"'"+'},'+'\n'
        tit2='   font:{size:'+str(self.sizeLabels)+',color:'+"'"+self.colorLabels+"'"+'},'+'\n'+\
             "   legend: {y:1.2,font: {size: 8.5},yref:'paper'},"+'\n'+\
             '   autosize: true,'+'\n'+\
             '   margin: { t: 30, b: 30, l: 30,r:20, autoexpand: true}};'+'\n'
        tit=tit1+tit2
        self.html=self.html+tit
    
    def close(self):
        cierre='var config = {responsive: true}'+'\n'+\
        "Plotly.newPlot('myDiv', data, layout, {displayModeBar: false}, config);"+'\n'+\
        'window.onresize = function() {'+'\n'+\
        "Plotly.relayout('myDiv', {"+'\n'+\
        "'xaxis.autorange': false,"+'\n'+\
        "'yaxis.autorange': true,"+'\n'+\
        "'margin': { t: 30, b: 30, l: 30, r:20, autoexpand: true}"+'\n'+\
        '});'+'\n'+\
        '};'+'\n'+\
        '</script>'+'\n'+\
        '</div>'+'\n'+\
        '</body>'+'\n'+\
        '</html>'
        self.html=self.html+cierre 
    
    def update(self):
        self.styles[self.style]()       
        
    
    
    
    
    
    
    