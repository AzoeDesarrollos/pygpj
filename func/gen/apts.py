# coding=UTF-8
from func.gen.dotes import elegir_dotes
from func.core.intro import imprimir_titulo
from func.core.prsnj import Pj as p
import func.core.viz as v
from func.data.setup import data as s

import os
from math import floor

def elegir_AE (apts_pj,APTS):
    '''Subselector dedicado para la aptitud de Pícaro: Aptitud especial'''
    
    elegibles = [[APTS[key]['Nombre'],key] for key in APTS
                if ('3' in APTS[key]['Clase']) and (key not in apts_pj)]
    
    nom = sorted([i[0] for i in elegibles])
    ind = sorted([i[1] for i in elegibles])

    sel = subselector('AE',nom)
    seleccion = APTS[ind[sel]]['Tipo']
        
    if seleccion == 'd':
        return 'd' # devuelve 'd' si la selección es una dote adicional
    else:
        return ind[sel] # o el índice de la aptitud especial.

def actualizar_aptitudes (ap,apts_pj,APTS): # tiene similitud con dotes.validar_requisitos
    '''Lee la aptitud entrante, y la envía a Pj.agregar_ap con el método correspondiente'''
    
    tipo = APTS[ap]['Tipo'].split(':')[0]
    if ':' in APTS[ap]['Tipo']:
        mec = APTS[ap]['Tipo'].split(':')[1]    

    if 'Sublista' in APTS[ap]: # si la aptitud tiene opciones, pasa por aqui.
        sub = APTS[ap]['Sublista']
        prompt = APTS[ap]['Sub_Sel']
        if tipo == 'u': 
            if ap not in apts_pj:
                apt = tipo_u(ap,sub,prompt)
        elif tipo == 'v': 
            apt = tipo_v(ap,sub,prompt)
        elif tipo == 'r': 
            apt = tipo_r (ap,mec,sub,prompt)
        elif tipo == 'a': 
            apt = tipo_a(ap,sub,prompt)
    else:
        if tipo == 'u': # tipo u: aptitudes únicas e irrepetibles
            if ap not in apts_pj:
                apt = tipo_u(ap)
        elif tipo == 'v': # tipo v: aptitud apilable (ataque furtivo, forma salvaje, etc.)
            apt = tipo_v(ap)
        elif tipo == 'r': # tipo r: esta aptitud reemplaza a otra (ej. evasión mejorada)
            apt = tipo_r (ap,mec)
        elif tipo == 'a': # tipo a: esta aptitud es una dote adicional.
            apt = tipo_a (ap)
        elif tipo == 'd': # tipo d: dotes de guerreros, magos y dotes adicionales de picaro
            apt = ['',{},'t']
        elif tipo == 'x': # tipo x: activa Elegir AE para la aptitud especial de pícaro
            apt = tipo_x (apts_pj)
        elif tipo == 's': # tipo s: activa Elegir dominio para los dominios de clérigo
            apt = tipo_s (ap)
    
    return apt

def tipo_u (ap,sub = '',prompt = ''):
    if sub != '':
        print ('\n'+s.APTS[ap]['Intro'])
        elec = v.subselector(prompt,sub,dos_col=True)
        apt = [str(ap),{'sub':str(elec)},'a']
    else:
        apt = [str(ap),{},'a']

    return apt 

def tipo_v (ap,sub = '',prompt = ''):
    if sub != '':
        print ('\n'+s.APTS[ap]['Intro'])
        elec = v.subselector(prompt,sub,dos_col=True)
        apt = [str(ap),{'sub':str(elec),'In_Val':s.APTS[ap]['Valor_Inicial']},'c']
    else:
        apt = [str(ap),{'cant':s.APTS[ap]['Valor_Inicial']},'c']
    return apt

def tipo_r (ap,tipo,sub = '',prompt = ''):
    if sub != '':
        print ('\n'+s.ATPS[ap]['Intro'])
        elec = v.subselector(prompt,sub,dos_col=True)
        apt = [str(ap),{'sub':str(elec)},'r'+tipo]
    else:
        apt = [str(ap),{},'r'+tipo]
    
    return apt

def tipo_a (ap,sub = '',prompt = ''):
    if sub != '':
        print ('\n'+s.APTS[ap]['Intro'])
        elec = v.subselector(prompt,sub)
        for d in s.DOTES:
            if s.DOTES[d]['Nombre'] == sub[elec]:
                dote = [d,{},'d']
    else:
        dote = [str(s.APTS[ap]['ID_dt']),{},'d']
    return dote

def tipo_x (apts_pj):
    e = elegir_AE (apts_pj,s.APTS)
    if e == 'd':
        dote = elegir_dotes(s.DOTES,p.dotes)
        return [dote,{},'d']
    else:
        apt = actualizar_aptitudes(e,p.apts,s.APTS)
        return apt

def tipo_s (ap):
    doms = elegir_dominio(p.alini,2,s.DOMINIOS) # 2 es hardcoding...
    apt = [ap,{'doms':doms},'s']
    return apt

def elegir_dominio (alini,cant,DOMINIOS):
    '''Provee un selector para los dominios de clérigo'''
    
    imprimir_titulo()
    disponibles = []
    for i in DOMINIOS:
        if 'Req_AL' in DOMINIOS[i]:
            if alini in DOMINIOS[i]['Req_AL']:
                disponibles.append(DOMINIOS[i]['Nombre'])
        else:
            disponibles.append(DOMINIOS[i]['Nombre'])

    disponibles.sort()
    print ('Debes elegir '+str(cant)+' dominios de entre los siguientes:')
    elect = v.subselector('Dominio',disponibles,True,cant)

    keys = []
    for i in elect:
        for key in DOMINIOS:
            if disponibles[i] == DOMINIOS[key]['Nombre']:
                keys.append(key) 
    
    return keys

def sort_conj_clase (clase, nv_cnj, conjuros, CONJUROS, ESCUELAS, escuela='Ninguna'):
    '''Muestra los conjuros disponibles por de Clase y por Nivel de conjuro.
    
    También puede, opcionalmente, discriminar por escuela.'''
    texto = []
    for conj in CONJUROS:
        if conj not in conjuros:
            if clase+' '+str(nv_cnj) in CONJUROS[conj]['Nivel']:
                if escuela == 'Ninguna':
                    texto.append(CONJUROS[conj]['Nombre'])
                else:
                    for esc in ESCUELAS:
                        if escuela == ESCUELAS[esc]['Nombre']:
                            if conj in ESCUELAS[esc]['Conjuros']:
                                texto.append(CONJUROS[conj]['Nombre'])
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
    conjuros_nuevos = sort_conj_clase(CLASES[clase]['Abr'],nv_cnj,conjuros,CONJUROS,ESCUELAS)
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
        for c in CONJUROS:
            if CONJUROS[c]['Nombre'] == conjuros_nuevos[index]:
                conocidos.append(c)

    return conocidos

def calcular_NL (clase,cla,CLASES):
    NL = {}    
    for cls in CLASES:
        if 'NL' in CLASES[clase]:
            if clase == cls:
                if not cla.count(clase) < CLASES[cls]['NL'][1]:
                    NL[clase] = floor(cla.count(clase)*CLASES[cls]['NL'][0])
    return NL

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
        imprimir_titulo()
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