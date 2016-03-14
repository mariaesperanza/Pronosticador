#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Autor: Esperanza Ramirez Armijos
@Tema: Pronosticador del Futbol Ecuatoriano
@Descripcion: Genere el archivo de respuesta html, la información contenida en una instancia de la clase info_liga
'''

import recoleccion_info
import graficos_liga
import os
import sys

#  CLASE VOLCADO INFO  
class volcado_info:
    #Constructor que toma un objeto de clase info_liga basico (solo contiene info en el campo jornada)
    #Se establece como salida estandar el fichero que seria index para la info de jornada en instancia_info_liga
    def __init__(self, instancia_info_liga):
        self.graficas=graficos_liga.graficos_liga(instancia_info_liga)
        self.index="jornada"+str(instancia_info_liga.get_jornada())+".html"
        self.optimos="optimosj"+str(instancia_info_liga.get_jornada())+".html"
        self.dir_imgs="imgs"

        try:
            print("Cargando Datos Para El Pronosticador")
            os.remove(self.index)
            #os.remove(self.optimos)
        except:
            print("Generando INDEX...")
        self.fsalida=open(self.index, 'a+')
        sys.stdout=self.fsalida

    #Metodo que genera todos los archivos de imagen de las graficas en un directorio dado
    def genera_graficas(self):
        self.graficas.set_graficos_ratios_todos_guarda(self.dir_imgs)
        self.graficas.set_graficos_resultados_todos_guarda(self.dir_imgs)
        self.graficas.set_grafico_marca_encaja_primero_todos_guarda(self.dir_imgs)

    #Metodo que genera la lineas de estilo tocadas manualmente
    def estilo_manual(self):
        print("<STYLE type=text/css>")
        print(".pstrong{ font-weight: bold; }")
        print(".pgrande{ font-size:18; }")
        print(".lider{ color: blue; font-weight: bold; font-size:18; }")
        print(".champions{ color: grey; font-weight: bold; font-size:18; }")
        print(".uefa{ color: orange; font-weight: bold; font-size:18; }")
        print(".descenso{ color: red; font-weight: bold; font-size:18; }")
        print(".img-grafica{ display: inline; float: right; -webkit-column-span: in-column; -moz-column-span: in-column;} ")
        print(".img-ratios{ display: inline; float: left; -webkit-column-span: in-column; -moz-column-span: in-column;} ")
        print(".navbar{ background: black; text-align:center; padding: 3 0;}")
        print(".link-github{ color: #363636; font-weight: bold; font-size:14; }")
        print(".link-inicio{ color: #363636; font-weight: bold; }")
        print("</STYLE>")

    #Metodo que vuelca en el archivo la deficion del estilo
    def estilo(self):
        print("<link href='css/bootstrap.min.css' rel='stylesheet'>")
        print("<link href='css/agency.css' rel='stylesheet'>")
        print("<link href='css/backtotop.css' rel='stylesheet'>")
        self.estilo_manual()

    #Metodo que vuelca en el archivo la deficion del estilo para los html de enfrentamientos
    def estilo_partidos(self):
        print("<link href='../css/bootstrap.min.css' rel='stylesheet'>")
        print("<link href='../css/agency.css' rel='stylesheet'>")
        self.estilo_manual()

    #Metodo que vuelva en el archivo la cabecera al completo
    def cabecera(self):
        print("<html>")
        print("<head>")
        print("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
        print("<title>Información Jornada "+ str(self.graficas.get_instancia_info_liga().get_jornada())+"</title>")
        self.estilo()

        print("</head>")

    def back_to_top(self):
        print("<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js'></script> <script>$(document).ready(function(){	// hide #back-top first	$('#back-top').hide();		// fade in #back-top	$(function () {		$(window).scroll(function () {			if ($(this).scrollTop() > 100) {				$('#back-top').fadeIn();			} else {				$('#back-top').fadeOut();			}		});		// scroll body to 0px on click		$('#back-top a').click(function () {			$('body,html').animate({				scrollTop: 0			}, 800);			return false;		});	});});</script>")

    #Metodo que vuelva la info de un equipo dado
    def info_equipo(self, e):
        if e in self.graficas.get_instancia_info_liga().get_equipos():
            print("<div class='container' id='%s'>" % e[:-2].replace(' ', ''))
            print("<div class='row'>")
            print("<br>")
            print("<h2 class='section-heading'>")
            print(e, ":")
            print("</h2>")
            print("</div>")
            #Ratios y resultados
            #Grafica de ratios
            print("<div class='row'>") #ojo
            g=self.dir_imgs+"/ratio"+e[:-2]+".png"
            print("<img src='%s' class='img-ratios img-responsive' width=450  />" % g)
            g=self.dir_imgs+"/resultados"+e[:-2]+".png"
            print("<img src='%s' class='img-grafica img-responsive' width=450/>" % g)

            c=self.graficas.get_instancia_info_liga().get_clasif()[e]
            posicion=int(c[0][:])
            print("</div>")

            print("<div class='row'>")
            print("<br><p class='pgrande'>Ha jugado ", c[1], "partidos; ", c[3], "victorias, ", c[4], "empates,", c[5], "derrotas;  =>  ", c[2], "puntos.</p>")

            #Posicion | Color segun que posicion
            if posicion==1:
                print("<p class='posicion lider'>  \tPosicion: ", c[0], " .Lider</p>")
            elif posicion==18 or posicion==19 or posicion==20:
                print("<p class='posicion descenso'>  Posicion: ", c[0], " .En Descenso</p>")
            elif posicion ==2 or posicion==3 or posicion==4:
                print("<p class='posicion champions'> \tPosicion: ", c[0], " </p>")
            elif posicion==5 or posicion==6:
                print("<p class='posicion uefa'>  \tPosicion: ", c[0], " </p>")
            else:
                print("<p class='posicion pgrande'>  \tPosicion: ", c[0], "</p>")
            print("<p class='pgrande'>LLeva: ", c[6], "goles a favor. |", c[7], "goles en contra. | ", c[8],"</p>")
            print("</div>")
            print("<br>")
            
            #Goles Total
            gall=self.graficas.get_instancia_info_liga().get_golesTotal()[e[1:]]
            print("<div class='col-md-4'>") # Para posicionamiento en varias columnas!
            print("<h3>GOLES:</h3>")
            print("<p class='pstrong' >Media goles por partido: ", gall[1], "</p>")
            print("<p>Partidos con: <br>más de <strong>0.5</strong> goles:  ", gall[2], "<br>más de <strong>1.5</strong>:  ", gall[3], "<br>más de <strong>2.5</strong>:  ", gall[4], "<br>más de <strong>3.5</strong>:  ", gall[5], "<br>más de <strong>4.5</strong>: ", gall[6], "</p>")
            
            #Goles e info Casa
            gcasa=self.graficas.get_instancia_info_liga().get_golesLocal()[e[1:]]
            pcasa=self.graficas.get_instancia_info_liga().get_partidosCasa()[e]
            print("<p class='pstrong'>Como LOCAL: </p><p>", gcasa[0], "partidos: ", pcasa[0], "victorias, ", pcasa[1], " empates, ", pcasa[2], "derrotas. <br>", pcasa[3], "goles a favor. |", pcasa[4], "goles en contra.</p>" )
            print("<p>Media goles por partido en casa: ", gcasa[1], "</p>")
            print("<p>En casa. Partidos con: <br>más de <strong>0.5</strong> goles: ", gcasa[2], "<br>más de <strong>1.5</strong>: ", gcasa[3], "<br>más de <strong>2.5</strong>: ", gcasa[4], "<br>más de <strong>3.5</strong>: ", gcasa[5], "<br>más de <strong>4.5</strong>: ", gcasa[6], "</p>")
            
            #Goles e info fuera
            gfuera=self.graficas.get_instancia_info_liga().get_golesVisitante()[e[1:]]
            pfuera=self.graficas.get_instancia_info_liga().get_partidosFuera()[e]
            print("<p class='pstrong'>Como VISITANTE: </p><p>", gfuera[0], "partidos: ",pfuera[0], "victorias, ", pfuera[1], " empates, ", pfuera[2], "derrotas. ", pfuera[3], "goles a favor. |", pfuera[4], "goles en contra.</p>" )
            print("<p>Media goles por partido en fuera: ", gfuera[1], "</p>")
            print("<p>Fuera. Partidos con: <br>más de <strong>0.5</strong> goles: ", gfuera[2], "<br>más de <strong>1.5</strong>: ", gfuera[3], "<br>más de <strong>2.5</strong>: ", gfuera[4], "<br>más de <strong>3.5</strong>: ", gfuera[5], "<br>más de <strong>4.5</strong>: ", gfuera[6], "</p>")
            print("</div>")
            print("<div class='col-md-4'>")
            print("</div>")
            print("<div class='col-md-4'>")
            
            #Cantidad de goles por partido
            ip=self.graficas.get_instancia_info_liga().get_infopartidos()[e]
            print("<h3>Promedio de Goles Marcados/Encajados (c. 10 minutos)</h3>")
            print("<p>")
            print("Puntos por partido: <strong>", ip[0], "</strong><br>")
            print("Partidos con mas de <strong>2.5</strong> goles(a favor+en contra): <strong>", ip[1], "</strong><br>")
            print("Partidos <strong>sin encajar: ", ip[2], "</strong><br>")
            print("Partidos <strong>sin marcar: ", ip[3], "</strong><br>")
            print("Partidos <strong>ambos equipos marcan: ", ip[4], "</strong>")
            print("</p>")

            partidoscasa=self.graficas.get_instancia_info_liga().get_partidosCasa()[e]
            partidosfuera=self.graficas.get_instancia_info_liga().get_partidosFuera()[e]

            #Porcentaje puntos casa-fuera
            ppcasa=(int(partidoscasa[0])*3+int(partidoscasa[1]))/int(c[2])
            ppfuera=(int(partidosfuera[0])*3+int(partidosfuera[1]))/int(c[2])
            print("<p>% puntos ganados en Casa: <strong>", ppcasa*100, '%</strong></p>')
            print("<p>% puntos ganados Fuera: <strong>", ppfuera*100, '%</strong></p>')

            #Porcentajes goles a favor-en contra en casa-fuera
            pgfavorcasa=int(partidoscasa[3])/int(c[6])
            pgfavorfuera=int(partidosfuera[3])/int(c[6])
            pgcontracasa=int(partidoscasa[4])/int(c[7])
            pgcontrafuera=int(partidosfuera[4])/int(c[7])

            print("<p>")
            print("% goles a favor como local:<strong>", pgfavorcasa*100, '%</strong>  <br>| ', partidoscasa[3], "de", c[6], " anotados<br>")
            print("% goles en contra como local:<strong>", pgcontracasa*100, '%</strong> <br>| ', partidoscasa[4], "de", c[7], " encajados<br>")
            print("% goles a favor como visitante:<strong>", pgfavorfuera*100, '%</strong> <br>| ', partidosfuera[3], "de", c[6], " anotados<br>")
            print("% goles en contra como visitante:<strong>", pgcontrafuera*100, '%</strong> <br>| ', partidosfuera[4], "de", c[7], " encajados<br>")
            print("</p>")
            print("</div>")
            print("</div>")

# Metodo que crea el html con la info dedicada a un partido de la siguiente jornada
    def info_enfrentamiento(self, partido):
        loc=partido[0]
        vis=partido[1]
        print("<html>")
        print("<head>")
        print("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
        print("<title>Jorná ", self.graficas.get_instancia_info_liga().get_jornada(), ": ", loc, "-", vis, "</title>")
        self.estilo_partidos()
        print("</head>")
        print("<body>")
        print("<div class='container'>")
        print("<div class='intro-text'>")
        print("<h2 class='section-heading'>Info siguiente jornada partido ", loc, "-", vis, ":</h2>")
        print("</div>")

        #Nav con los nombres de cada equipo. Pinchando en un equipo te lleva a su info
        print("<nav class='navbar navbar-default navbar-fixed-top'>")
        for e in sorted(self.graficas.get_instancia_info_liga().get_equipos()):
           print("<a class='page-scroll' href=%s#%s>%s</a>" % ('../'+self.index, e[:-2].replace(' ', ''), e) )
           print(" | ")
        print("</nav>")
        
        #Barra con los enlaces a los partidos de la proxima jornada
        print("<h5><a class='link-inicio' href='../%s'>Inicio</a></h5>" % (str(self.index)))
        print("<h4>Partidos siguiente jornada:</h4>")
        for p in self.graficas.get_instancia_info_liga().get_siguiente_jornada():
            enlace=p[0][1:-1].replace(' ', '')+"-"+p[1][1:-1].replace(' ', '')+".html"
            print("<span><a class='navbar navbar-default' href=%s >%s</a><span>" % (str(enlace), p[0]+"-"+p[1]))
        print("</nav>")

    #INICIO Muestra la informacion del partido a analizar
        #AQUI ES LA PARTE A MODIFICAR
        print("<div class='row'>")
        print("<h2 class='section-heading'>")
        print(loc, "-", vis, " : Jornada ", str(self.graficas.get_instancia_info_liga().get_jornada()+1))
        print("</h2>")
        print("</div>")

        #Grafica de ratios (goles marcados/encajados)
        print("<div class='row'>")
        gl='../'+self.dir_imgs+"/ratio"+loc[:-2]+".png"
        gv='../'+self.dir_imgs+"/ratio"+vis[:-2]+".png"
        print("<img src='%s' class='img-ratios img-responsive' width=450 />" % gl)
        print("<img src='%s' class='img-ratios img-responsive' width=450 />" % gv)
        print("</div>")

        #Grafica de resultados
        print("<br><br>")
        print("<div class='row'>")
        gl='../'+self.dir_imgs+"/resultados"+loc[:-2]+".png"
        gv='../'+self.dir_imgs+"/resultados"+vis[:-2]+".png"
        print("<img src='%s' class='img-ratios img-responsive' width=400/>" % gl)
        print("<img src='%s' class='img-ratios img-responsive' width=400/>" % gv)
        print("</div>")

        #Grafica de Marca-Encaja primero
        print("<div class='row'>")
        g='../'+self.dir_imgs+"/marcaencaja"+loc[:-2]+".png"
        print("<img src='%s'  width=400/>" % g)
        g='../'+self.dir_imgs+"/marcaencaja"+vis[:-2]+".png"
        print("<img src='%s'  width=400/>" % g)
        '''
        print("</div>")
        print("<div class='col-md-3'>")
        print("<h4>%s</h4>" % (loc))
        '''
    #FIN Muestra la informacion del partido a analizar
        print("</body>")
        print("<br><br>")
        self.pie()

    #Metodo que vuelva la info de todos los equipos
    def info_equipos(self):
        for i in sorted(self.graficas.get_instancia_info_liga().get_equipos()):
            self.info_equipo(i)

    #Metodo que incluye el body, la info global
    def cuerpo(self):
        print("<body>")
        print("<div class='container'>")
        print("<div class='intro-text'>")
        print("<h2 class='section-heading'>Info actualizada tras final de jornada ", self.graficas.get_instancia_info_liga().get_jornada(), ":</h2>")
        print("</div>")
        self.back_to_top()
        print("<p id='back-top'><a href=%s ><span>Vuerta parriba</span></a></p>" % (self.index))

        #Nav con los nombres de cada equipo. Pinchando en un equipo te lleva a su info
        print("<nav class='navbar navbar-default navbar-fixed-top'>")
        for e in sorted(self.graficas.get_instancia_info_liga().get_equipos()):
           print("<a class='page-scroll' href=#%s>%s</a>" % (e[:-2].replace(' ', ''), e) )
           print(" | ")
        print("</nav>")
        print("<nav>")

        #Lista con la info para cada par de equipos correspondientes a los partidos de la siguiente jornada
        print("<h4>Partidos siguiente jornada:</h4>")
        for p in self.graficas.get_instancia_info_liga().get_siguiente_jornada():
            enlace='partidos/'+p[0][1:-1].replace(' ', '')+"-"+p[1][1:-1].replace(' ', '')+".html"
            print("<a class='navbar navbar-default' href=%s >%s</a>" % (str(enlace), p[0]+"-"+p[1]))
        print("</nav>")
        print("<div class='container'><h1>Info de todos los equipos: Jornada "+str(self.graficas.get_instancia_info_liga().get_jornada())+"</h1></div>")

        #Llamada a volcado info equipos
        self.info_equipos()
        print("</div>") #Fin container
        print("</body>")

    #Metodo que incluye el footer
    def pie(self):
        print("<footer>")
        print("<div class='container'>")
        print("<p>Web Creada Por Esperanza Ramirez Armijos</p>")
        print("</div>")
        print("</footer>")
        print("</html>")

    #Metodo que vuelca la información completa de todos los equipos en un html
    def todo_index(self):
        self.genera_graficas()
        self.cabecera()
        self.cuerpo()
        self.pie()
        try:
            sys.stdout=sys.__stdout__
            self.fsalida.close()
        except:
            print("No se ha podido cerrar", str(self.fsalida))

    #Metodo que genera cada html correspondiente a cada partido de la siguiente jornada
    def todo_enfrentamientos(self):
        directorio='partidos/'
        if not os.path.isdir(directorio):
            os.makedirs(directorio)
        for p in self.graficas.get_instancia_info_liga().get_siguiente_jornada():
            enlace=directorio+p[0][1:-1].replace(' ', '')+"-"+p[1][1:-1].replace(' ', '')+".html"
            if os.path.exists(enlace):
                os.remove(enlace)
            fenlace=open(enlace, 'a+')
            sys.stdout=fenlace
            #try:
            self.info_enfrentamiento(p)
            #except:
            sys.stdout=sys.__stdout__
            #    print("Error en tiempo de ejecucion")
            fenlace.close()

        try:
            sys.stdout=sys.__stdout__
        except:
            print("No se ha podido cerrar", str(self.fsalida))

    #Metodo que actualiza el html de index (solo ejecutar si ya existen las graficas)
    def actualiza_index(self):
        self.cabecera()
        self.cuerpo()
        self.pie()
        try:
            sys.stdout=sys.__stdout__
            self.fsalida.close()
        except:
            print("No se ha podido cerrar", str(self.fsalida))
# FIN CLASE VOLCADO INFO 
#MAIN PARA MOSTRAR
if __name__ == "__main__":
    j=7
    info_jornada=recoleccion_info.info_liga(j)

    #JORNADA SIGUIENTE: 8
    """  DEFINICION DE LOS SIGUIENTES PARTIDOS  """
    siguiente_jornada=[[' Delfin SC ', ' River Ecuador ']] #0
    siguiente_jornada.append([' Independiente ', ' Fuerza Amarilla ']) #1
    siguiente_jornada.append([' LDU de Quito ', ' Mushuc Runa ']) #2
    siguiente_jornada.append([' Emelec ', ' Barcelona SC ']) #3
    siguiente_jornada.append([' El Nacional  ', ' U. Catolica ']) #4
    siguiente_jornada.append([' Dep. Cuenca ', ' Aucas ']) #5

    info_jornada.set_siguiente_jornada(siguiente_jornada)

    info=volcado_info(info_jornada)
    info.todo_index()
    info.todo_enfrentamientos()
    print("Done!")
