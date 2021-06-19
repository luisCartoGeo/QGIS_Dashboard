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
from ..calculations.dataQuery import queriesData
from ..calculations.spatialQuery import spatialQueries
from qgis.core import QgsProject, QgsVectorLayer, QgsFeature

class operations():
    operations_polygon=['Sum of an attribute','Percentage','Statistics. Selected entities',\
    'Statistics. Selection that coincides with','Total selected entities','Entities contained in selection',\
    'Entities contained. count by attribute that coincides with','Number of entities in the area. Density',\
    'Sum of attribute between area. Density']
    
    operations_nospatial=['Sum of an attribute','Percentage','Statistics. Selected entities',\
    'Statistics. Selection that coincides with','Total selected entities']
    
    operations_nopolygon=['Sum of an attribute','Percentage','Statistics. Selected entities',\
    'Statistics. Selection that coincides with','Total selected entities','Entities contained at a distance. Buffer',\
    'Entities contained at a distance that coincides with','Sum of attributes of entities contained at a distance']
    
    def __init__(self,panel,operation,modeE='processing'):
        self.listOperations={'atributo':self.attribute,'Porcentaje':self.percentage,\
    'math-atributo':self.statisticsAttrib,'entid_seleccionadas':self.selection,\
    'entid-selec-intersect':self.countContains,\
    'entid-selec-intersect-atrib':self.countsAttribContains,\
    'buffer-contains':self.countContainsBuffer,\
    'buffer-contains-attrib':self.countAttribBuffer,\
    'buffer-contains-sum':self.sumAttribBuffer,\
    'densidad':self.density,\
    'densidad valor':self.densityValue}
        self.spatialOperation=modeE
        self.panel=panel
        self.capa=panel.capa
        self.expression=self.panel.expresion
    
    @classmethod
    def getOperation(operation,type='polygon'):
        if type=='polygon':
            listOperat=operation.operations_polygon
            return listOperat
        elif type=='line or point':
            listOperat=operation.operations_nopolygon
            return listOperat
        elif type=='no spatial':
            listOperat=operation.operations_nospatial
            return listOperat
    
    def attribute(self):
        campo=self.expression[0]
        if self.capa.selectedFeatureCount()==0:
            calculo=sum([f[campo] for f in self.capa.getFeatures() if type(f[campo])==int or type(f[campo])==float ])
            val='<p class='+'"valor"><strong>'+str(round(calculo,2))+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()==1:
            entidad=list(self.capa.getSelectedFeatures())[0]
            if type(entidad[campo])==int or type(entidad[campo])==float:
                calculo=entidad[campo]
            else:
                calculo=0
            val='<p class='+'"valor"><strong>'+str(round(calculo,2))+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>1:
            calculo=sum([f[campo] for f in self.capa.getSelectedFeatures() if type(f[campo])==int or type(f[campo])==float])
            val='<p class='+'"valor"><strong>'+str(round(calculo,2))+'</strong></p>'+'\n'
        return val
    
    def percentage(self):
        campo=self.expression[0]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'100 %'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            vp=queriesData.porcentaje(self.capa.getSelectedFeatures(),campo,self.capa)
            val='<p class='+'"valor"><strong>'+vp+' %'+'</strong></p>'+'\n'
        return val
    
    def selection(self):
        calculo=self.capa.selectedFeatureCount()
        val='<p class='+'"valor"><strong>'+str(calculo)+'</strong></p>'+'\n'
        return val
    
    def statisticsAttrib(self):
        if len(self.expression)==2:
            campo=self.expression[0]
            operador=self.expression[1]
            val='<p class='+'"valor"><strong>[% aggregate('+"'"+self.capa.name()+"', '"+operador+"',"+'"'+campo+\
            '",filter:=is_selected('+"'"+self.capa.name()+"'"+', $currentfeature)) %]</strong></p>'+'\n'
        elif len(self.expression)==4:
            campo=self.expression[0]
            operador=self.expression[1]
            atrib=self.expression[2]
            valor_atrib=self.expression[3]
            val='<p class='+'"valor"><strong>[% aggregate('+"'"+self.capa.name()+"', '"+operador+"',"+'"'+campo+\
            '",filter:=is_selected('+"'"+self.capa.name()+"'"+', $currentfeature) and '+\
            '"'+atrib+'"= '+"'"+valor_atrib+"'"+') %]</strong></p>'+'\n'
        return val
    
    #SPATIAL OPERATIONS*********************************************************
    def countContains(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expression[0])[0]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.containsCountProcess(self.capa,capa2)
                val='<p class='+'"valor"><strong>'+str(calculo)+'</strong></p>'+'\n'
        return val
    
    def countsAttribContains(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expression[0])[0]
        campo=self.expression[1]
        atributo=self.expression[2]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.containsCountAttribProcess(self.capa,capa2,campo,atributo)
                val='<p class='+'"valor"><strong>'+str(round(calculo,3))+'</strong></p>'+'\n'
        return val
    
    def density(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expresion[0])[0]
        unidad=self.expression[1]
        #Definimos la unidad de medida
        divisor=1
        if unidad=='hectareas':
            divisor=10000
        elif unidad=='km2':
            divisor=1000000
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.densityProcess(self.capa,capa2,divisor)
                val='<p class='+'"valor"><strong>'+str(round(calculo,4))+'</strong></p>'+'\n'
        return val
    
    def densityValue(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expression[0])[0]
        unidad=self.expression[1]
        campo=self.expression[2]
        #Definimos la unidad de medida
        divisor=1
        if unidad=='hectareas':
            divisor=10000
        elif unidad=='km2':
            divisor=1000000
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.densityAttribProcess(capa,capa2,campo,divisor)
                val='<p class='+'"valor"><strong>'+str(round(calculo,4))+'</strong></p>'+'\n'
        return val
    
    def countContainsBuffer(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expression[0])[0]
        distancia=self.expression[1]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.bufferCountProcess(capa,capa2,distance)
                val='<p class='+'"valor"><strong>'+str(calculo)+'</strong></p>'+'\n'
        return val
    
    def countAttribBuffer(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expresion[0])[0]
        distancia=self.expression[1]
        campo=self.expression[2]
        atributo=self.expression[3]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.bufferAttribProcess(self.capa,capa2,distancia,campo,atributo,tipo='conteo')
                val='<p class='+'"valor"><strong>'+str(calculo)+'</strong></p>'+'\n'
        return val
        
    def sumAttribBuffer(self):
        pry=QgsProject.instance()
        capa2=pry.mapLayersByName(self.expresion[0])[0]
        distancia=self.expression[1]
        campo=self.expression[2]
        atributo=self.expression[3]
        if self.capa.selectedFeatureCount()==0:
            val='<p class='+'"valor"><strong>'+'0'+'</strong></p>'+'\n'
        elif self.capa.selectedFeatureCount()>0:
            if self.spatialOperation=='processing':
                calculo=spatialQueries.bufferAttribProcess(self.capa,capa2,distancia,campo,atributo,tipo='sum')
                val='<p class='+'"valor"><strong>'+str(calculo)+'</strong></p>'+'\n'
        return val
            
    