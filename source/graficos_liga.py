#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Autor: Esperanza Ramirez Armijos
@Tema: Pronosticador del Futbol Ecuatoriano
@Descripcion: Genere el archivo de respuesta html, la información contenida en una instancia de la clase info_liga
'''

import recoleccion_info
import matplotlib.pyplot as plt
import numpy as np
import os

# CLASE GRAFICOS_LIGA  
class graficos_liga:
    #Constructor que toma un objeto info_liga basico (jornada ya establecido), procesa todo la info para ese objeto y establece el valor de vmax
    def __init__(self, info_liga_obj):
        self.info_liga=info_liga_obj
        self.info_liga.procesar_todo()
        self.graficos_ratios={}
        self.graficos_resultados={}
        self.graficos_primero={}
        vmax=0
        clasif=self.info_liga.get_clasif()
        for i in clasif:
            if int(clasif[i][3])>vmax:
                vmax=int(clasif[i][3])
            if int(clasif[i][4])>vmax:
                vmax=int(clasif[i][4])
            if int(clasif[i][5])>vmax:
                vmax=int(clasif[i][5])
        self.vmax=vmax
        
    #Metodo __str__ llamado cuando se realice una llamada a imprimir por pantalla a la variable con la instancia de la clase
    def __str__(self):
        mensaje="Instancia de GRAFICAS para la jornada"+ str(self.info_liga.get_jornada())
        return mensaje        

    def get_instancia_info_liga(self):
        return self.info_liga

    def get_graficosRatios(self):
        return self.graficos_ratios

    #Metodo que para cada equipo genera y guarda el archivo de imagen de su grafica de ratios de goles anotados en intervalos de 10 min
    def set_graficos_ratios_todos_guarda(self, directorio):
        if not os.path.isdir(directorio):
                os.makedirs(directorio)        
        r=self.info_liga.get_ratios()   
        #t=self.info_liga.get_timing()
        maxi=self.info_liga.get_maximoR()
        mini=self.info_liga.get_minimoR()
        tiempos=['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90']
        for i in r:            
            aux=r[i][0:9]
            if len(aux)==9:
                x=range(9)

                plt.plot(x, aux, color='black') #Linea continua negra
                plt.grid(True)
                plt.title(i)
                plt.ylabel("Goles Marcados/Encajados")
                plt.xlabel("Tiempo")
                plt.xticks(x, tiempos, rotation=15)
                plt.ylim(mini, maxi)
             
                plt.savefig(directorio+"/ratio"+i[:-2])
                self.graficos_ratios[i]=plt
                plt.clf()

    #Metodo que para cada equipo genera y guarda el archivo de imagen su grafica de resultados en el directorio dado
    def set_graficos_resultados_todos_guarda(self, directorio):        
        if not os.path.isdir(directorio):
                os.makedirs(directorio)        
        for i in self.info_liga.get_equipos():
            valores=self.info_liga.get_clasif()[i][3:6]
            assert(len(valores)==3)
            ind=np.arange(3)
            r=[int(i) for i in valores]
            t=['Victorias', 'Empates', 'Derrotas']
            plt.bar(ind, r, 0.45, color='g')
            plt.title("Resultados Partidos"+i)
            plt.xticks(ind, t, rotation=-45)
            plt.ylim(0, self.vmax)
            plt.xlim(-0.1, 2.5)                        
            #aux=plt.figure()            
            plt.savefig(directorio+"/resultados"+i[:-2])
            #self.graficos_resultados[i]=plt
            #plt.close()            
            plt.clf()         

    #Metodo que para cada equipo genera y guarda el archivo de imagen de su grafica de porcentajes de partidos en que marca-encaja primero como local y visitante
    def set_grafico_marca_encaja_primero_todos_guarda(self, directorio):        
        if not os.path.isdir(directorio):
            os.makedirs(directorio)        
        c=self.info_liga.get_casa()
        f=self.info_liga.get_fuera()
        for i in self.info_liga.get_equipos():
            valores=[5,10,5,2]
            assert(len(valores)==4)
            ind=np.arange(4)
            r=[int(i) for i in valores]
            t=['Marca 1º\n como Local', 'Encaja 1º\n como Local', 'Marca 1º\n como Visitante', 'Encaja 1º\n como Visitante']
            plt.bar(ind[0:2], r[0:2], 0.35, color='y')
            plt.bar(ind[2:4], r[2:4], 0.35, color='orange')
            plt.xticks(ind, t, rotation=0)
            plt.grid(True)
            plt.title("Marca/Encaja Primero "+i[:-2])
            plt.ylabel("% Partidos")
            plt.ylim(0, 100)
            plt.xlim(-0.2, 3.5)            
            plt.savefig(directorio+"/marcaencaja"+i[:-2])
            #self.graficos_resultados[i]=plt
            plt.clf()

# FIN CLASE GRAFICOS_LIGA 
#MAIN PARA MOSTRAR
if __name__ == "__main__":
    j=7
    il=recoleccion_info.info_liga(j)
    graficas=graficos_liga(il)
