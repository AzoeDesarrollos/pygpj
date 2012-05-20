# coding=UTF-8

from time import sleep
import os
import setup as s
from func import *
from procs import *
from sels import *

# barra = ''.join((Raza[0],'| FUE '+str(CARS[0]),' DES '+str(CARS[1]),' CON '+str(CARS[2]),' INT '+str(CARS[3]),' SAB '+str(CARS[4]),'| Al '+alinis[alini]))

while True:
    s.nivel += 1
    if s.nivel == 1:
        ## Inicio ##
        tirs = GenTir()
        op = SelTirs(tirs)
        while op == False:
            tirs = GenTir()
            op = SelTirs(tirs)
        
        ## Seleccionar Raza ##
        Raza = SelRaza(s.RAZAS)
        subtipo = Raza[3]
        tam_nom = Raza[2]
        tam_mod = s.tamaño[tam_nom][0]
        tam_pres = s.tamaño[tam_nom][1]
        tam_esc = s.tamaño[tam_nom][2]
        raciales = Raza[4]
        
        ## Repartir puntuaciones de característica y aplicar mods. raciales ##
        print ('\nReparte tus puntuaciones de característica')
        for Car in s.Cars:
            s.CARS[s.Cars.index(Car)]=RepPunto(tirs,Car)

        for Car in s.Cars:
            s.CARS[s.Cars.index(Car)]+Raza[1][s.Cars.index(Car)]
        
        CARS_mods = [CarMod(s.CARS[0]),CarMod(s.CARS[1]),
                     CarMod(s.CARS[2]),CarMod(s.CARS[3]),
                     CarMod(s.CARS[4]),CarMod(s.CARS[5])]

        ## Elección de Alineamiento ##
        s.alini = Alinear()
    
    # os.system(['clear','cls'][os.name == 'nt'])
    # print (barra)
    print ('\n~~ '+str(s.nivel)+'º NIVEL ~~\n')
    
    ## Elección de Clase ##
    if s.nivel == 1:
        clase = SelCla('',s.CLASES,s.alini)
    else:
        clase = SelCla(s.lasclases[s.nivel-2],s.CLASES,s.alini)
    s.compW = Competencias (s.ARMAS,clase,s.compW)
    s.compA = Competencias (s.ARMDS,clase,s.compA)
    s.cla.append(clase)
    s.lasclases.append(s.CLASES[5][s.CLASES[0].index(clase)])
    for i in range(len(s.cla)):
        if s.cla[i] == '':
            s.cla[i] = s.cla[i-1]
    s.stats = ProCla(s.CLASES,clase,s.cla.count(clase),s.stats)
    
    for aptitud in AppClas (s.APPS,clase,s.cla.count(clase)):
        s.nuevas.append(aptitud)
        for ap in s.nuevas:
            e = ProcMecApp(s.APs_mc,ap,s.apps)
            if e == 'd':
                s.dotes.append(SelDot(s.nivel,s.dotes,s.DOTES,s.compW,s.ARMAS,s.HABS[0],True,clase,s.dt_cls))
            elif e == 'x':
                e = SelAE (s.APs_mc,s.apps)
                if e == 'd':
                    s.dotes.append(SelDot(s.nivel,s.dotes,s.DOTES,s.compW,s.ARMAS,s.HABS[0],False,clase,s.dt_cls))
                else:
                    s.aprin.append(e)
            elif e == 'a':
                s.dotes.append(str(s.DOTES[0].index(ap)))
            else:
                s.aprin.append(e)
        s.apps.append(aptitud) # Recuerda, luego, calcular los índices: APs_mc[0].index(aptitud)
        s.nuevas = []
    ## Aumento de Características en niveles multiplos de 4 ##
    if s.nivel % 4 == 0:
        Car = AumentaCar(s.nivel)
        s.CARS[Car]+=1
        print ('El personaje tiene ahora '+s.Cars[Car]+' '+str(s.CARS[Car])+' (+'+str(CarMod(s.CARS[Car]))+')')
        input ('\n[Presione Enter para continuar]\n')
    
    ## Cáculo de puntos y Asignación de Rangos de habilidad ##
    # os.system(['clear','cls'][os.name == 'nt'])
    # print (barra)
    hab_rng = RepRNG (PuntHab (s.CLASES,clase,s.nivel,CARS_mods[3],subtipo),
                      s.cla.count(clase),Claseas(s.hab_cls,clase,s.HABS[0]),s.HABS[0],s.rng)
    for i in hab_rng:
        s.rng[s.HABS[0].index(i)] = hab_rng[i]
    
    ## Elección de Dotes ##
    if s.nivel in (1,3,6,9,12,15,18):
        #os.system(['clear','cls'][os.name == 'nt'])
        # print (barra)
        dote = SelDot(s.nivel,s.dotes,s.DOTES,s.compW,s.ARMAS,s.HABS[0],False,clase,s.dt_cls)
        if dote.split(':')[0] in ('26','27'):
            s.compW.append(int(dote.split(':')[1]))
        elif dote.split(':')[0] == '28':
            for i in range(len(s.ARMAS[0])):
                if s.ARMAS[2][i] == '28':
                    if i not in s.compW:
                        s.compW.append(i)
            s.compW.sort()
        elif dote.split(':')[0] in ('29','30','31'):
            for i in range(len(s.ARMDS[0])):
                if s.ARMDS[2][i] == dote.split(':')[0]:
                    if i not in s.compA:
                        s.compA.append(i)
            s.compA.sort()
        s.dotes.append(dote)
    if not input('\nDesea subir de nivel? ').lower().startswith('s'):
        break
