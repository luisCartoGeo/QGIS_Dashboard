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
from qgis.core import QgsProject, QgsProcessingFeatureSourceDefinition,\
               QgsCoordinateTransform, QgsGeometry, QgsSpatialIndex,QgsFeatureRequest,\
               QgsGeometryEngine,QgsProcessingFeedback
import processing
#import ..decorator
#from ..decorator.medirTiempo import medirTiempo

class spatialQueries:
    @staticmethod
#    @medirTiempo
    def containsCountSecuencial(capa,capa2):
        equalCoord=True
        if capa.crs()!=capa2.crs():
            equalCoord=False
            if capa.crs().isGeographic()==False:
                scf=capa.crs()
                sci=capa2.crs()
            else:
                sci=capa.crs()
                scf=capa2.crs()
            transform=QgsCoordinateTransform(sci, scf, QgsProject.instance())
        conteo=0
        for i in capa.selectedFeatures():
            geo=i.geometry()
            if equalCoord==False:
                geo.transform(transform)
            for j in capa2.getFeatures():
                if geo.boundingBoxIntersects(j.geometry()):
                    if geo.contains(j.geometry()):
                        conteo=conteo+1
        return conteo
    
    @staticmethod
#    @medirTiempo
    def containsCountOptimi(capa,capa2,IE):
        equalCoord=True
        if capa.crs()!=capa2.crs():
            equalCoord=False
            if capa.crs().isGeographic()==False:
                scf=capa.crs()
                sci=capa2.crs()
            else:
                sci=capa.crs()
                scf=capa2.crs()
        transform=QgsCoordinateTransform(sci, scf, QgsProject.instance())
        conteo=0
        for i in capa.selectedFeatures():
            geo=i.geometry()
            if equalCoord==False:
                geo.transform(transform) 
            engine = QgsGeometry.createGeometryEngine(geo.constGet())
            engine.prepareGeometry()
            candidate_ids = index.intersects(geo.boundingBox())
            req = QgsFeatureRequest().setFilterFids(candidate_ids)
            for c in capa2.getFeatures(req):
                if engine.contains(c.geometry().constGet()):
                    conteo += 1
        return conteo
    
    @staticmethod
#    @medirTiempo
    def containsCountProcess(capa,capa2):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
        pre=6  #contains
        inters=QgsProcessingFeatureSourceDefinition(capa.source(),True)
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)
        c=capa2.selectedFeatureCount()
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        return c 
    
    @staticmethod
#    @medirTiempo
    def containsCountAttribProcess(capa,capa2,campo,atributo):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
        pre=6  #contains
        inters=QgsProcessingFeatureSourceDefinition(capa.source(),True)
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)
        featIds=capa2.selectedFeatureIds()
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        idCampo=capa2.fields().indexOf(campo)
        reqts= QgsFeatureRequest().setFilterFids(featIds)
        reqts.setFlags(QgsFeatureRequest.NoGeometry )
        reqts.setSubsetOfAttributes([idCampo])
        lfeat=capa2.getFeatures(reqts)
        field=capa2.fields().field(campo)
        conteo=0
        if field.isNumeric:
            try:
                atributo=float(atributo)
            except:
                pass
        for i in lfeat:
            valor=i[campo]
            if i[campo]==atributo:
                conteo=conteo+1
        del(lfeat)
        del(featIds)
        return conteo
    
    @staticmethod
    def densityProcess(capa,capa2,divisor=1):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
        
        area=sum([i.geometry().area() for i in capa.selectedFeatures()])
        area=area/divisor
        pre=6  #contains
        inters=QgsProcessingFeatureSourceDefinition(capa.source(),True)
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)
        c=capa2.selectedFeatureCount()
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        return c/area 
    
    @staticmethod
    def densityAttribProcess(capa,capa2,campo,divisor=1):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
        
        area=sum([i.geometry().area() for i in capa.selectedFeatures()])
        area=area/divisor
        pre=6  #contains
        inters=QgsProcessingFeatureSourceDefinition(capa.source(),True)
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)
        
        accum=sum([i[campo] for i in capa2.selectedFeatures()\
             if type(i[campo])==int or type(i[campo])==float])
        
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        return accum/area
    
    @staticmethod
    def bufferCountProcess(capa,capa2,dist):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
            
        crs=capa.crs().authid()
#        uri="polygon?CRS="+crs
        uri="polygon?crs="+capa.crs().toWkt()
        capaTemp=QgsVectorLayer(uri, "capa temp", "memory")
        if capaTemp.crs().authid()!=crs:
            capaTemp.setCrs(capa.sourceCrs())
        campID = QgsField("ID", QVariant.String)
        capaTemp.dataProvider().addAttributes([campID])
        capaTemp.updateFields()
        entidades=[]
        
        for e,i in enumerate(capa.selectedFeatures()):
            feat=QgsFeature()
            feat.setFields(capaTemp.fields())
            feat.setAttribute(0,e)
            geom=i.geometry()
            buffer=geom.buffer(dist,10)
            feat.setGeometry(buffer)
            entidades.append(feat)
        capaTemp.dataProvider().addFeatures(entidades)
        
        pre=6  #contains
        inters=capaTemp
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)
        conteo=capa2.selectedFeatureCount()
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        del(capaTemp)
        return conteo
        
    @staticmethod
    def bufferAttribProcess(capa,capa2,dist,campo,atributo,tipo='conteo'):
        selection=False
        idsSelect=None
        if capa2.selectedFeatureCount()>0:
            selection=True
            idsSelect=capa2.selectedFeatureIds()
        if capa2.featureCount()>1000 and capa2.hasSpatialIndex()!=2:
            result=capa2.dataProvider().createSpatialIndex()
        crs=capa.crs().authid()
#        uri="polygon?CRS="+crs
        uri="polygon?crs="+capa.crs().toWkt()
        capaTemp=QgsVectorLayer(uri, "capa temp", "memory")
        if capaTemp.crs().authid()!=crs:
            capaTemp.setCrs(capa.sourceCrs())
        campID = QgsField("ID", QVariant.String)
        capaTemp.dataProvider().addAttributes([campID])
        capaTemp.updateFields()
        entidades=[]
        
        for e,i in enumerate(capa.selectedFeatures()):
            feat=QgsFeature()
            feat.setFields(capaTemp.fields())
            feat.setAttribute(0,e)
            geom=i.geometry()
            buffer=geom.buffer(dist,10)
            feat.setGeometry(buffer)
            entidades.append(feat)
        capaTemp.dataProvider().addFeatures(entidades)
        
        pre=6  #contains
        inters=capaTemp
        metodo=0 #new selection
        param={'INPUT':capa2,
               'PREDICATE':pre,
               'INTERSECT':inters,
               'METHOD':metodo   }
        alg_name = 'native:selectbylocation'
        feedback = QgsProcessingFeedback()
        processing.run(alg_name,param,feedback=feedback)

        ids=capa2.selectedFeatureIds()
        idCampo=capa.fields().indexOf(campo)
        request= QgsFeatureRequest().setFilterFids(ids)
        request.setFlags(QgsFeatureRequest.NoGeometry )
        request.setSubsetOfAttributes([idCampo])
        listResult=capa.getFeatures(request)
        resultado=0
        if tipo=='conteo':
            for i in listResult:
                if i[campo]==atributo:
                    resultado=resultado+1
        elif tipo=='sum':
            for i in listResult:
                valor=i[campo]
                if type(valor)==int or type(valor)==float:
                    resultado=resultado+valor 
        if selection is True:
            capa2.selectByIds(idsSelect)
        else:
            capa2.removeSelection()
        del(capaTemp)
        return conteo    