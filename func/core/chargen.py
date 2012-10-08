# coding=UTF-8
import os
from func.core.lang import t # t() función de traducción a otros idiomas
from func.core.intro import imprimir_titulo # función para imprimir el título del programa
from func.core.prsnj import Pj as P # estadisticas del personaje a crear
from func.data.setup import data as S # datos básicos necesarios (razas, clases, dotes, etc)
import func.gen.iniciales as B # funciones relativas a elecciones básicas (clase, raza, etc)
import func.gen.cars as C # funciones relativas a las características
import func.gen.habs as H # funciones relativas a las habilidades
import func.gen.dotes as D # funciones relativas a las dotes
import func.gen.apts as A # funciones relativas a las aptitudes especiales y los conjuros
import func.gen.viz as V # funciones relativas a la visualización del generador
import func.gen.objetos as O # funciones relativas al oro y los objetos del personaje
import func.gen.estats as T # funciones relativas a las estadísticas de combate
import func.gen.export as E # funciones relativas al guardado del personaje generado


def go ():
    os.system(['clear','cls'][os.name == 'nt'])
    while True:
        P.nivel += 1
        if P.nivel == 1:
            imprimir_titulo()
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
            if 'Dt_rcl' in P.raza:
                P.e_dts['dt_rcl'] =  P.raza['Dt_rcl']
            
            ## Repartir puntuaciones de característica y aplicar mods raciales ##
            print ('\n'+t('Reparte tus puntuaciones de característica'))
            for Car in S.Cars:
                P.CARS[S.Cars.index(Car)]=C.repartir_puntuaciones(tirs,Car)
        
            if 'Ajustes' in  P.raza:
                for Car in P.raza['Ajustes']:
                    P.CARS[S.Cars.index(Car)]+=P.raza['Ajustes'][Car]
            
            for i in range(len(P.CARS)):
                P.CARS_mods.append(C.CarMod(P.CARS[i]))
                        
            ## Elección de Alineamiento ##
            P.alini = B.elegir_alineamiento(S.alinieamientos)
        
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
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
        P.NL = A.calcular_NL(clase,P.cla,S.CLASES)
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
                nuevas.append(str(aptitud))
                for ap in nuevas:
                    A.actualizar_aptitudes (clase,ap,S.APTS,S.CLASES[clase]['Apts'],S.DOTES)
                nuevas = []
        ## Aumento de Características en niveles multiplos de 4 ##
        if P.nivel % 4 == 0:
            Car = C.aumenta_caract(P.nivel)
            P.CARS[Car]+=1
            P.CARS_mods[Car] = C.CarMod(P.CARS[Car])
            print ('El personaje tiene ahora '+S.Cars[Car]+' '+str(P.CARS[Car])+' (+'+str(P.CARS_mods[Car])+')')
        
        ## Cáculo de puntos y Asignación de Rangos de habilidad ##
        input (t('\n[Presione Enter para continuar]\n'))
        hab_rng = H.elegir_habs (S.CLASES[clase]['PH'],P.rng,S.HABS,clase,
                             H.PuntHab (S.CLASES,clase,P.nivel,P.CARS_mods[3],P.subtipo))
        for i in range(len(hab_rng)):
            P.rng[i] =+ hab_rng[i]
        
        ## Elección de Dotes ##
        os.system(['clear','cls'][os.name == 'nt'])
        if P.nivel in (1,3,6,9,12,15,18):
            P.e_dts['dt_nv'] = True
        if any(P.e_dts.values()):
            dotes = D.elegir_dotes(P.dotes,clase) # nuevo
            for dote in dotes:
                D.aplicar_dote(dote,S.DOTES,S.ARMAS,S.ARMDS)
        
        ## Elección de Equipo ##
        compras = O.elegir_equipo(clase,P.equipo)
        P.equipo = compras[0]
        P.dinero = compras[1]
        
        ## Cálculo de estadísticas de combate
        P.PG = T.calcular_PG(P.PG,P.CARS_mods[2],S.CLASES[clase]['DG'],P.nivel,P.dotes) # puntos de golpe
        P.ataques = T.calcular_ATKs (P.stats[0],P.CARS_mods[0],P.CARS_mods[1],
                                     P.tam,P.equipo['Armas'],P.dotes,S.ARMAS) # modificadores de ataque
        P.CA = T.calcular_CA (P.tam,P.CARS_mods[1],P.equipo['Armds'],S.ARMDS) # CA
        P.iniciativa = T.calcular_inic (P.CARS_mods[1],P.dotes) # iniciativa
        
    
        if "Lanzamiento_de_conjuros" in S.CLASES[clase]:
            A.elegir_conjuros(clase,P.cla.count(clase),P.conjuros,
                              S.CLASES,S.CONJUROS,S.ESCUELAS)
            
        if not input('\nDesea subir de nivel? ').lower().startswith('s'):
            break
    
    if P.nombre == '':
        P.nombre = input('\nNombre: ').capitalize()
    
    E.aplicar_mods (S.DOTES, S.HABS, P.raciales, P.dotes, P.rng)
    E.imprimir_apts(P.apps,S.APTS,P.aprin)
    E.autoguardar(P.guardar_pj())
    E.exportar_pj()