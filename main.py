# coding=UTF-8

from time import sleep
import os
import setup
import prsnj as p
import func as f
import sels as s
import viz as v
import export as e
from intro import *

while True:
    p.nivel += 1
    if p.nivel == 1:
        ## Inicio ##
        tirs = f.GenTir()
        op = s.SelTirs(tirs)
        while op == False:
            tirs = f.GenTir()
            op = s.SelTirs(tirs)
        
        ## Seleccionar Raza ##
        p.raza = s.SelRaza(setup.RAZAS)
        p.subtipo = p.raza['Subtipo']
        p.tam_nom = p.raza['Tamaño']
        p.velocidad = p.raza['Velocidad']
        p.tam_mod = setup.tam[p.tam_nom][0]
        p.tam_pres = setup.tam[p.tam_nom][1]
        p.tam_esc = setup.tam[p.tam_nom][2]
        if 'Hab_rcl' in p.raza:
            p.raciales = p.raza['Hab_rcl']
        elif 'Dt_rcl' in p.raza:
            p.dt_rcl =  p.raza['Dt_rcl']
        
        ## Repartir puntuaciones de característica y aplicar mods raciales ##
        print ('\nReparte tus puntuaciones de característica')
        for Car in p.Cars:
            p.CARS[p.Cars.index(Car)]=s.RepPunto(tirs,Car)

        for Car in p.Cars:
            p.CARS[p.Cars.index(Car)]+= p.raza['Ajustes'][p.Cars.index(Car)]
        
        p.CARS_mods = [f.CarMod(p.CARS[0]),f.CarMod(p.CARS[1]),f.CarMod(p.CARS[2]),
                     f.CarMod(p.CARS[3]),f.CarMod(p.CARS[4]),f.CarMod(p.CARS[5])]
        
        p.iniciativa = p.CARS_mods[1]
        
        ## Elección de Alineamiento ##
        p.alini = s.Alinear()
    
    os.system(['clear','cls'][os.name == 'nt'])
    print (v.barra(p.CARS,setup.alinis[p.alini],p.raza['Nombre']))
    print ('\n~~ '+str(p.nivel)+'º NIVEL ~~\n')
    
    ## Elección de Clase ##
    if p.nivel == 1:
        cla_in = s.SelCla('',setup.CLASES,p.alini)
        p.idiomas = s.SelIdiomas(setup.IDIOMAS,setup.CLASES[cla_in],p.raza,p.CARS_mods[3])
    else:
        cla_in = s.SelCla(p.lasclases[p.nivel-2],setup.CLASES,p.alini)
    p.compW = f.Competencias (setup.CLASES[cla_in]['Comp_Arma'],p.compW)
    p.compA = f.Competencias (setup.CLASES[cla_in]['Comp_Armd'],p.compA)
    p.cla.append(cla_in)
    clase = setup.CLASES[cla_in]['Abr']
    p.clases.append(setup.CLASES[cla_in]['Abr'])
    p.lasclases.append(setup.CLASES[cla_in]['Nombre'])
    for i in range(len(p.cla)):
        if p.cla[i] == '':
            p.cla[i] = p.cla[i-1]
        
    p.stats = f.procesar_clase(setup.CLASES[cla_in],p.clases.count(clase),p.stats)
    
    ## Asignar y aplicar Aptitudes de clase ##
    nuevas = []
    if str(p.clases.count(clase)) in setup.CLASES[cla_in]['Apts']:
        for aptitud in setup.CLASES[cla_in]['Apts'][str(p.clases.count(clase))]:
            nuevas.append(aptitud)
            for ap in nuevas:
                f.actualizar_aptitudes (ap,setup.APTS,setup.CLASES[cla_in]['Apts'],
                                        p.dotes,setup.DOTES,setup.HABS,cla_in)
            # p.apps.append(aptitud) # Recuerda, luego, calcular los índices: APs_mc[0].index(aptitud)
            nuevas = []
        
    ## Aumento de Características en niveles multiplos de 4 ##
    if p.nivel % 4 == 0:
        Car = s.AumentaCar(p.nivel)
        p.CARS[Car]+=1
        p.CARS_mods[Car] = f.CarMod(p.CARS[Car])
        print ('El personaje tiene ahora '+p.Cars[Car]+' '+str(p.CARS[Car])+' (+'+str(f.CarMod(p.CARS[Car]))+')')
    
    ## Cáculo de puntos y Asignación de Rangos de habilidad ##
    input ('\n[Presione Enter para continuar]\n')
    os.system(['clear','cls'][os.name == 'nt'])
    print (v.barra(p.CARS,setup.alinis[p.alini],p.raza['Nombre']))
    hab_rng = s.SelHabs (p.CARS_mods[3],setup.CLASES[cla_in]['PH'],
                         f.PuntHab (setup.CLASES,cla_in,p.nivel,p.CARS_mods[3],p.subtipo),
                         p.rng,setup.HABS,clase,cla_in,p.clases.count(clase),p.subtipo,)
    #hab_rng = s.RepRNG (f.PuntHab (setup.CLASES,cla_in,p.nivel,p.CARS_mods[3],p.subtipo),
    #                  p.clases.count(clase),f.Claseas(setup.CLASES,cla_in,setup.HABS),setup.HABS,p.rng)
    for i in range(len(hab_rng)):
        p.rng[i] =+ hab_rng[i]
    
    ## Elección de Dotes ##
    os.system(['clear','cls'][os.name == 'nt'])
    print (v.barra(p.CARS,setup.alinis[p.alini],p.raza['Nombre']))
    if p.dt_rcl == True:
        texto = '\nComo aptitud racial, tienes una dote adicional para elegir.\n'
        dote = s.SelDot(p.dotes,setup.DOTES,p.compW,setup.ARMAS,setup.ESCUELAS,setup.HABS,False,cla_in,intro=texto)
        p.dt_rcl = False
        f.aplicar_dote(dote,setup.DOTES,setup.ARMAS,setup.ARMDS)
        p.dotes.append(dote)
    if p.nivel in (1,3,6,9,12,15,18):
        texto = '\nEn el '+str(p.nivel)+'º nivel, tienes una dote para elegir.\n'
        dote = s.SelDot(p.dotes,setup.DOTES,p.compW,setup.ARMAS,setup.ESCUELAS,setup.HABS,False,cla_in,intro=texto)
        f.aplicar_dote(dote,setup.DOTES,setup.ARMAS,setup.ARMDS)
        p.dotes.append(dote)
    if p.dt_cl == True:
        dote = s.SelDot(p.dotes,setup.DOTES,p.compW,setup.ARMAS,setup.ESCUELAS,setup.HABS,True,cla_in,setup.CLASES[cla_in]['dt_cls'])
        p.dt_cl = False
        f.aplicar_dote(dote,setup.DOTES,setup.ARMAS,setup.ARMDS)
        p.dotes.append(dote)
   
    ## Cálculo de puntos de golpe
    p.PG += f.PG(p.CARS_mods[2],setup.CLASES[cla_in]['DG'],p.nivel)
    if not input('\nDesea subir de nivel? ').lower().startswith('s'):
        break

e.Aplicar_mods (setup.DOTES, setup.HABS, p.raciales, p.dotes, p.rng)
e.autoguardar() ## placeholder
e.Guardar()
