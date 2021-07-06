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

class styleIndicadorPanel():
    typeStyles=('Angular','Bullet','Card')
    def __init__(self,data,threshold,range,estilo='Angular',title='',colorTit='black',sizeTitle=10,\
    colorBar="blue",colorBackground='white',colorBase='lightgray',colorLine='red',colorValue='black',\
    sizeLabel=10,colorFinal='#B31101',colorMark='red',relative='false'):
        self.styles={'Angular':self.angular,'Bullet':self.bullet,'Card':self.card}
#        dir=os.path.dirname(__file__)
#        self.dirJs=os.path.join(dir,'plotly-latest.min.js')
        self.dir='C:\dashboard\plugin\qgis_dashboard\panels\plotly-latest.min.js'
        self.title=title
        self.colorTit=colorTit
        self.sizeTitle=sizeTitle
        self.sizeLabel=sizeLabel
        self.colorBar=colorBar
        self.colorBackground=colorBackground
        self.colorBase=colorBase
        self.colorLine=colorLine
        self.colorFinal=colorFinal
        self.colorMark=colorMark
        self.colorValue=colorValue
        self.style=estilo
        print(self.style)
        self.relative=relative
        self.range=range
        self.vmax=range[1]
        self.vmin=range[0]
        self.threshold=threshold
        
        self.shape='"angular"'
        self.data=data
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
        '<script src='+"'file:///"+ self.dir+"'"+'></script>'+'\n'+\
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
        colors=[self.colorTit,self.colorBar,self.colorBackground,self.colorBase,\
        self.colorLine,self.colorFinal,self.colorMark,self.colorValue]
        lc=map(lambda x:'rgb('+str(x.red())+','+str(x.green())+','+str(x.blue())+')'\
        if type(x)==QColor else x,colors)
        self.colorTit,self.colorBar,self.colorBackground,self.colorBase,\
        self.colorLine,self.colorFinal,self.colorMark,self.colorValue=lc
    
    def angular(self):
        self.evalColors()
        self.html=self.html0
        if self.title== None or self.title=='':
            self.title='Indicator chart'
#        medio=(max(self.range)-min(self.range))/2
                
        data=self.data#DEBE LLEGAR UN VALOR
        ht='var data = [{'+'\n'+\
        '   type: "indicator",'+'\n'+\
        '   mode: "gauge+number+delta",'+'\n'+\
        '   domain: { x: [0, 1], y: [0, 1] },'+'\n'+\
        '   title: { text:'+'\n'+\
        '   "<b><span style='+"'font-size:"+str(self.sizeTitle)+\
        "vh;color:"+self.colorTit+"'"+'>'+self.title+'</span></b>"'+'\n'+\
        '   },'+'\n'+\
        '   gauge: { axis: { range: ['+str(self.vmin)+','+str(self.vmax)+'] },'+'\n'+\
        '   bar: {color:"'+self.colorBar+'"},'+'\n'+\
        '   shape: '+self.shape+','+'\n'+\
        '   steps: ['+'\n'+\
        '   {range:['+str(self.vmin)+','+str(self.vmax)+'], color:"'+self.colorBase+'"},'+'\n'+\
        '   {range:['+str(self.threshold)+','+str(self.vmax)+'], color:"'+self.colorFinal+'"}],'+'\n'+\
        '   threshold: {'+'\n'+\
        '   line:{color:"'+self.colorLine+'", width:4},'+'\n'+\
        '   thickness: 0.75,'+'\n'+\
        '   value:'+str(self.threshold)+'}},'+'\n'+\
        '   delta: { reference:'+str(self.threshold)+','+\
        'relative:'+self.relative+',increasing:{ color:"'+self.colorLine+'"}},'+'\n'+\
        '   value:'+self.data+' }];'+'\n'+\
        'var layout = {'+'\n'+\
        '    paper_bgcolor:"'+self.colorBackground+'",'+'\n'+\
        '    autosize: true,'+'\n'+\
        "    font: {family: 'Arial',"+'\n'+\
        '    size:'+str(self.sizeLabel)+",color:"+"'"+self.colorValue+"'"+"},"+'\n'
        self.html=self.html+ht
        self.close()
        
    def bullet(self):
        self.shape='"bullet"'
        self.angular()
    
    def card(self):
        self.evalColors()
        self.html=self.html0
        if self.title== None or self.title=='':
            self.title='Indicator chart'
        data=self.data#DEBE LLEGAR UN VALOR
        ht='var data = [{'+'\n'+\
           '   type: "indicator",'+'\n'+\
           '   mode: "number+delta",'+'\n'+\
           '   domain:{x:[0, 1],y:[0,1]},'+'\n'+\
           '   title: { text:'+'\n'+\
           '   "<b><span style='+"'font-size:"+str(self.sizeTitle)+\
           "vh;color:"+self.colorTit+"'"+'>'+self.title+'</span></b>"'+'\n'+\
           '   },'+'\n'+\
           '   delta: { reference:'+str(self.threshold)+','+\
           'relative:'+self.relative+',increasing:{ color:"'+self.colorLine+'"}},'+'\n'+\
           '   value:'+self.data+' }];'+'\n'+\
           'var layout = {'+'\n'+\
           '    paper_bgcolor:"'+self.colorBackground+'",'+'\n'+\
           '    autosize: true,'+'\n'+\
           "    font: {family: 'Arial',"+'\n'+\
           '    size:'+str(self.sizeLabel)+",color:"+"'"+self.colorValue+"'"+"},"+'\n'
        self.html=self.html+ht
        self.close()

    def close(self):
        print('en close',self.style)
        if self.style=='Angular':
            ht='   margin: {t:20,b:0,l:25,r:30},'+'\n'
        elif self.style=='Bullet':
            ht='   margin: {t:20,b:40,r:5},'+'\n'
        elif self.style=='Card':
            ht='   margin: {t:20,b:0,l:20,r:20},'+'\n'
        h2='autoexpand:true};'+'\n'+\
           "Plotly.newPlot('myDiv',data,layout,{displayModeBar: false});"+'\n'+\
           'window.onresize = function() {'+'\n'+\
           "Plotly.relayout('myDiv', {"+'\n'+\
           "'layout.autosize': true,"+'\n'
        self.html=self.html+ht+h2+ht
        close='});'+'\n'+\
              '};'+'\n'+\
              '</script>'+'\n'+\
              '</div>'+'\n'+\
              '</body>'+'\n'+\
              '</html>'+'\n'
        self.html=self.html+close
    
    def update(self):
        self.styles[self.style]()
        
    