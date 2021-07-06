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
from ..myUtils.dashColors import dashColors

class styleBarPanel():
    typeStyles=('multiple_fields','sum_attrib')
    def __init__(self,data,estilo='sum_attrib',select=False,title='',colorBar="#4db0c3",\
    wordBreak=False,colorTit='black',sizeTitle=12,colorLabels='black',sizeLabels=9,orientation='v',\
    typeColor='palette',palette='contrast'):
        self.styles={'sum_attrib':self.sumAttrib,'multiple_fields':self.multipleFields}
        dir=os.path.dirname(__file__)
        self.dirJs=os.path.join(dir,'plotly-latest.min.js')
        self.title=title
        self.wordBreak=wordBreak
        self.colorBar=colorBar
        self.colorTit=colorTit
        self.sizeTitle=sizeTitle
        self.colorLabels=colorLabels
        self.sizeLabels=sizeLabels
        self.orientation=orientation
        self.typeColor=typeColor
        self.palette=palette
        
        self.data=data
        self.style=estilo
        #self.barpanel=panelo
        
        self._select=select
        self._database=None
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
        '<script src='+"'file:///"+self.dirJs+"'"+'></script>'+'\n'+\
        '<div  id='+'"myDiv"'+'>'+'\n'+\
        '<script>'+'\n'
    
    @classmethod
    def getTypeStyles(estilo):
        tipos=estilo.typeStyles
        return tipos
    
    def assignStyle(self,estilo):
        if estilo in self.styles:
            self.styles[estilo]()
    
    def evalColors(self):
        colors=[self.colorTit,self.colorBar,self.colorLabels]
        lc=map(lambda x:'rgb('+str(x.red())+','+str(x.green())+','+str(x.blue())+')'\
        if type(x)==QColor else x,colors)
        self.colorTit,self.colorBar,self.colorLabels=lc
    
    #sustituir este metodo por una clase estatica en utils
    def defPaletteColors(self,listLabels):
        buildColor=dashColors()
        colores=buildColor.getPalette(self.palette,len(listLabels))
        return colores
            
    def multipleFields(self):
        self.evalColors()
        self.html=self.html0
        data=self.data[0]
        if self.wordBreak==True:
            labels=utils.splitText(data.keys())
        else:
            labels=data.keys()

        #ESCRIBIR CAMPOX EN UN STRING LOS VALORES
        vx="[' "+"','".join(labels)+"']"
        #ESCRIBIR CAMPOY EN UN STRING LOS VALORES
        vy="["+','.join(str(n) for n in data.values())+']'
        self.defData([vx,vy])
        self.defTitle()
        self.close()
    
    def sumAttrib(self):
        self.evalColors()
        self.html=self.html0
        if self._select==False:
            data=self.data[0]
        else:
            data=self.data[0]
        if self.wordBreak==True:
            labels=utils.splitText(data.keys())
        else:
            labels=data
        vx="[' "+"','".join(labels)+"']"
        vy="["+','.join(str(n) for n in data.values())+']'
        self._dataBase=[(vx,vy)]

        if self._select==True:
            data2=self.data[1]
            vx2=vx
            vy2="["+','.join(str(n) for n in data2.values())+']'
            self._dataBase=[self._dataBase[0],(vx2,vy2)]
        self.defData(self._dataBase)
        self.modo()
        self.defTitle()
        self.close()
    
    def defData(self,data):
        if self.style=='multiple_fields':
            vx=data[0]
            vy=data[1]
            val=' xv= '+vx+';'+'\n'+\
                ' yv= '+vy+';'+'\n'+\
                'var data = [{'+'\n'+\
                '  x: xv,'+'\n'+\
                '  y: yv,'+'\n'+\
                '  type: "bar",'+'\n'
            if self.typeColor=='unicolor':
                val=val+'  marker: {color: '+"'"+self.colorBar+"'"+',line:{color:"black",width:1}},'+'\n'
            else:
                val=val+'  marker: {color:'+self.defPaletteColors(self.data[0].keys())+',line:{color:"black",width:1}},'+'\n'
            text='  text: yv.map(String),'+'\n'+\
                 '  textposition:'+" 'auto'"+'}];'+'\n'+\
                 'var layout = {'+'\n'
            self.html=self.html+val+text
        elif self.style=='sum_attrib':
            if len(data)==1:
                opacidad=1
            else:
                opacidad=0.6
            dat='var trace1 = {'+'\n'+\
                '  x:'+data[0][0]+','+'\n'+\
                '  y:'+data[0][1]+','+'\n'+\
                '  opacity:'+str(opacidad)+','+'\n'+\
                '  type: "bar",'+'\n'
            if self.typeColor=='unicolor':
                dat=dat+'  marker: {color: '+"'"+self.colorBar+"'"+',line:{color:"black",width:1}}};'+'\n'
            else:
                dat=dat+'  marker: {color:'+self.defPaletteColors(self.data[0].keys())+',line:{color:"black",width:1}}};'+'\n'

            self.html=self.html+dat
            if self._select==True or len(data)>1:
                dat2='var trace2 = {'+'\n'+\
                '  x:'+data[1][0]+','+'\n'+\
                '  y:'+data[1][1]+','+'\n'+\
                '  opacity: 1,'+'\n'+\
                '  type: "bar",'+'\n'+\
                'marker: {color: "yellow",line:{color:"red",width:2}},'+'\n'+\
                '};'+'\n'+\
                'var data = [trace1, trace2];'+'\n'
                self.html=self.html+dat2
            else:
                self.html=self.html+'var data = [trace1];'+'\n'
    
    def modo(self):
        if self._select==True:
            modo='var layout = {showlegend:false,'+'\n'+\
                   '  barmode: "overlay",'+'\n'
        else:
            modo='var layout = {'+'\n'
        self.html=self.html+modo
    
    def defTitle(self):
        if self.title== None or self.title=='':
            tit1='title: '+"'<b>"+'Grafico de Barras'+"</b>'"+', titlefont:{size:'+\
            str(self.sizeTitle)+',color:'+"'"+self.colorTit+"'"+'},'+'\n'
        else:
            tit1='title: '+"'<b>"+self.title+"</b>'"+', titlefont:{size:'+\
            str(self.sizeTitle)+',color:'+"'"+self.colorTit+"'"+'},'+'\n'
        tit2='font:{size:'+str(self.sizeLabels)+',color:'+"'"+self.colorLabels+"'"+'},'+'\n'+\
             'autosize: true,'+'\n'+\
             'orientation:'+"'"+self.orientation+"'"+','+'\n'+\
             'margin: { t: 30, b: 30, l: 30,r:10, autoexpand: false}};'+'\n'
        tit=tit1+tit2
        self.html=self.html+tit

    def close(self):
        cierre='var config = {responsive: true}'+'\n'+\
        "Plotly.newPlot('myDiv', data, layout, {displayModeBar: false}, config);"+'\n'+\
        'window.onresize = function() {'+'\n'+\
        "Plotly.relayout('myDiv', {"+'\n'+\
        "'xaxis.autorange': true,"+'\n'+\
        "'yaxis.autorange': true,"+'\n'+\
        "'margin': { t: 30, b: 30, l: 30, r:10, autoexpand: true}"+'\n'+\
        '});'+'\n'+\
        '};'+'\n'+\
        '</script>'+'\n'+\
        '</div>'+'\n'+\
        '</body>'+'\n'+\
        '</html>'
        self.html=self.html+cierre 
    
    def update(self):
        self.styles[self.style]()
    
    
    
    