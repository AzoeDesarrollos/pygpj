# coding=UTF-8

from time import sleep
import os
import csv
from func import *

csv.register_dialect('myCSV',delimiter=';')

# Set Up
def leerCSV (archivo):
    arch = csv.reader(open(archivo),dialect='myCSV')
    temp = []
    for t in arch:
        temp.append(t)
    if len(temp) == 1:
        temp = temp[0]
    return temp

def claseas (clase):
    hab_cls = {'Brb':(1,14,17,20,22,36,38,40,41),'Brd':(1,2,5,6,7,8,9,10,11,12,13,14,16,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,39,41),'Clr':(1,5,6,8,23,26,30,32,35,37),'Drd':(1,3,5,6,8,14,20,22,23,33,37,38,40,44),'Exp':(1,3,4,5,13,14,20,21,22,23,28,29,33,36,37,38,40,41,43,44),'Gue':(1,17,20,22,23,36,40,41),'Hcr':(1,5,6,10,23,26),'Mag':(1,5,6,7,23,26,27,28,29,30,31,32,33,34,35),'Mnj':(1,2,3,5,8,11,12,13,14,16,21,22,23,24,26,35,36,41),'Pld':(1,2,5,8,20,23,34,35,37,40),'Pcr':(0,1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,31,36,39,41,42,43)}
    cls = []
    for i in hab_cls[clase]:
        cls.append(habs[i])
    return cls

def HabMod(mods,hab_num,FUE,DES,CON,INT,SAB,CAR):
    mod = 0
    temp = mods[hab_num]
    if temp == 'FUE': mod = FUE
    elif temp == 'DES': mod = DES
    elif temp == 'CON': mod = CON
    elif temp == 'INT': mod = INT
    elif temp == 'SAB': mod = SAB
    elif temp == 'CAR': mod = CAR
    return rng[hab_num]+mod+rcl[hab_num]+sng[hab_num]+dts[hab_num]+obj[hab_num]
    
Cars = ['Fuerza','Destreza','Constitución','Inteligencia','Sabiduría','Carisma']
CARS = [0,0,0,0,0,0]

DOTES = leerCSV('data/dotes.csv')
habs = leerCSV('data/habs.csv')
hab_mods = leerCSV('data/mods.csv')

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
tirs = GenTir()
print('Sus tiradas son: '+PrepPrint(tirs))
sleep (2)
while input ('Desea tirar de nuevo?\n').lower().startswith('s'):
    os.system(['clear','cls'][os.name == 'nt'])
    tirs = GenTir()
    print('Sus tiradas son: '+PrepPrint(tirs))

print('\nSeleccione Raza (humano, enano, elfo, gnomo, mediano, semielfo o semiorco)\n')
Raza = SelRaza()
subtipo = Raza[2]
tam_nom = Raza[1]
tam_mod = tamaño[tam_nom][0]
tam_pres = tamaño[tam_nom][1]
tam_esc = tamaño[tam_nom][2]
raciales = Raza[3]

nv_pj = input('\nNivel del personaje?: ')
while not nv_pj.isnumeric():
    print ('\nEl nivel debe ser un NUMERO entre 1 y 20')
    nv_pj = input('\nNivel del personaje?: ')
nv_pj = int(nv_pj)

cla = [] ## ['Gue', '', 'Mag']
clases = [] ## ['Gue', 'Gue', 'Mag']
lasclases = [] ## ['Guerrero', 'Guerrero', 'Mago']
dotes = []

print ('\nReparte tus puntuaciones de característica')
for Car in Cars:
    CARS[Cars.index(Car)]=RepPunto(tirs,Car)

for nivel in range(1,nv_pj+1):
    os.system(['clear','cls'][os.name == 'nt'])
    print ('~~ '+str(nivel)+'º NIVEL ~~\n')
    ## elija clase
    print ('Elije una clase para este nivel')
    cla.append(SelCla())
    if nivel %4==0: ## Aumento de Características en niveles multiplos de 4
        print ('\nEn el '+str(nivel)+'º nivel, tienes un aumento de características')
        print ('Selecciona la característica que quieres aumentar')
        Car = input('Característica: ').capitalize()
        while Car.capitalize() not in Cars:
            print ('La característica es inválida o inexistente')
            Car = input('Característica: ').capitalize()
        CARS[Cars.index(Car)]+=1
        print ('El personaje tiene ahora '+Car+' '+str(CARS[Cars.index(Car)])+' (+'+str(CarMod(CARS[Cars.index(Car)]))+')')
    if nivel ==1:## Elección de Dote en nivel 1
        print ('\nEn el '+str(nivel)+'º nivel, tienes una dote para elegir')
        dotes.append(SelDot(DOTES))
    elif nivel %3==0: ## Elección de Dotes en niveles multiplos de 3
        print ('\nEn el '+str(nivel)+'º nivel, tienes una dote para elegir')
        dotes.append(SelDot(DOTES))

for i in range(len(cla)):
    if cla[i] != '':
        clases.append(cla[i])
    else:
        clases.append(clases[i-1])

proc = ProCla(clases)
ATKbase = proc[0]
Fortbase = proc[1]
Refbase = proc[2]
Volbase = proc[3]

for Car in Cars:
    CARS[Cars.index(Car)]+Raza[0][Cars.index(Car)] 

FUE_mod = CarMod(CARS[0])
DES_mod = CarMod(CARS[1])
CON_mod = CarMod(CARS[2])
INT_mod = CarMod(CARS[3])
SAB_mod = CarMod(CARS[4])
CAR_mod = CarMod(CARS[5])