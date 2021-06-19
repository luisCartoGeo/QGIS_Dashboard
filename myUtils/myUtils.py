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
class utils:
    @staticmethod
    def splitText(cadena):
        resultado=[]
        lbr=[]
        for e,texto in enumerate(cadena):
            if len(texto)>10:
                l=[texto[i:i+10] for i in range(0,len(texto),10)]
                text=''
                br=0
                for e,i in enumerate(l):
                    if e<len(l)-1 and len(l[e+1])>4:
                        br=br+1
                        lbr.append(br)
                        if i[-1].isspace():
                            text=text+i[:-1]+'<br>'
                        else:
                            text=text+i+'<br>'
                    else:
                        text=text+i
                resultado.append(text)
            else:
                resultado.append(texto)
        return resultado
#        return (resultado,lbr)   
    
    @staticmethod
    def splitSentence(texto,max):
        if len(texto)>max:
            l=[texto[i:i+max] for i in range(0,len(texto),max)]
            text=''
            for e,i in enumerate(l):
                if e<len(l)-1 and len(l[e+1])>4:
                    if i[-1].isspace():
                        text=text+i[:-1]+'<br>'
                    else:
                        text=text+i+'<br>'
                else:
                    text=text+i
            return text
        else:
            return texto
        