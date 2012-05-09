﻿# coding=UTF-8

from time import sleep
import os
import csv
from func import *

csv.register_dialect('myCSV',delimiter=';')

# Set Up
Cars = ['Fuerza','Destreza','Constitución','Inteligencia','Sabiduría','Carisma']
CARS = [0,0,0,0,0,0]

DOTES = leerCSV('data/dotes.csv')
habs = leerCSV('data/habs.csv')
hab_mods = leerCSV('data/mods.csv')
CLASES = leerCSV('data/clases.csv')
APPS = ProcApps(leerCSV('data/apps.csv'))

rng = [i*0 for i in range(len(habs))] # Rangos de habilidad
dts = [i*0 for i in range(len(habs))] # Bonificadores por dotes
rcl = [i*0 for i in range(len(habs))] # Bonificadores raciales
sng = [i*0 for i in range(len(habs))] # Bonificadores de sinergía
obj = [i*0 for i in range(len(habs))] # Bonificadores por objetos

dt_S = [51,57]
dt_ns = [26,27,41,69,86,87,88,89]
dt_gue = [8,9,10,11,12,13,17,18,19,20,21,22,23,24,25,26,34,41,43,44,45,46,47,48,49,50,52,53,54,60,61,62,63,64,65,68,72,73,74,75,76,79,80,82,83,84,85,89]
dt_hab = {1:[24,36],14:[22,41],16:[37,38],2:[20,40],3:[11,12],42:[0,18],52:[9,15],58:[6,42],6:[3,14],66:[4,25],7:[7,39],70:[19,43],71:[2,8],77:[10,17],82:[13,21]}
hab_sin = {1:[39],2:[8],10:[8,9,17,19],6:[42],12:[43],24:[11,36],26:[6],27:[4],28:[38],29:[38],31:[25],32:[38],33:[38],34:[8],31:[25],37:[24],40:[44,20],37:[24]}
hab_n_E = [0,6,7,17,20,21,25,26,28,29,30,31,32,33,34,35,40,42,44]

tamaño = {'Minúsculo':(+8,-16,+16),'Diminuto':(+4,-12,+12),'Menudo':(+2,-8,+8),'Pequeño':(+1,-4,+4),'Mediano':(+0,+0,+0),'Grande':(-1,+4,-4),'Enorme':(-2,+8,-8),'Gargantuesco':(-4,+12,-12),'Colosal':(-8,+16,-16)}

#Inicio#
print('Sus tiradas son: '+GenTir())
sleep (2)
while input ('Desea tirar de nuevo?\n').lower().startswith('s'):
    os.system(['clear','cls'][os.name == 'nt'])
    print('Sus tiradas son: '+GenTir())

print('\nSeleccione Raza (humano, enano, elfo, gnomo, mediano, semielfo o semiorco)\n')
Raza = SelRaza()
subtipo = Raza[2]
tam_nom = Raza[1]
tam_mod = tamaño[tam_nom][0]
tam_pres = tamaño[tam_nom][1]
tam_esc = tamaño[tam_nom][2]
raciales = Raza[3]

print ('\nReparte tus puntuaciones de característica')
for Car in Cars:
    CARS[Cars.index(Car)]=RepPunto(tirs,Car)
    
for Car in Cars:
    CARS[Cars.index(Car)]+Raza[0][Cars.index(Car)]

FUE_mod = CarMod(CARS[0])
DES_mod = CarMod(CARS[1])
CON_mod = CarMod(CARS[2])
INT_mod = CarMod(CARS[3])
SAB_mod = CarMod(CARS[4])
CAR_mod = CarMod(CARS[5])

CARS_MODS = [FUE_mod,DES_mod,CON_mod,INT_mod,SAB_mod,CAR_mod]

nv_pj = input('\nNivel del personaje?: ')
while not nv_pj.isnumeric():
    print ('\nEl nivel debe ser un NUMERO entre 1 y 20')
    nv_pj = input('\nNivel del personaje?: ')
nv_pj = int(nv_pj)

cla = [] ## ['Gue', '', 'Mag']
lasclases = [] ## ['Guerrero', 'Guerrero', 'Mago']
dotes = []
stats = [0,0,0,0]

for nivel in range(1,nv_pj+1):
    os.system(['clear','cls'][os.name == 'nt'])
    print ('~~ '+str(nivel)+'º NIVEL ~~\n')
    ## Elegir Clase ##
    if nivel == 1:
        clase = SelCla('')
    else:
        clase = SelCla(lasclases[nivel-2])
    cla.append(clase)
    lasclases.append(CLASES[5][CLASES[0].index(clase)])
    for i in range(len(cla)):
        if cla[i] == '':
            cla[i] = cla[i-1]
    for i in range(4):
        stats[i] += ProCla(CLASES,clase,cla.count(clase))[i]
    
    ## Aumento de Características en niveles multiplos de 4 ##
    if nivel %4==0: 
        print ('\nEn el '+str(nivel)+'º nivel, tienes un aumento de características')
        print ('Selecciona la característica que quieres aumentar')
        Car = input('Característica: ').capitalize()
        while Car.capitalize() not in Cars:
            print ('La característica es inválida o inexistente')
            Car = input('Característica: ').capitalize()
        CARS[Cars.index(Car)]+=1
        print ('El personaje tiene ahora '+Car+' '+str(CARS[Cars.index(Car)])+' (+'+str(CarMod(CARS[Cars.index(Car)]))+')')
    
    ## Cáculo de puntos y Asignación de Rangos de habilidad ##
    hab_rng = RepRNG (PuntHab (CLASES,clase,nivel,INT_mod,subtipo),cla.count(clase),Claseas(clase),habs)
    for i in hab_rng:
        rng[habs.index(i)] += hab_rng[i]
    
    ## Elección de Dotes ##
    dotes.append(SelDot(DOTES,nivel))