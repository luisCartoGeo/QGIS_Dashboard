# QGIS_Dashboard
<table align="center">
    <p align = "center">
      <a href="https://www.linkedin.com/in/luisedpg/"><img alt="LuisGeo" src="https://img.shields.io/badge/AUTOR-Luis%20Eduardo%20Perez%20Graterol-brightgreen"></a>
       <a href="https://github.com/luisCartoGeo/QGIS_Dashboard/tree/master/"><img alt="LuisGeo" src="https://img.shields.io/badge/ENGLISH-Documentation-lightgrey"></a>
      <a href="https://github.com/luisCartoGeo/QGIS_Dashboard/stargazers"><img src="https://img.shields.io/badge/STARS-15-blue"></a>
        <a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FluisCartoGeo%2FQGIS_Dashboard%2F"><img alt="Twitter" src="https://img.shields.io/twitter/url?label=TWITTER&style=social&url=https%3A%2F%2Ftwitter.com%2FLuiseperezg"></a>
      </P>
</table>
     <h2><b>Repositorio del código del plugin para la construcción de Dashboards en QGIS</b></h2><br>
El objetivo del plugin <strong>QGIS Dashboard</strong> es permitir la creación de tableros de control en la pantalla de QGIS.<br>
<hr></hr>
<h2>ESTE PLUGIN SE ENCUENTRA EN DESARROLLO (PRODUCCION)</h2>
<center><img style="text-align:center" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/trabajando.gif" style="max-width:80%;"></center>
<hr></hr>

## Indice

- [Introducción](https://www.linkedin.com/pulse/generalidades-y-procedimiento-para-la-instalaci%25C3%25B3n-del-perez-graterol)
- [ ¿Por qué QGIS necesita un Dashboard? ](https://www.linkedin.com/pulse/generalidades-y-procedimiento-para-la-instalaci%25C3%25B3n-del-perez-graterol)
- [Instalación del plugin QGIS Dashboard](https://www.linkedin.com/pulse/generalidades-y-procedimiento-para-la-instalaci%25C3%25B3n-del-perez-graterol)
    - [Procedimiento para descargar el plugin](https://www.linkedin.com/pulse/generalidades-y-procedimiento-para-la-instalaci%25C3%25B3n-del-perez-graterol)
    - [Procedimiento para la instalación](https://www.linkedin.com/pulse/generalidades-y-procedimiento-para-la-instalaci%25C3%25B3n-del-perez-graterol)
 - [Caracteristicas del plugin QGIS Dashboard](#caracteristicas)
 - [<b>Tutorial rapido</b>](#Tutorial-rapido)
 - [Tutorial](#tutorial)
    - [Funcionamiento general del plugin](#funcionamiento-general-del-plugin)
    - [Graficos e indicadores disponibles](#graficos-e-indicadores-disponibles)
    - [Asistente para crear paneles](#Asistente-para-crear-panels)
        - [Configuración inicial](#configuración-inicial)
            - [Numero de paneles a construir](#Numero-de-paneles-a-construir)
            - [Tamaño y posición inicial](#Tamaño-y-posición-inicial)
            - [Opciones adicionales](#Opciones-adicionales)
        - [Diseño de graficos e indicadores](#Diseño-de-graficos-e-indicadores)
            - [Panel de texto](#Panel-de-texto)
                - [Asignando un estilo](#Asignando-un-estilo)
                - [Configurando los colores](#Configurando-los-colores)
                - [Integrando y configurando un icono](#Integrando-y-configurando-un-icono)
                - [Consultas de datos](#Consultas-de-datos)
                    - [Totalizar un atributo](#Totalizar-un-atributo)
                    - [Porcentaje. Proporción](#Porcentaje.-Proporción)
                    - [Estadistica de un atributo](#Estadistica-de-un-atributo)
                - [Consultas espaciales](#Consultas-espaciales)
                    - [Entidades contenidas. Poligonos](#Entidades-contenidas.-Poligonos)
                    - [Entidades a una distancia. Lineas-puntos](#Entidades-a-una-distancia.-Lineas-puntos)
                    - [Entidades contenidas que coinciden con](#Entidades-contenidas-que-coinciden-con)
                    - [Entidades a una distancia que contenide con](#Entidades-a-una-distancia-que-contenide-con)
            - [Grafico Indicador](#Grafico-Indicador)
            - [Grafico de Barras](#Grafico-de-Barras)
            - [Grafico de lineas. Series](#Grafico-de-lineas.-Series)
    -  [Mover, redimensionar y borrar paneles](#Mover-y-redimensionar-paneles)
    -  [Darle trasnparencia a los paneles](#Darle-trasnparencia-a-los-paneles)
    -  [Guardar un tablero](#Guardar-un-tablero)
    -  [Abrir un tablero desde archivo](#Abrir-un-tablero-desde-archivo)

## Tutorial
### Funcionamiento general del plugin
Los <strong>Tableros de Control (Dashboards)</strong> son construidos creando paneles los cuales contendrán indicadores o gráficos, los paneles son adaptables, el usuario podrá mover, borrar, redimensionar utilizando las herramientas de anotación de QGIS.<br>
Este plugin aprovecha y extiende mediante Python las <strong>Anotaciones Html</strong> propias de QGIS para darles mayor funcionalidad, desplegar gráficos, responder a eventos.

### Graficos e indicadores disponibles
Hasta el momento el plugin cuenta con cuatro tipos de paneles:
<ul><li><b>Paneles de texto:</b> despliegan un valor o indicador de un conjunto de datos o consulta espacial. Este panel aunque sencillo, presenta la mayor variedad de estilos y configuraciones. El valor desplegado puede provenir de un resumen estadístico de un conjunto de datos o una consulta espacial. Las opciones de consulta espacial variaran dependiendo de la geometría de la capa consultada. Si es un capa de <strong>polígono</strong> podrá consultar las entidades contenidas que pertenezcan a otra capa, también puede consultar las entidades contenidas a una distancia especificada de las entidades seleccionadas de la capa de poligono (buffer). Si es <strong>línea</strong> o <strong>punto</strong> solo podrá consultar las entidades contenidas de otra capa a una distancia especificada de las entidades seleccionadas.</li>
  <li><b>Grafico indicador</b> también llamado grafico de 'bala'o 'velocímetro', de forma similar al panel de texto muestra un valor o indicador, pero en un contexto que facilita su interpretación, el usuario debe especificar un rango dentro del que se espera que dicho valor oscile, además un valor umbral, después del cual se considera la condición desfavorable o favorable.
  Este panel permitirá opciones similares de consulta que el panel de texto.</li>
  <li><b>Grafico de barras</b> puede desplegar un gráfico de barras de un campo numérico dadas las categorías de un campo de texto de la tabla de atributos. También puede generar el grafico de un conjunto de campos numéricos presentes en la tabla de atributos. En cuanto al estilo puede configurar colores y tamaños de textos, también puede asignar un color a las barras o utilizar una de las paletas de colores disponibles.</li>
  <li><b>Grafico de líneas</b> mediante este grafico puede representar un conjunto de datos que presentan una secuencia cronológica. Presenta opciones de configuración de estilos similares al grafico de barras. Puede representar solo puntos si configura un espesor de línea igual a 0, líneas del grosor especificado o áreas rellenas.</li>
  </ul>
<img width="80%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/DASHBOARDS.jpg" style="max-width:100%;">




