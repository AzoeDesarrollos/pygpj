# coding=UTF-8
from gen.dotes import elegir_dotes
from core.prsnj import Pj as p
import gen.viz as v
import data.setup as s
import os

def elegir_AE (mecanicas,app_pj):
    print ('Esta aptitud especial te permite elegir una de las siguientes aptitudes.\nElije una.\n')

    elegibles = []

    for i in range(len(mecanicas[1])):
        if mecanicas[1][i] == '3':
            if mecanicas[0][i] not in app_pj:
                elegibles.append(mecanicas[0][i])

    for i in range(len(elegibles)):
        if ':' in elegibles[i]:
            tipo = elegibles[i].split(':')[1]
            if tipo == 'Gen':
                elegibles[i] = 'Dote general'
    
    seleccion = v.subselector('AE',elegibles)
        
    if seleccion == 'Dote general':
        return 'd'
    else:
        return seleccion

def actualizar_aptitudes (ap,APSmc,apps_pj,dotes,DOTES,HABS,clase,sub = ''):
    '''Actuliza la lista de aptitudes del personaje.'''
    
    nom = APSmc[ap]['Nombre']
    tipo = APSmc[ap]['Tipo'].split(':')[0]
    if ':' in APSmc[ap]['Tipo']:
        mec = APSmc[ap]['Tipo'].split(':')[1]
    if 'Sublista' in APSmc[ap]:
        sub = APSmc[ap]['Sublista']
        prompt = APSmc[ap]['Sub_Sel']
    
    if tipo == 'u':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = v.subselector(prompt,sub,dos_col=True)
            p.apps.append(str(ap)+':'+str(elec))
        else:
            p.apps.append(str(ap))

    elif tipo == 'v':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = v.subselector(prompt,sub,dos_col=True)
            p.apps.append(str(ap)+':'+str(elec))
        elif ap == '83': ## Chapuza.. no me gusta
            p.apps.append(str(ap))
        else:
            p.apps.append(str(ap))

    elif tipo == 'r':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = v.subselector(prompt,sub,dos_col=True)
            p.apps[p.apps.index(mec)] = str(ap)+':'+str(elec)
        elif apps_pj.count(mec) > 1:
            while apps_pj.count(mec) >1:
                del p.apps[p.apps.index(mec)]
            p.apps[p.apps.index(mec)] = str(ap)
        else:
            p.apps[p.apps.index(mec)] = str(ap)
        
    elif tipo == 'a':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = v.subselector(prompt,sub)
            for i in range(len(DOTES)):
                if DOTES[i]['Nombre'] == sub[elec]:
                    p.dotes.append(str(i))
        else:
            p.dotes.append(str(APSmc[ap]['ID_dt']))

    elif tipo == 'd':
        p.e_dts['dt_cls'] = True

    elif tipo == 'x':
        e = elegir_AE (APSmc,apps_pj)
        if e == 'd':
            p.dotes.append(elegir_dotes(setup.DOTES,p.dotes))
        else:
            p.apps.append(e)

def sort_conj_clase (clase, nv_cnj, conjuros, CONJUROS, ESCUELAS, escuela='Ninguna'):
    '''Muestra los conjuros disponibles por de Clase y por Nivel de conjuro.
    
    También puede, opcionalmente, discriminar por escuela.'''
    texto = []
    for i in range(len(CONJUROS)):
        if i not in conjuros:
            if clase+' '+str(nv_cnj) in CONJUROS[i]['Nivel']:
                if escuela == 'Ninguna':
                    texto.append(CONJUROS[i]['Nombre'])
                else:
                    for j in range(len(ESCUELAS)):
                        if escuela == ESCUELAS[j]['Nombre']:
                            if i in ESCUELAS[j]['Conjuros']:
                                texto.append(CONJUROS[i]['Nombre'])
    return texto

def sort_conj_escuela (index_escuela, CONJUROS, ESCUELAS):
    '''Muestra todos los conjuros de la escuela dada y su nivel para cada clase.'''
    texto = []
    for i in ESCUELAS[index_escuela]['Conjuros']:
        texto.append(CONJUROS[i]['Nombre'])
    
    return texto

def info_conjuro (CONJUROS,ESCUELAS):
    '''Devuelve la info completa de un conjuro por su nombre.'''
    
    conjuros = [CONJUROS[i]['Nombre'] for i in range(len(CONJUROS))]
    conjuro = ''
    while conjuro == '':
        conjuro = input('\nConjuro: ').capitalize()
        while conjuro not in conjuros:
            print ('\nEscriba el nombre del conjuro correctamente')
            conjuro = input('Conjuro: ')
    
    for i in range(len(CONJUROS)):
        if CONJUROS[i]['Nombre'] == conjuro:
            texto = '\n'.join((conjuro,ESCUELAS[CONJUROS[i]['Escuela']]['Nombre'],
                               'Nivel: '+', '.join(CONJUROS[i]['Nivel']),CONJUROS[i]['Efecto']))
    return texto

def conjuros_conocidos (clase,nv_cls,nv_cnj,conjuros,CLASES,CONJUROS,ESCUELAS):
    conocidos = []
    elects = []
    conjuros_nuevos = sort_conj_clase(clase,nv_cnj,conjuros,CONJUROS,ESCUELAS)
    if 'Conjuros_Conocidos' in CLASES[clase]:
        cantidad = CLASES[clase]['Conjuros_Conocidos'][str(nv_cls)][str(nv_cnj)]
        print ('\nPuede elegir '+str(cantidad)+' conjuros, de entre los siguientes:\n')
        elect = v.subselector('Conjuro',conjuros_nuevos,True,cantidad)
        for i in elect:
            elects.append(i)
    else:
        while True:
            vueltas = ''
            while vueltas == '':
                vueltas = input ('\n¿Cuantos conjuros desea agregar? ')
                if not vueltas.isnumeric():
                    print ('\nLa cantidad debe ser numérica.')
                    vueltas = ''
                elif int(vueltas) > len(conjuros_nuevos):
                    print('\nNo puede seleccionar tantos conjuros. El máximo es '+str(len(conjuros_nuevos))+'.')
                    vueltas = ''
                else:
                    vueltas = int(vueltas)

            if vueltas > 1:
                elect = v.subselector('Conjuro',conjuros_nuevos,True,vueltas)
                for i in elect:
                    elects.append(i)
            else:
                elect = v.subselector('Conjuro',conjuros_nuevos,True)
                elects.append(elect)
            if not input('\n¿Desea agregar más conjuros? ').lower().startswith('s'):
                break

    for index in elects:
        for i in range(len(CONJUROS)):
            if CONJUROS[i]['Nombre'] == conjuros_nuevos[index]:
                conocidos.append(i)

    return conocidos

def elegir_conjuros (clase, nv_cls, conjuros, CLASES, CONJUROS, ESCUELAS):
    '''Selección de conjuros.'''

    def nivel_conjuro ():
        nv_cnj = ''
        while nv_cnj == '':
            nv_cnj = input('\nElija un nivel de conjuros [0 - 9]: ')
            if not nv_cnj.isnumeric():
                print('\nEl nivel de conjuros debe ser numérico.')
                nv_cnj = ''
            elif not 0 <= int(nv_cnj) <= 9:
                print ('\nEl nivel de conjuros debe ser un número entre 0 y 9')
                nv_cnj = ''
            else:
                nv_cnj = int(nv_cnj)
        return nv_cnj
    
    opciones = ['Elegir nuevos conjuros conocidos',
                'Preparar un set de conjuros',
                'Ver los conjuros de clase disponibles',
                'Ver la información de un conjuro específico',
                'Ver los conjuros conocidos',
                'Ver todos los conjuros de una escuela de magia']
    op = ''
    while op == '':
        os.system(['clear','cls'][os.name == 'nt'])
        print('En este nivel, debe elegir conjuros',end = '\n\n')
        print ('¿Que desea hacer?\n')
        op = v.subselector('Opción',opciones)
        if op == 0: # Elegir nuevos conjuros conocidos
            nv_cnj = nivel_conjuro()
            conjuros  += conjuros_conocidos(clase,nv_cls,nv_cnj,conjuros,CLASES,CONJUROS,ESCUELAS)
            opciones.append('Nada más')            
            op = ''
        elif op == 1: # Preparar un set de conjuros
            print ('\nEsta opción aún no se encuentra en funcionamiento')
        elif op == 2: # Ver los conjuros de clase disponibles
            nv_cnj = nivel_conjuro()
            v.paginar_dos_columnas(10,(sort_conj_clase (clase, nv_cnj, conjuros, CONJUROS, ESCUELAS)))
        elif op == 3: # Ver la información de un conjuro específico
            print('\n'+info_conjuro(CONJUROS,ESCUELAS))
        elif op == 4: # Ver los conjuros conocidos
            if len(conjuros) == 0:
                print ('\nNo hay conjuros que mostrar aún.')
            else:
                lineas = [CONJUROS[i]['Nombre'] for i in conjuros]
                v.paginar_dos_columnas(10,lineas)
        elif op == 5: # Ver todos los conjuros de una escuela de magia
            print('\nElija una escuela de magia')
            escuelas = [ESCUELAS[i]['Nombre'] for i in range(len(ESCUELAS))]
            esc = v.subselector('Escuela',escuelas)
            v.paginar_dos_columnas(10,(sort_conj_escuela (esc, CONJUROS, ESCUELAS)))
            op = ''
        elif op == 6: # Nada más
            return sorted(conjuros)
    
    input ('\n[Presione Enter para continuar]')