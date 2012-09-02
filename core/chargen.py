# coding=UTF-8
import os
from core.lang import t # t() función de traducción a otros idiomas
from core.prsnj import Pj as P # estadisticas del personaje a crear
import data.setup as S # datos básicos necesarios (razas, clases, dotes, etc)
import gen.iniciales as B # funciones relativas a elecciones básicas (clase, raza, etc)
import gen.cars as C # funciones relativas a las características
import gen.habs as H # funciones relativas a las habilidades
import gen.dotes as D # funciones relativas a las dotes
import gen.apts as A # funciones relativas a las aptitudes especiales y los conjuros
import gen.viz as V # funciones relativas a la visualización del generador
import core.export as E # funciones relativas al guardado del personaje generado

def go ():
    os.system(['clear','cls'][os.name == 'nt'])
    while True:
        P.nivel += 1
        if P.nivel == 1:
            ## Inicio ##
            tirs = C.generar_tiradas()
            op = C.elegir_tiradas(tirs)
            while op == False:
                tirs = C.generar_tiradas()
                op = C.elegir_tiradas(tirs)
            
            ## Seleccionar Raza ##
            P.raza = B.elegir_raza(S.RAZAS)
            P.subtipo = P.raza['Subtipo']
            P.tam['Nombre'] = P.raza['Tamaño']
            P.velocidad = P.raza['Velocidad']
            P.tam['mod_gen'] = S.tam[P.tam['Nombre']][0]
            P.tam['mod_pre'] = S.tam[P.tam['Nombre']][1]
            P.tam['mod_esc'] = S.tam[P.tam['Nombre']][2]
            if 'Hab_rcl' in P.raza:
                P.raciales = P.raza['Hab_rcl']
            elif 'Dt_rcl' in P.raza:
                P.e_dts['dt_rcl'] =  P.raza['Dt_rcl']
            
            ## Repartir puntuaciones de característica y aplicar mods raciales ##
            print ('\n'+t('Reparte tus puntuaciones de característica'))
            for Car in S.Cars:
                P.CARS[S.Cars.index(Car)]=C.repartir_puntuaciones(tirs,Car)
    
            for Car in S.Cars:
                P.CARS[S.Cars.index(Car)]+= P.raza['Ajustes'][S.Cars.index(Car)]
            
            for i in range(len(P.CARS)):
                P.CARS_mods.append(C.CarMod(P.CARS[i]))
            
            P.iniciativa = P.CARS_mods[1]
            
            ## Elección de Alineamiento ##
            P.alini = B.elegir_alineamiento(S.alinieamientos)
        
        os.system(['clear','cls'][os.name == 'nt'])
        print (V.barra(P.CARS,S.alinis[P.alini],P.raza['Nombre']))
        print ('\n~~ '+t(str(P.nivel)+'º')+' '+t('NIVEL')+' ~~\n')
        
        ## Elección de Clase ##
        if P.nivel == 1:
            clase = B.elegir_clase('',S.CLASES,P.alini)
            P.idiomas = B.idiomas_iniciales(S.IDIOMAS,S.CLASES[clase],P.raza,P.CARS_mods[3])
        else:
            clase = B.elegir_clase(P.clases[P.nivel-2],S.CLASES,P.alini)
        P.compW = B.Competencias (S.CLASES[clase]['Comp_Arma'],P.compW)
        P.compA = B.Competencias (S.CLASES[clase]['Comp_Armd'],P.compA)
        P.cla.append(clase)
        P.clases.append(S.CLASES[clase]['Nombre'])
        for i in range(len(P.cla)):
            if P.cla[i] == '':
                P.cla[i] = P.cla[i-1]
            
        P.stats = B.procesar_clase(S.CLASES[clase],P.cla.count(clase),P.stats)
        P.stats[1] += P.CARS_mods[2] # TS Fortaleza
        P.stats[2] += P.CARS_mods[1] # TS Reflejos
        P.stats[3] += P.CARS_mods[4] # TS Voluntad
        
        ## Asignar y aplicar Aptitudes de clase ##
        nuevas = []
        if str(P.cla.count(clase)) in S.CLASES[clase]['Apts']:
            for aptitud in S.CLASES[clase]['Apts'][str(P.cla.count(clase))]:
                nuevas.append(aptitud)
                for ap in nuevas:
                    A.actualizar_aptitudes (ap,S.APTS,S.CLASES[clase]['Apts'],
                                            P.dotes,S.DOTES,S.HABS,clase)
                nuevas = []
            
        ## Aumento de Características en niveles multiplos de 4 ##
        if P.nivel % 4 == 0:
            Car = C.aumenta_caract(P.nivel)
            P.CARS[Car]+=1
            P.CARS_mods[Car] = C.CarMod(P.CARS[Car])
            print ('El personaje tiene ahora '+S.Cars[Car]+' '+str(P.CARS[Car])+' (+'+str(P.CARS_mods[Car])+')')
        
        ## Cáculo de puntos B Asignación de Rangos de habilidad ##
        input (t('\n[Presione Enter para continuar]\n'))
        os.system(['clear','cls'][os.name == 'nt'])
        print (V.barra(P.CARS,S.alinis[P.alini],P.raza['Nombre']))
        hab_rng = H.elegir_habs (S.CLASES[clase]['PH'],P.rng,S.HABS,clase,
                             H.PuntHab (S.CLASES,clase,P.nivel,P.CARS_mods[3],P.subtipo))
        for i in range(len(hab_rng)):
            P.rng[i] =+ hab_rng[i]
        
        ## Elección de Dotes ##
        os.system(['clear','cls'][os.name == 'nt'])
        if P.nivel in (1,3,6,9,12,15,18):
            P.e_dts['dt_nv'] = True
        if any(P.e_dts.values()):
            print (V.barra(P.CARS,S.alinis[P.alini],P.raza['Nombre']))
            dotes = D.elegir_dotes(P.dotes,P.e_dts,clase) # nuevo
            for dote in dotes:
                D.aplicar_dote(dote,S.DOTES,S.ARMAS,S.ARMDS)
        
        #if P.dt_rcl == True:
        #    print('\nComo aptitud racial, tienes una dote adicional para elegir.\n')
        #    dote = D.elegir_dotes(S.DOTES,P.dotes)
        #    P.dt_rcl = False
        #    D.aplicar_dote(dote,S.DOTES,S.ARMAS,S.ARMDS)
        #if P.nivel in (1,3,6,9,12,15,18):
        #    print('\nEn el '+str(P.nivel)+'º nivel, tienes una dote para elegir.\n')
        #    dote = D.elegir_dotes(S.DOTES,P.dotes)
        #    D.aplicar_dote(dote,S.DOTES,S.ARMAS,S.ARMDS)
        #if P.dt_cl == True:
        #    print ('\nComo aptitud de clase, tienes una dote adicional para elegir.\n')
        #    dote = D.elegir_dotes(S.CLASES[clase]['dt_cls'],P.dotes)
        #    P.dt_cl = False
        #    D.aplicar_dote(dote,S.DOTES,S.ARMAS,S.ARMDS)
       
        ## Cálculo de puntos de golpe
        P.PG += B.PG(P.CARS_mods[2],S.CLASES[clase]['DG'],P.nivel)
    
        if "Lanzamiento_de_conjuros" in S.CLASES[clase]:
            A.elegir_conjuros(clase,P.cla.count(clase),P.conjuros,
                              S.CLASES,S.CONJUROS,S.ESCUELAS)
            
        if not input('\nDesea subir de nivel? ').lower().startswith('s'):
            break
        
    E.aplicar_mods (S.DOTES, S.HABS, P.raciales, P.dotes, P.rng)
    E.autoguardar(P.guardar_pj())
    E.exportar_pj()