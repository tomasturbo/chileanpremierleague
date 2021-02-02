#!/usr/bin/env python
# coding: utf-8

# In[242]:


import pandas as pd
import numpy as np
df1 = pd.read_excel('C:\\Users\\tomaa\\Desktop\\Tomás\\Fútbol chileno.xlsx', sheet_name='2019')
df2 = pd.read_excel('C:\\Users\\tomaa\\Desktop\\Tomás\\Fútbol chileno.xlsx', sheet_name='2020')
df3 = pd.read_excel('C:\\Users\\tomaa\\Desktop\\Tomás\\Fútbol chileno.xlsx', sheet_name='Partidos')
df_1 = df1.to_numpy()
df_2 = df2.to_numpy()
df_3 = df3.to_numpy()

class Equipo:
    def __init__(self,nombre,pj_19=0,pj_20=0,puntos_19=0,puntos_20=0,promedio=0,ganados=0,empatados=0,perdidos=0,diferencia=0):
        self.nombre=nombre
        self.partidos_jugados_2019=pj_19
        self.partidos_jugados_2020=pj_20
        self.puntos_2019=puntos_19
        self.puntos_2020=puntos_20
        self.promedio=promedio
        self.ganados=ganados
        self.empatados=empatados
        self.perdidos=perdidos
        self.diferencia=diferencia

class Partido:
    def __init__(self,local,visita,goles_local=0,goles_visita=0,fecha=0):
        self.local=local
        self.visita=visita
        self.goles_local=goles_local
        self.goles_visita=goles_visita
        self.fecha=fecha
        
equipos=[]
for i in range(18):
    equipo=Equipo(df_2[i][1],0,df_2[i][2],0,df_2[i][3],0,df_2[i][4],df_2[i][5],df_2[i][6],df_2[i][7])
    if equipo.nombre != "Wanderers" and equipo.nombre != "La Serena":
        for j in range(16):
            if equipo.nombre == df_1[j][1]:
                equipo.partidos_jugados_2019=df_1[j][2]
                equipo.puntos_2019=df_1[j][3]
    
    if equipo.nombre=="Wanderers" or equipo.nombre=="La Serena":
        equipo.promedio=equipo.puntos_2020/equipo.partidos_jugados_2020
    else:
        equipo.promedio=(equipo.puntos_2019/equipo.partidos_jugados_2019)*0.6 + (equipo.puntos_2020/equipo.partidos_jugados_2020)*0.4
    
    equipos.append(equipo)
    
partidos=[]
for i in range(32):
    for equipo in equipos:
        if df_3[i][0]==equipo.nombre:
            locals=equipo
        if df_3[i][3]==equipo.nombre:
            visitass=equipo
    partido=Partido(locals,visitass,goles_local=0,goles_visita=0,fecha=0)
    partidos.append(partido)

#(self,local,visita,goles_local=0,goles_visita=0,fecha=0)
for i,partido in enumerate(partidos):
    partido.goles_local=df_3[i][1]
    partido.goles_visita=df_3[i][2]
    partido.fecha=int(df_3[i][4])
    
for partido in partidos:
    if np.isnan(partido.goles_local) == False and np.isnan(partido.goles_visita) == False:
        partido.local.partidos_jugados_2020+=1
        partido.visita.partidos_jugados_2020+=1
        if partido.goles_local > partido.goles_visita:
            partido.local.puntos_2020+=3
            partido.local.ganados+=1
            partido.visita.perdidos+=1
            partido.local.diferencia=partido.local.diferencia+partido.goles_local-partido.goles_visita
            partido.visita.diferencia=partido.visita.diferencia-partido.goles_local+partido.goles_visita
        
        elif partido.goles_local < partido.goles_visita:
            partido.visita.puntos_2020+=3
            partido.visita.ganados+=1
            partido.local.perdidos+=1
            partido.local.diferencia=partido.local.diferencia+partido.goles_local-partido.goles_visita
            partido.visita.diferencia=partido.visita.diferencia-partido.goles_local+partido.goles_visita
        else:
            partido.local.puntos_2020+=1
            partido.visita.puntos_2020+=1
            partido.local.empatados+=1
            partido.visita.empatados+=1
            
for equipo in equipos:
    if equipo.nombre=="Wanderers" or equipo.nombre=="La Serena":
        equipo.promedio=equipo.puntos_2020/equipo.partidos_jugados_2020
    else:
        equipo.promedio=(equipo.puntos_2019/equipo.partidos_jugados_2019)*0.6 + (equipo.puntos_2020/equipo.partidos_jugados_2020)*0.4

gua = sorted(equipos,reverse=True,key=lambda x: x.promedio)
gua2 = sorted(equipos,reverse=True,key=lambda x: (x.puntos_2020,x.diferencia,x.ganados))
tabla_pond = []
tabla = []
for i in range(18):
    aux=[]
    aux2=[]
    aux.append(i+1)
    aux2.append(i+1)
    aux.append(gua[i].nombre)
    aux2.append(gua2[i].nombre)
    aux.append(round(gua[i].promedio,4))
    aux2.append(gua2[i].partidos_jugados_2020)
    aux2.append(gua2[i].ganados)
    aux2.append(gua2[i].empatados)
    aux2.append(gua2[i].perdidos)
    aux2.append(gua2[i].diferencia)
    aux2.append(gua2[i].puntos_2020)
    
    tabla.append(aux2)
    tabla_pond.append(aux)

tabla_ponderada=pd.DataFrame(tabla_pond,columns=["Posición","Equipo","Promedio"])
tabla_normal=pd.DataFrame(tabla,columns=["Posición","Equipo","Jugados","Ganados","Empatados","Perdidos","Diferencia","Puntos"])
print(tabla_normal)
print("\n",tabla_ponderada)

