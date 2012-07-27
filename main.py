# coding=UTF-8

from time import sleep
import os
import setup
import prsnj as p
import func as f
import sels as s

# barra = ''.join((Raza[0],'| FUE '+str(CARS[0]),' DES '+str(CARS[1]),' CON '+str(CARS[2]),' INT '+str(CARS[3]),' SAB '+str(CARS[4]),'| Al '+alinis[alini]))

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
        Raza = s.SelRaza(setup.RAZAS)
        p.subtipo = Raza['Subtipo']
        p.tam_nom = Raza['Tamaño']
        p.tam_mod = p.tam[tam_nom][0]
        p.tam_pres = p.tam[tam_nom][1]
        p.tam_esc = p.tam[tam_nom][2]
        if 'Hab_rcl' in Raza:
            p.raciales = Raza['Hab_rcl']
        
        ## Repartir puntuaciones de característica y aplicar mods raciales ##
        print ('\nReparte tus puntuaciones de característica')
        for Car in p.Cars:
            p.CARS[p.Cars.index(Car)]=s.RepPunto(tirs,Car)

        for Car in p.Cars:
            p.CARS[p.Cars.index(Car)]+Raza['Ajustes'][p.Cars.index(Car)]
        
        p.CARS_mods = [f.CarMod(p.CARS[0]),f.CarMod(p.CARS[1]),f.CarMod(p.CARS[2]),
                     f.CarMod(p.CARS[3]),f.CarMod(p.CARS[4]),f.CarMod(p.CARS[5])]
        
        ## Elección de Alineamiento ##
        p.alini = s.Alinear()
    
    # os.system(['clear','cls'][os.name == 'nt'])
    # print (barra)
    print ('\n~~ '+str(p.nivel)+'º NIVEL ~~\n')
    
    ## Elección de Clase ##
    if p.nivel == 1:
        cla_in = s.SelCla('',setup.CLASES,p.alini)
        p.idiomas = s.SelIdiomas(setup.IDIOMAS,setup.CLASES[cla_in],Raza,CARS_mods[3])
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
        Car = AumentaCar(p.nivel)
        p.CARS[Car]+=1
        print ('El personaje tiene ahora '+p.Cars[Car]+' '+str(p.CARS[Car])+' (+'+str(f.CarMod(p.CARS[Car]))+')')
        input ('\n[Presione Enter para continuar]\n')
    
    ## Cáculo de puntos y Asignación de Rangos de habilidad ##
    # op.system(['clear','cls'][op.name == 'nt'])
    # print (barra)
    hab_rng = s.RepRNG (f.PuntHab (setup.CLASES,cla_in,p.nivel,CARS_mods[3],subtipo),
                      p.clases.count(clase),f.Claseas(setup.CLASES,cla_in,setup.HABS),setup.HABS,p.rng)
    for i in hab_rng[0]:
        p.rng[i] = hab_rng[0][i]
    p.idiomas += hab_rng[1]
    
    ## Elección de Dotes ##
    if p.nivel in (1,3,6,9,12,15,18):
        #os.system(['clear','cls'][os.name == 'nt'])
        # print (barra)
        dote = s.SelDot(p.nivel,p.dotes,setup.DOTES,p.compW,setup.ARMAS,setup.HABS,False,cla_in)
        p.dotes.append(dote)
    if p.dt_cl == True:
        dote = s.SelDot(p.nivel,p.dotes,setup.DOTES,p.compW,setup.ARMAS,setup.HABS,True,cla_in,
                        setup.CLASES[cla_in]['dt_cls'])
        p.dt_cl = False
        p.dotes.append(dote)
    if dote != '':
        if dote.split(':')[0] in ('26','27'):
            p.compW.append(int(dote.split(':')[1]))
        elif dote.split(':')[0] == '28':
            for i in range(len(setup.ARMAS)):
                if setup.ARMAS[i]['Competencia'] == 28:
                    if i not in p.compW:
                        p.compW.append(i)
            p.compW.sort()
        elif dote.split(':')[0] in ('29','30','31'):
            for i in range(len(setup.ARMDS)):
                if setup.ARMDS[i]['Competencia'] == int(dote.split(':')[0]):
                    if i not in p.compA:
                        p.compA.append(i)
            p.compA.sort()
        
    if not input('\nDesea subir de nivel? ').lower().startswith('s'):
        break