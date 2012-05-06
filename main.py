# coding=UTF-8

from time import sleep
import os
import csv
from funciones import *

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

def RepDot(lista_de_dotes,dtD):
    lasdotes = []
    nom = lista_de_dotes[0]
    pre = lista_de_dotes[1]
    des = lista_de_dotes[2]
    ldt = []
    while dtD > 0:
        dt = input('Dote: ').rstrip(' ').capitalize()
        while dt not in nom:
            print ('Por favor, escribe la dote correctamente\n')
            dt = input('Dote: ').rstrip(' ').capitalize()
        if input('\n¿Desea conocer información sobre esta dote?\n').lower().startswith('s'):
                print('\nPrerrequisitos: '+pre[nom.index(dt)]+'\n'+des[nom.index(dt)])
        if input('\n¿Esta seguro?').lower().startswith('s'):
            if nom.index(dt) in lasdotes:
                if nom.index(dt) in dt_S:
                    dtD -=1
                    lasdotes.append(dotes.index(dt))
                    ldt.append(dt)
                elif nom.index(dt) in dt_ns:
                    print ('Puedes elegir esta dote multiples veces, pero sus efectos no se apilan')
                else:
                    print ('No puedes elegir esa dotes dos veces, elige otra\n')
            else:
                dtD -=1
                lasdotes.append(nom.index(dt))
                ldt.append(dt)
    return lasdotes,ldt

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
    print('Sus nuevas tiradas son: '+PrepPrint(tirs))

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

print('\nNiveles de clase')
clases = SelCla(nv_pj)
proc = ProCla(clases)
ATKbase = proc[0]
Fortbase = proc[1]
Refbase = proc[2]
Volbase = proc[3]

print ('\nReparte tus puntuaciones de característica')
for Car in Cars:
    CARS[Cars.index(Car)]=RepPunto(tirs,Car)

lasclases = []
temp = []
for cla in clases:
        if cla not in lasclases:
            if cla == 'Brb':clase = 'Bárbaro'
            elif cla == 'Brd':clase = 'Bardo'
            elif cla == 'Clr':clase = 'Clérigo'
            elif cla == 'Drd':clase = 'Druida'
            elif cla == 'Exp':clase = 'Explorador'
            elif cla == 'Gue':clase = 'Guerrero'
            elif cla == 'Hcr':clase = 'Hechicero'
            elif cla == 'Mag':clase = 'Mago'
            elif cla == 'Mnj':clase = 'Monje'
            elif cla == 'Pld':clase = 'Paladín'
            elif cla == 'Pcr':clase = 'Pícaro'
            if clase not in temp:
                lasclases.append(clase)

## A partir de este punto, clases contiene la lista corta 'gue','gue','mag'
## mientras que lasclases contiene la lista con el nombre completo: 'Guerrero','Guerrero','Mago'

## Aumento de Características ##
os.system(['clear','cls'][os.name == 'nt'])
if nv_pj >= 4:
    print ('Tu personaje es de nivel superior a 4. Tienes'+round(nv_pj/4)+' aumentos de características')
    for i in range(1, nv_pj+1):
        if i%4==0:
            punt = 1
            for Car in Cars:
                inpunt = input (Car+' '+str(CARS[Cars.index(Car)])+'+')
                while int(inpunt) > punt:
                    print ('No dispones de esos puntos')
                    inpunt = input (Car+' '+str(CARS[Cars.index(Car)])+'+')
                while int(inpunt) < 0:
                    print ('No puedes restar puntos')
                    inpunt = input (Car+' '+str(CARS[Cars.index(Car)])+'+')
                if int(inpunt) > 0:
                    CARS[Cars.index(Car)] += punt
                    punt -= 1


fFUE = CARS[0]+Raza[0][0]
fDES = CARS[1]+Raza[0][1]
fCON = CARS[2]+Raza[0][2]
fINT = CARS[3]+Raza[0][3]
fSAB = CARS[4]+Raza[0][4]
fCAR = CARS[5]+Raza[0][5]

os.system(['clear','cls'][os.name == 'nt'])
if nv_pj > 4:
    print('Tus puntuaciones de característica finales son:')
    for Car in Cars:
        print (Car+' '+str(CARS[Cars.index(Car)]+Raza[0][Cars.index(Car)]))

FUE_mod = CarMod(fFUE)
DES_mod = CarMod(fDES)
CON_mod = CarMod(fCON)
INT_mod = CarMod(fINT)
SAB_mod = CarMod(fSAB)
CAR_mod = CarMod(fCAR)
                
PHs = PuntosHab(INT_mod,clases)
DotesNivel = DtsNivel(clases)
velocidad = Raza[4]

Iniciativa = DES_mod
ATKFinalCC = ATKbase + FUE_mod
ATKFinalAD = ATKbase + DES_mod
Presa = ATKbase + FUE_mod + tam_pres
Fort = Fortbase + CON_mod
Ref = Refbase + DES_mod
Vol = Volbase + SAB_mod
PG = PG(CON_mod,clases)

if Raza[2] == 'humano':
    for i in PHs:
        if PHs.index(i) == 0:
            PHs[PHs.index(i)]+=4
        else:
            PHs[PHs.index(i)]+=1
elif Raza[2] == 'mediano':
    Fort += 1
    Ref += 1
    Vol += 1
#########################################3
        
temp = list(range(len(PHs)))
for i in temp:
    PH = PHs[i]
    os.system(['clear','cls'][os.name == 'nt'])
    print('\nTienes '+str(PH)+' puntos de habilidad para distribuir en este nivel.\n')
    b = ''
    if input('Deseas conocer tus habilidades de clase? ('+lasclases[temp.index(i)]+')\n').lower().startswith('s'):
        for hab in claseas(clases[temp.index(i)]):
            b = b+hab+', '
        print(b.rstrip(', ')+'.\n')

    print ('Recuerda que cualquier habildiad transclásea cuesta dos puntos en lugar de uno.\nEscribe una habilidad y los puntos que desees invertir en ella.\n')

    rng_max = nv_pj+3
    rng_max_tc = round(rng_max/2)
    while PH > 0:
        hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        while hab not in habs:
            print('Por favor, escribe la habilidad correctamente')
            hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        if rng[habs.index(hab)] > 0:
            print (hab+' ya posee '+str(rng[habs.index(hab)])+' rangos.')
        puntos = input('Puntos: ')
        while not puntos.isnumeric():
            print ('Los rangos deben ser numéricos')
            puntos = input('Puntos: ')
        while int(puntos) > PH:
            print('No posees tantos puntos de habilidad')
            puntos = input('Puntos: ')
        puntos = int(puntos)
        
        clase = clases[i]
        if hab not in claseas(clase):
            PH -= puntos
            rng[habs.index(hab)] += puntos/2
            print('\nPuntos restantes: '+str(PH))
            if PH < 0:
                print('no alcanzan los puntos')
                PH += puntos*2
                rng[habs.index(hab)] -= puntos/2
        else:
            if rng[habs.index(hab)] + puntos > rng_max:
                print(hab+' ha alcanzado el rango máximo ('+str(rng_max)+').')
                PH -= rng_max
                rng[habs.index(hab)] += rng_max
                print('\nPuntos restantes: '+str(PH))
                if PH < 0:
                    print('no alcanzan los puntos')
                    PH += rng_max
                    rng[habs.index(hab)] -= rng_max
            else:
                PH -= puntos
                rng[habs.index(hab)] += puntos
                print('\nPuntos restantes: '+str(PH))
                if PH < 0:
                    print('no alcanzan los puntos')
                    PH += puntos
                    rng[habs.index(hab)] -= puntos

print('\nElige dotes')
if Raza[2] == 'humano':
    dotes = RepDot (DOTES,DotesNivel+1)
else:
    dotes = RepDot (DOTES,DotesNivel)

# Aplicar modificadores
# Raciales
for r in raciales:
    rcl[r[0]]+=r[1]

# Por Dotes
for d in dotes[0]:
    if d in dt_hab:
        for i in dt_hab[d]:
            dts[i]+=2

# Por Objetos
## aún no implementado

# Por sinergías
for r in rng:
    if rng.index(r) in hab_sin:
        for i in hab_sin[rng.index(r)]:
            sng[i]+=2

# Ordenar las habilidades que se van a imprimir
temp = []
t = -1
imprimir = ''

# Rangos de habilidad
for r in rng:
    t+=1
    if rng[t]>0:
        if habs[t] not in temp:
            temp.append(habs[t])

# Bonificadores raciales
t = -1
for r in rcl:
    t+=1
    if rcl[t]>0:
        if habs[t] not in temp:
            temp.append(habs[t])

# Bonificadores de sinergia
t = -1
for r in sng:
    t+=1
    if sng[t]>0:
        if habs[t] not in temp:
            temp.append(habs[t])

# Bonificadores por dotes
t = -1
for r in dts:
    t+=1
    if dts[t]>0:
        if habs[t] not in temp:
            temp.append(habs[t])

temp.sort()

# Eliminar las habilidades 'solo entrenadas' sin rangos
for h in temp:
    if rng[habs.index(h)] == 0:
        if habs.index(h) in hab_n_E:
            del temp[temp.index(h)]

for h in temp:
    imprimir = imprimir+h+' +'+str(HabMod(hab_mods,habs.index(h),FUE_mod,DES_mod,CON_mod,INT_mod,SAB_mod,CAR_mod))+', '
imprimir = imprimir.rstrip(', ')+'.'

#Output
if input('Deseas Guardar este personaje?\n').lower().startswith('s'):
    nombre = input('\nNombre: ').capitalize()
    Pj = open('Personajes/'+nombre+'.txt','w')
    Pj.write('Nombre: '+nombre+'\n')
    Pj.write('Tipo y Tamaño: Humanoide '+tam_nom+' ('+subtipo+')\n')
    Pj.write('DG: '+PG[1]+' ('+str(PG[0])+' pg)\n')
    Pj.write('Iniciativa: +'+str(Iniciativa)+'\nVelocidad: '+velocidad+'\n\n')
    Pj.write("Ataque base: +"+str(ATKbase)+"\nPresa: +"+str(Presa)+"\n\nE/A: 5'/5'.\n\n\n")
    Pj.write('TS: Fortaleza +'+str(Fort)+', Reflejos +'+str(Ref)+', Voluntad +'+str(Vol)+'\n')
    Pj.write('Características: Fuerza '+str(fFUE)+', Destreza '+str(fDES)+', Constitución '+str(fCON)+', Inteligencia '+str(fINT)+', Sabuduría ' + str(fSAB)+', Carisma '+str(fCAR)+'.\nHabilidades y Dotes: '+imprimir+' '+PrepPrint(dotes[1]))
    sleep(3)
    print('\nPersonaje Guardado')
    Pj.close()
print ('Gracias')
sleep (2)
