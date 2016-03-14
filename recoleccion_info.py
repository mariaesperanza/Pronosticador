#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Autor: Esperanza Ramirez Armijos
@Tema: Pronosticador del Futbol Ecuatoriano
@Descripcion: Contiene la clase info_liga para procesar y almacenar la información sobre las estadísticas contenida en los distintos archivos .txt:
'''
import sys
import os

#  CLASE INFO_LIGA  
class info_liga:
    #Constructor que solo toma por argumentos la jornada y % goles después minuto 80
    def __init__(self, jornada):
        self.jornada=jornada
        self.timing=None
        self.timing_partes=None
        self.ratios=None
        self.ratios_partes=None
        self.casa=None
        self.fuera=None
        self.clasif=None
        self.partidosCasa=None
        self.partidosFuera=None
        self.infopartidos=None
        self.goleslocal=None
        self.golesvisitante=None
        self.empates0=None
        self.golestotal=None
        self.marcaprimero=None
        self.encajaprimero=None
        self.minimoR=0
        self.maximoR=0
        self.siguiente_jornada=None
        
    #Metodo __str__ llamado cuando se realice una llamada a imprimir por pantalla a la variable con la instancia de la clase
    def __str__(self):
        mensaje="Instancia para la jornada"+ str(self.jornada)
        return mensaje
  
    #Metodos set get para el valor de jornada
    def set_jornada(self, ultima_jornada):
        self.jornada=ultima_jornada
    def get_jornada(self):
        return self.jornada
               
    #Metodo que recoge la informacion contenida en general.txt para establecer los valores de 
    # - clasif, partidosCasa, partidosFuera, infopartidos
    def procesar_clasificacion(self):

        fi=open('infotxt/general.txt', 'r')
        info = [i for i in fi]
        fi.close()
        #print(info)
        while '\n' in info:
            info.remove('\n')
        
        todo={}
        clasif={}
        partidoscasa={}
        partidosfuera={}
        ipartidos={}
        cont=0
        for i in info:
            temp=i.split('\t')                
            if not cont:
                eq=temp[1]
                aux=[]
                aux=[j for j in temp if j!=temp[1]]
                cont=1
            else:
                for j in temp:
                    aux.append(j)
                cont+=1
                if cont==3:
                    todo[eq]=aux[:]
                    cont=0
                    aux.clear()
                    
        for i in todo:
            aux=todo[i]
            clasif[i]=[aux[0], aux[1], aux[8], aux[2], aux[3], aux[4], aux[5], aux[6], aux[7]]
            partidoscasa[i]=aux[10:15]
            partidosfuera[i]=aux[21:26]
            ipartidos[i]=aux[27:32]
            ipartidos[i][4]=ipartidos[i][4][0:3]
        
        self.clasif=clasif    
        self.partidosCasa=partidoscasa                    
        self.partidosFuera=partidosfuera
        self.infopartidos=ipartidos
        
    # Metodo que devuelve un array con todos los nombres de los equpipos (son keys de los maps)
    def get_equipos(self):
        return [i for i in self.clasif]
       
# Metodos get para las variables asignadas tras la ejecucion del metodo clasificacion         
    def get_clasif(self):
        return self.clasif
    def get_partidosCasa(self):
        return self.partidosCasa
    def get_partidosFuera(self):
        return self.partidosFuera
    def get_infopartidos(self):
        return self.infopartidos        

    #Metodo que recoge la informacion en timing.txt para establecer los valores de
    # - timing, timing_partes, ratios, ratios_partes
    def procesar_timing(self):
        fi=open('infotxt/timing.txt', 'r')
        info = [i for i in fi]
        fi.close()

        timing={}
        timing_partes={}
        ratios={}
        ratios_partes={}

        for i in info:
            temp=i.split('\t')            
            aux=temp[1:11]        
            timing[temp[0]]=aux

        for i in info:
            temp=i.split('\t')
            aux=temp[10:13]
            timing_partes[temp[0]]=[aux[-2], aux[-1]]

        for i in timing:
            aux=timing[i]            
            t=[]            
            for j in aux:
                if j!='':
                    if j[1]!=' ':
                        a=int(j[0:2])
                    else:
                        a=int(j[0])
                    if j[5]!=' ':
                        b=int(j[4:6])
                    else:
                        b=int(j[4])
                    ratio=a-b
                    t.append(ratio)
            ratios[i]=t[:]
            t.clear()
        
        for i in timing_partes:
            aux=timing_partes[i]        
            t=[]
            for j in aux:
                if j!='':
                    if j[1]!=' ':
                        a=int(j[0:2])
                    else:
                        a=int(j[0])
                    if j[5]!='\\':
                        b=int(j[4:6])
                    else:
                        b=int(j[4])
                    ratio=a-b
                    t.append(ratio)
            ratios_partes[i]=t[:]
            t.clear()
    
        self.timing=timing
        self.timing_partes=timing_partes
        self.ratios=ratios
        self.ratios_partes=ratios_partes

# Metodos get para las variables asignadas tras la ejecucion del metodo timing
    def get_timing(self):
        return self.timing
    def get_timing_partes(self):
        return self.timing_partes
    def get_ratios(self):
        return self.ratios
    def get_ratios_partes(self):
        return self.ratios_partes                

    #Metodo que recoge la informacion ya almacenada en ratios para establecer los valores de
    # - maximoR, minimoR
    def procesar_ratiomaxmin(self):
        if(self.ratios!=None):
            max_temp = min_temp = 0
            for i in self.ratios:
                aux=self.ratios[i]
                if max(aux)>max_temp:
                    max_temp=max(aux)
                if min(aux)<min_temp:
                    min_temp=min(aux)
            self.maximoR=max_temp
            self.minimoR=min_temp

# Metodos get para las variables asignadas tras la ejecucion del metodo procesar_ratiomaxmin
    def get_maximoR(self):
        return self.maximoR
    def get_minimoR(self):
        return self.minimoR

    #Metodo que recoge la informacion en goleslocal.txt, golesvisitante.txt, golestotal.txt  para establecer los valores de
    # - gcasa, gfuera, gall  
    def procesar_goles(self):
        info=[]
        gcasa={}
        gfuera={}
        gall={}

        #Goles Local
        fi=open('infotxt/goleslocal.txt', 'r')
        info = [ i for i in fi]
        for i in fi:
            info.append(i)
        fi.close()

        cont=0
        for i in info:
            temp=i.split('\t')        
            if not cont:
                eq=temp[0]
                aux=[]
                aux=[j for j in temp if j!=temp[0] and j!='\n' and j!=temp[2]]
                cont=1
            else:
                for j in temp:
                    if j!='':
                        aux.append(j)
                if cont==1:
                    gcasa[eq]=aux[:]
                    gcasa[eq][6]=gcasa[eq][6][:-1]
                    cont=0
                    aux.clear()
            
        info.clear()
        #Goles Visitante
        fi=open('infotxt/golesvisitante.txt', 'r')
        for i in fi:
            info.append(i)
        fi.close()

        cont=0
        for i in info:
            temp=i.split('\t')

            if not cont:
                eq=temp[0]
                aux=[]
                aux=[j for j in temp if j!=temp[0] and j!='\n' and j!=temp[2]]
                cont=1
            else:
                for j in temp:
                    if j!='':
                        aux.append(j)
                if cont==1:
                    gfuera[eq]=aux[:]
                    gfuera[eq][6]=gfuera[eq][6][:-1]
                    cont=0
                    aux.clear()
    
        info.clear()
        #Goles Total
        fi=open('infotxt/golestotal.txt', 'r')
        for i in fi:
            info.append(i)
        fi.close()

        cont=0
        for i in info:
            temp=i.split('\t')

            if not cont:
                eq=temp[0]
                aux=[]
                aux=[j for j in temp if j!=temp[0] and j!='\n' and j!=temp[2]]
                cont=1
            else:
                for j in temp:
                    if j!='':
                        aux.append(j)
                if cont == 1:
                    gall[eq]=aux[:]
                    gall[eq][6]=gall[eq][6][:-1]
                    cont=0
                    aux.clear()

        self.goleslocal=gcasa
        self.golesvisitante=gfuera
        self.golestotal=gall
        
# Metodos get para las variables asignadas tras la ejecucion del metodo goles
    def get_golesLocal(self):
        return self.goleslocal
    def get_golesVisitante(self):
        return self.golesvisitante
    def get_golesTotal(self):
        return self.golestotal

    #Metodo que recoge la informacion en first.txt para establecer los valores de
    # - casa, fuera, empates0
    def procesar_primero(self):
        fi=open('infotxt/first.txt', 'r')
        info = [i for i in fi]
        fi.close()
        
        casa={}
        fuera={}
        for i in info:            
            temp2=i.split("\t")
            temp=[i for i in temp2 if i!=' ' and i!='  ' and i!='']
            for i in temp:
                casa[temp[0]]=[temp[1:6]]
                fuera[temp[0]]=[temp[6], temp[7], temp[8], temp[9], temp[10]]

        empates={}
        for i in self.ratios:
            k=i[1:]
            empates[i]=int(casa[k][0][1])+int(fuera[k][1])
            
        self.casa=casa
        self.fuera=fuera        
        self.empates0=empates       

# Metodos get para las variables asignadas tras la ejecucion del metodo primero
    def get_casa(self):
        return self.casa
    def get_fuera(self):
        return self.fuera
    def get_empates0(self):
        return self.empates0

    #Metodo que recoge la informacion en marcaprimero.txt para establecer los valores de
    # - marcaprimero
    def procesar_marcaprimero(self):
        info=[]
        victoria_primero={}
        fi=open('infotxt/marcaprimero.txt', 'r')
        for i in fi:
            info.append(i)
        fi.close()
        for i in info:
            temp2=i.split("\t")
            temp=[i for i in temp2 if i!=' ' and i!='  ' and i!='']
            victoria_primero[temp[0][1:-1]]=[temp[3], temp[4], temp[5]]
        
        self.marcaprimero=victoria_primero

    #Metodo que recoge la informacion en encajaprimero.txt para establecer los valores de
    # - encajaprimero
    def procesar_encajaprimero(self):
        encaja_primero={}
        fi=open('infotxt/encajaprimero.txt', 'r')
        info = [i for i in fi]
        fi.close()
        for i in info:
            temp2=i.split("\t")
            temp=[i for i in temp2 if i!=' ' and i!='  ' and i!='']        
            encaja_primero[temp[0][1:-1]]=[temp[3], temp[4], temp[5]]

        self.encajaprimero=encaja_primero

# Metodos get para las variables asignadas tras la ejecucion de los metodos marcaprimero y encajaprimero
    def get_marcaPrimero(self):
        return self.marcaprimero
    def get_encajaPrimero(self):
        return self.encajaprimero
   
# Metodo que establece los valores de los partidos de la siguiente jornada
    def set_siguiente_jornada(self, partidos):
        self.siguiente_jornada=[]
        for i in partidos:
            self.siguiente_jornada.append(i)
       
# Metodo que devuelve la lista de listas de los partidos de la siguiente jornada
    def get_siguiente_jornada(self):
        return self.siguiente_jornada
      
# Metodo que compila la informacion al completo en la instancia actual
    def procesar_todo(self):
        self.procesar_clasificacion()
        self.procesar_timing()
        self.procesar_goles()
        self.procesar_primero()
        self.procesar_marcaprimero()
        self.procesar_encajaprimero()
        self.procesar_ratiomaxmin()
       
# FIN CLASE INFO_LIGA 
#MAIN PARA MOSTRAR
if __name__ == "__main__":
    j=7
    test=info_liga(j)
    test.procesar_todo()

    #Para verificar si los datos se recolectaron correctamente
    
    print ('Valor de la jornada si se ingresa j = x get_jornada')
    print(test.get_jornada())
    print ('\nValor de todos los equipos  get_equipos')
    print(test.get_equipos())
    print ('\nMuestra la clasificacion get_clasif')
    print(test.get_clasif())
    print ('\nMuestra los partidos casa get_partidosCasa')
    print(test.get_partidosCasa())
    print ('\nMuestra los partidos fuera get_partidosFuera')
    print(test.get_partidosFuera())
    print ('\nMuestra la informacion de partidos get_infopartidos')
    print(test.get_infopartidos())
    print ('\nMuestra el timing get_timing')
    print(test.get_timing())
    print ('\nMuestra el timing partes get_timing_partes')
    print(test.get_timing_partes())
    print ('\nMuestra ratios get_ratios')
    print(test.get_ratios())
    print ('\nMuestra ratios partes get_ratios_partes')
    print(test.get_ratios_partes())
    print ('\nMuestra maximo r get_maximoR')
    print(test.get_maximoR())
    print ('\nMuestra minimo r get_minimoR')
    print(test.get_minimoR())
    print ('\nMuestra goles local get_golesLocal')
    print(test.get_golesLocal())
    print ('\nMuestra goles visitante get_golesVisitante')
    print(test.get_golesVisitante())
    print ('\nMuestra goles total get_golesTotal')
    print(test.get_golesTotal())
    print ('\nMuestra casa get_casa')
    print(test.get_casa())    
    print ('\nMuestra fuera get_fuera ')
    print(test.get_fuera())
    print ('\nMuestra empates get_empates0 ')
    print(test.get_empates0())
    print ('\nMuestra marca primero get_marcaPrimero')
    print(test.get_marcaPrimero())
    print ('\nMuestra encaja primero get_encajaPrimero')
    print(test.get_encajaPrimero())
    print ('\nMuestra siguiente jornada get_siguiente_jornada')
    print(test.get_siguiente_jornada())
 
