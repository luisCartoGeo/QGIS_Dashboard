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
#Concultar datos
class queriesData:
    
    #totalizar clases, totaliza un campo numerico por un campo categorico
    @staticmethod
    def summarizeClasses(listaEntidades,campoC,campoN):
        resultado=dict()
        for e in listaEntidades:
            categoria=e[campoC]
            valor=e[campoN]
            if type(valor)==int or type(valor)==float:
                if categoria in resultado:
                    resultado[categoria]=resultado[categoria]+valor
                else:
                    resultado[categoria]=valor
        return resultado
    
    #totalizar campos: totaliza todos los campos numericos
    @staticmethod
    def summarizeFields(listaEntidades,listaCampos):
        resultado=dict()
        for e in listaEntidades:
            for c in listaCampos:
                valor=e[c]
                if type(valor)==int or type(valor)==float:
                    if c in resultado:
                        resultado[c]=resultado[c]+valor
                    else:
                        resultado[c]=valor
        return resultado
    
    #Calcular el porcentaje del valor de un campo de las entidades seleccionadas
    #considera si el total existe como una variable o no, por defecto el total es None
    @staticmethod
    def porcentaje(listaEntidades,campo,capa=None,total=None):
        if total==None:
            sumat=sum([f[campo] for f in capa.getFeatures() if type(f[campo])==int or type(f[campo])==float ])
            valorSelec= sum([f[campo] for f in listaEntidades if type(f[campo])==int or type(f[campo])==float ])
            resultado=(valorSelec*100)/sumat
        else:
            valorSelec= sum([f[campo] for f in listaEntidades if type(f[campo])==int or type(f[campo])==float ])
            resultado=(valorSelec*100)/total
        return resultado
    
    @staticmethod
    def valuesSelectRegister(listaEntidades,campoC,listCamposN,max):
        resultado=[]
        for e,i in enumerate(listaEntidades):
            if e==max:
                break
            categoria=i[campoC]
            dicc=dict()
            for c in listCamposN:
                valor=i[c]
                if type(valor)==int or type(valor)==float:
                    if c in dicc:
                        dicc[c]=dicc[c]+valor
                    else:
                        dicc[c]=valor
                else:
                    if c in dicc:
                        dicc[c]=dicc[c]+0
                    else:
                        dicc[c]=0
            resultado.append((categoria,dicc))
        return resultado
        
    