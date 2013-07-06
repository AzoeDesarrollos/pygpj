# coding=UTF-8
import os
from func.core.lang import t # t() función de traducción a otros idiomas
from func.core.intro import imprimir_titulo # función para imprimir el título del programa
from func.core.config import puntgen # configuración para la generacion de características
from func.core.prsnj import Pj as P # estadisticas del personaje a crear
import func.core.export as E # funciones relativas al guardado del personaje generado
import func.core.viz as V # funciones relativas a la visualización del generador
from func.data.setup import data as S # datos básicos necesarios (razas, clases, dotes, etc)
import func.gen.iniciales as B # funciones relativas a elecciones básicas (clase, raza, etc)
import func.gen.cars as C # funciones relativas a las características
import func.gen.habs as H # funciones relativas a las habilidades
import func.gen.dotes as D # funciones relativas a las dotes
import func.gen.apts as A # funciones relativas a las aptitudes especiales y los conjuros
import func.gen.objetos as O # funciones relativas al oro y los objetos del personaje


def go ():
    while True:
        P.nivel += 1
        if P.nivel == 1:
            imprimir_titulo()
            
            ## Inicio ##
            tipo = puntgen[0]
            sub = puntgen[1:]
            if tipo == 'A':
                tirs = C.imprimir_puntos(C.generar_tiradas(S.CAMPNG[tipo][sub]),'A')
            elif tipo == 'C':
                tirs = C.imprimir_puntos(S.CAMPNG[tipo][sub],'C')
            
            ## Seleccionar Raza ##
            raza =  B.elegir_raza(S.RAZAS)
            
            ## Repartir puntuaciones de característica ##
            if tipo in ('A','C'):
                P.asignar_carcteristicas(S.CAMPNG,tirs)
            else:
                P.asignar_carcteristicas(S.CAMPNG)
            
            ## Aplicar modificadores raciales ##
            P.aplicar_raza (raza)
            
            ## Elección de Alineamiento ##
            P.alini = B.elegir_alineamiento(S.alins)
        
        imprimir_titulo()
        print (V.barra(P.CARS,S.alins[P.alini]['Abr'],P.raza['Nombre']))
        print ('\n~~ '+t(str(P.nivel)+'º')+' '+t('NIVEL')+' ~~\n')
        
        ## Elección de Clase ##
        if P.nivel == 1:
            clase = B.elegir_clase('',S.CLASES,P.alini)
            P.idiomas = B.idiomas_iniciales(S.IDIOMAS,S.CLASES[clase],P.raza,P.CARS['INT']['Mod'])
        else:
            clase = B.elegir_clase(P.clases[P.nivel-2],S.CLASES,P.alini)
        P.aplicar_clase(clase)
        
        ## Asignar y aplicar Aptitudes de clase ##
        nuevas = []
        if str(P.cla.count(clase)) in S.CLASES[clase]['Apts']:
            for aptitud in S.CLASES[clase]['Apts'][str(P.cla.count(clase))]:
                nuevas.append(str(aptitud))
                for ap in nuevas:
                    apt = A.actualizar_aptitudes (ap,P.apts,S.APTS)
                    if apt != None: #chapuza. el 'NoneType' se genera con Aptitud Especial,
                        #debido a que no es una aptitud real, si no un mero placeholder.
                        P.agregar_ap(*apt)
                nuevas = []
        
        ## Aumento de Características en niveles multiplos de 4 ##
        if P.nivel % 4 == 0:
            C.elegir_aumento_de_caracteristica(nivel,S.Cars)
        
        ## Cáculo de puntos y Asignación de Rangos de habilidad ##
        hab_rng = H.elegir_habs (P.habs,clase,P.nivel,S.HABS)
        P.actualizar_habilidades(hab_rng)
        
        ## Elección de Dotes ##
        if P.nivel == 1 or P.nivel%3 == 0:
            P.e_dts['dt_nv'] = True
        if any(P.e_dts.values()):
            D.elegir_dotes(P.dotes,clase)
        
        ## Elección de Equipo ##
        compras = O.comprar_equipo(clase)
        P.dinero = compras[1]
        
        P.actualizar_inventario (compras[0])
        P.equipar_pj ()
        
        ## Cálculo de estadísticas de combate
        P.calcular_estadisticas_de_combate(clase,S.DOTES,S.CLASES)
        
        if "Lanzamiento_de_conjuros" in S.CLASES[clase]:
            A.elegir_conjuros(clase,P.cla.count(clase),P.conjuros,
                              S.CLASES,S.CONJUROS,S.ESCUELAS)
            
        if not input('\nDesea subir de nivel? ').lower().startswith('s'):
            break
    
    if P.nombre == '':
        P.nombre = input('\nNombre: ').capitalize()
    
    P.calcular_sinergias (S.HABS)
    P.aprin = E.imprimir_apts(P.apts,S.APTS,P.aprin)
    E.autoguardar(P.guardar_pj())
    E.exportar_pj()

