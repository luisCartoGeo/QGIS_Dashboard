<h1># QGIS_Dashboard</h1>
<h2><b>Repositorio del código del plugin para la construcción de Dashboards en QGIS</b></h2><br>
El objetivo del plugin <strong>QGIS Dashboard</strong> es permitir la creación de tableros de control en la pantalla de QGIS.<br>
<hr></hr>
<h2>ESTE PLUGIN SE ENCUENTRA EN DESARROLLO (PRODUCCION)</H2>
<img width="80%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/trabajando.gif" style="max-width:80%;">
<hr></hr>
Los <strong>Tableros de Control (Dashboards)</strong> son construidos creando paneles los cuales contendrán indicadores o gráficos, los paneles son adaptables, el usuario podrá mover, borrar, redimensionar utilizando las herramientas de anotación de QGIS.<br>
Este plugin aprovecha y extiende mediante Python las <strong>Anotaciones Html</strong> propias de QGIS para darles mayor funcionalidad, desplegar gráficos, responder a eventos.

<h2><strong>Instalación y requerimientos</strong></h2>
Este plugin <B>NO</B> tiene requerimientos especiales, sencillamente instalar en una versión QGIS3.10 o superior.<br>

<h1><b>Interfaz de usuario</b></h1>
<img width="100%" src="https://user-images.githubusercontent.com/79421833/122484184-1c37c280-cfa2-11eb-9545-56e7be7a38ee.jpg" style="max-width:100%;">

<h1><b>Gráficos e indicadores</h1></b>
Hasta el momento el plugin cuenta con cuatro tipos de paneles:
<ul><li><b>Paneles de texto:</b> despliegan un valor o indicador de un conjunto de datos o consulta espacial. Este panel aunque sencillo, presenta la mayor variedad de estilos y configuraciones. El valor desplegado puede provenir de un resumen estadístico de un conjunto de datos o una consulta espacial. Las opciones de consulta espacial variaran dependiendo de la geometría de la capa consultada. Si es un capa de <strong>polígono</strong> podrá consultar las entidades contenidas que pertenezcan a otra capa, también puede consultar las entidades contenidas a una distancia especificada de las entidades seleccionadas de la capa de poligono (buffer). Si es <strong>línea</strong> o <strong>punto</strong> solo podrá consultar las entidades contenidas de otra capa a una distancia especificada de las entidades seleccionadas.</li>
  <li><b>Grafico indicador</b> también llamado grafico de 'bala'o 'velocímetro', de forma similar al panel de texto muestra un valor o indicador, pero en un contexto que facilita su interpretación, el usuario debe especificar un rango dentro del que se espera que dicho valor oscile, además un valor umbral, después del cual se considera la condición desfavorable o favorable.
  Este panel permitirá opciones similares de consulta que el panel de texto.</li>
  <li><b>Grafico de barras</b> puede desplegar un gráfico de barras de un campo numérico dadas las categorías de un campo de texto de la tabla de atributos. También puede generar el grafico de un conjunto de campos numéricos presentes en la tabla de atributos. En cuanto al estilo puede configurar colores y tamaños de textos, también puede asignar un color a las barras o utilizar una de las paletas de colores disponibles.</li>
  <li><b>Grafico de líneas</b> mediante este grafico puede representar un conjunto de datos que presentan una secuencia cronológica. Presenta opciones de configuración de estilos similares al grafico de barras. Puede representar solo puntos si configura un espesor de línea igual a 0, líneas del grosor especificado o áreas rellenas.</li>
  </ul>
<img width="100%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/DASHBOARDS.jpg" style="max-width:100%;">


