# coding=UTF-8

from time import sleep
import os
from setup import *
from func import *
from procs import *
from sels import *

# barra = ''.join((Raza[0],'| FUE '+str(CARS[0]),' DES '+str(CARS[1]),' CON '+str(CARS[2]),' INT '+str(CARS[3]),' SAB '+str(CARS[4]),'| Al '+alinis[alini]))

while True:
    nivel += 1
    if nivel == 1:
        ## Inicio ##
        tirs = GenTir()
        op = SelTirs(tirs)
        while op == False:
            tirs = GenTir()
            op = SelTirs(tirs)
        
        ## Seleccionar Raza ##
        Raza = SelRaza(RAZAS)
        subtipo = Raza[3]
        tam_nom = Raza[2]
        tam_mod = tamaño[tam_nom][0]
        tam_pres = tamaño[tam_nom][1]
        tam_esc = tamaño[tam_nom][2]
        raciales = Raza[4]
        
        ## Repartir puntuaciones de característica y aplicar mods. raciales ##
        print ('\nReparte tus puntuaciones de característica')
        for Car in Cars:
            CARS[Cars.index(Car)]=RepPunto(tirs,Car)

        for Car in Cars:
            CARS[Cars.index(Car)]+Raza[1][Cars.index(Car)]
        
        CARS_mods = [CarMod(CARS[0]),CarMod(CARS[1]),CarMod(CARS[2]),CarMod(CARS[3]),CarMod(CARS[4]),CarMod(CARS[5])]

        ## Elección de Alineamiento ##
        alini = Alinear()
    
    # os.system(['clear','cls'][os.name == 'nt'])
    # print (barra)
    print ('\n~~ '+str(nivel)+'º NIVEL ~~\n')
    
    ## Elección de Clase ##
    if nivel == 1:
        clase = SelCla('',CLASES,alini)
    else:
        clase = SelCla(lasclases[nivel-2],CLASES,alini)
    compW = Competencias (ARMAS,clase,compW)
    compA = Competencias (ARMDS,clase,compA)
    cla.append(clase)
    lasclases.append(CLASES[5][CLASES[0].index(clase)])
    for i in range(len(cla)):
        if cla[i] == '':
            cla[i] = cla[i-1]
    stats = ProCla(CLASES,clase,cla.count(clase),stats)
    
    for aptitud in AppClas (APPS,clase,cla.count(clase)):
        nuevas.append(aptitud)
        for ap in nuevas:
            e = ProcMecApp(APs_mc,ap,apps)
            if e == 'd':
                dotes.append(SelDot(nivel,DOTES,compW,ARMAS[0],HABS[0],True,clase,dt_cls))
            elif e == 'x':
                e = SelAE (APs_mc,apps)
                if e == 'd':
                    dotes.append(SelDot(nivel,DOTES,compW,ARMAS[0],HABS[0],False,clase,dt_cls))
                else:
                    aprin.append(e)
            elif e == 'a':
                dotes.append(str(DOTES[0].index(ap)))
            else:
                aprin.append(e)
        apps.append(aptitud) # Recuerda, luego, calcular los índices: APs_mc[0].index(aptitud)
        nuevas = []
    ## Aumento de Características en niveles multiplos de 4 ##
    if nivel % 4 == 0:
        CARS[Car]+=1
        print ('El personaje tiene ahora '+Cars[Car]+' '+str(CARS[Car])+' (+'+str(CarMod(CARS[Car]))+')')
        sleep (2)
    
    ## Cáculo de puntos y Asignación de Rangos de habilidad ##
    # os.system(['clear','cls'][os.name == 'nt'])
    # print (barra)
    hab_rng = RepRNG (PuntHab (CLASES,clase,nivel,CARS_mods[3],subtipo),cla.count(clase),Claseas(hab_cls,clase,HABS[0]),HABS[0],rng)
    for i in hab_rng:
        rng[HABS[0].index(i)] = hab_rng[i]
    
    ## Elección de Dotes ##
    if nivel in (1,3,6,9,12,15,18):
        #os.system(['clear','cls'][os.name == 'nt'])
        # print (barra)
        dotes.append(SelDot(nivel,DOTES,compW,ARMAS,HABS[0],False,clase,dt_cls))
        
    if not input('\nDesea subir de nivel? ').lower().startswith('s'):
        break
