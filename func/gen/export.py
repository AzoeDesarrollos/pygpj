# coding=UTF-8
'''Modulo de Exportación'''
from func.data.setup import data as s
from func.gen.habs import HabMod
from func.gen.dotes import ver_dotes
from func.core.config import guardar_json
from func.core.prsnj import Pj as p
from func.gen.objetos import imprimir_nom_objmag
from time import sleep,localtime,strftime
from math import floor
import os

def aplicar_mods (lista_dts, lista_habs, raciales, dotes, rangos):
    # Raciales
    for r in raciales:
        p.rcl[r[0]]+=r[1]

    # Por Objetos
    ## aún no implementado
    
    # Por sinergias
    for r in range(len(rangos)):
        if rangos[r] >= 5:
            if 'Sinergias' in lista_habs[r]:
                for i in lista_habs[r]['Sinergias']:
                    p.sng[i]+=2

def orden_habs_imprint (lista_habs,rangos,sinergia,dotes,racial,objetos,equipo,ARMDS):
    '''Ordena las habilidades que se van a imprimir.'''
    
    Orden = [rangos,sinergia,dotes,racial]
    indexes = []
    imprimir = ''
    
    for lista in Orden:
        for index in range(len(lista)):
            if lista[index]!= 0:
                if str(index) not in indexes:
                    indexes.append(str(index))
    indexes.sort()
    
    # Eliminar las habilidades 'solo entrenadas' sin rangos
    for i in indexes:
        if rangos[int(i)] == 0:
            if 'Solo_entrenada' in lista_habs[i]:
                x = indexes.index(i)
                del indexes[x]
    
    pen_armd = 0
    if equipo['armd'] != '':
        pen_armd += ARMDS[equipo['armd']['index']]['Penalizador']
    if equipo['mm'] != '':
        if equipo['mm']['subgrupo'] == 'esc':
            pen_armd += ARMDS[equipo['mm']['index']]['Penalizador']
    
    for h in indexes:
        if s.HABS[h]['Nombre'] == 'Nadar':
            debug = 'Nadar'
        imprimir = imprimir+s.HABS[h]['Nombre']+' +'+str(round(HabMod(h,lista_habs,p.CARS_mods,rangos,
                                                                  racial,sinergia,dotes,objetos,pen_armd)))+', '
    imprimir = imprimir.rstrip(', ')+'.'
    
    return imprimir

def imprimir_DG(clases_pj,CLASES,CON_mod,PG):
    tempD,tempN,tempF = [],[],[]
    modif = CON_mod*len(clases_pj)
    impr = []
    for d in clases_pj:
        impr.append('d'+str(CLASES[d]['DG']))
    
    for p in impr:
        if not p in tempD:
            tempD.append(p)
            tempN.append(str(impr.count(p)))

    for e in range(len(tempD)):
        tempF.append(tempN[e]+tempD[e])
    
    prim = ''
    for p in tempF:
        prim = prim+p+' más '

    if modif < 0:
        prim = prim.rstrip(' más ')+' '+str(modif)
    elif modif == 0:
        prim = prim.rstrip(' más ')
    else:
        prim = prim.rstrip(' más ')+' +'+str(modif)

    prim += ' ('+str(PG)+' pg)'
    return prim

def imprimir_apts (apts,APTS,aprin):
    for ap in apts:
        if ':' in ap:
            sub = ap.split(':')[1]
            ap = ap.split(':')[0]            
        if 'Aptitud' in APTS[ap]:
            if 'Formato' in APTS[ap]:
                nom = APTS[ap]['Nombre']
                if ap == '83':
                    cant = apts.count(ap)+1
                else:
                    cant = apts.count(ap)
                if '2' in APTS[ap]['Formato']:
                    texto = APTS[ap]['Formato'].format(nom,cant,sub)
                else:
                    texto = APTS[ap]['Formato'].format(nom,cant)
            else:
                texto = APTS[ap]['Nombre']
        
        if APTS[ap]['Aptitud'] == 'Ataque especial':
            if texto not in aprin['Ataques']:
                aprin['Ataques'].append(texto)
        else:
            if texto not in aprin['Cualidades']:
                aprin['Cualidades'].append(texto)
    return aprin

def imprimir_clases (cla,CLASES):
    texto = []
    clases = [CLASES[str(i)]['Nombre'] for i in range(len(CLASES))]
    for i in range(len(clases)):
        if str(i) in cla:
            texto.append(clases[i]+' '+str(cla.count(str(i)))+'º')
    
    return ' '.join(texto)

def imprimir_ATK (equipo,ATKs,ARMAS):
    
    arma = equipo['mb']
    imprimir = []

    nombre = imprimir_nom_objmag(arma,s.OBJMAG,s.ARMAS).rstrip()
    bon_atk = ATKs[arma['index']]
    categoria = ARMAS[arma['index']]['Tipo']
    if categoria == 'ad':
        imprimir.append(nombre+' '+'/'.join('+'+str(i) for i in bon_atk)+' a distancia')
    else:
        imprimir.append(nombre+' '+'/'.join('+'+str(i) for i in bon_atk)+' c/c')
    
    if imprimir == []:
        return ''
    else:
        return ', '.join(imprimir)+'.'

def imprimir_CA ():
    return '' #placeholder

def exportar_pj():
    if input('\nDesea Exportar este personaje? ').lower().startswith('s'):
        Pj = open('Personajes/'+p.nombre+'.txt','w')
        Pj.write('Nombre: '+p.nombre+'\n')
        Pj.write('Clase y nivel: '+imprimir_clases(p.cla,s.CLASES)+' AL '+s.alinieamientos[p.alini]+'\n')
        Pj.write('Tipo y Tamaño: Humanoide '+p.tam['Nombre'])
        if p.subtipo != '':
            Pj.write(' ('+p.subtipo+')\n')
        Pj.write('DG: '+imprimir_DG(p.cla,s.CLASES,p.CARS_mods[2],p.PG)+'\n')
        Pj.write('Iniciativa: +'+str(p.iniciativa)+'\nVelocidad: '+p.velocidad+'\n')
        Pj.write('CA: '+imprimir_CA()+'\n')
        Pj.write('Ataque base/Presa: +'+str(floor(p.stats[0]))+'/+'+str(floor(p.stats[0]+p.CARS_mods[0]))+'\n')
        if imprimir_ATK (p.equipo,p.ataques,s.ARMAS) != '':
            Pj.write('Ataque: '+imprimir_ATK (p.equipo,p.ataques,s.ARMAS)+'\n')
        Pj.write('Ataque completo: '+''+'\n')
        Pj.write("E/A: 5'/5'.\n")
        if p.aprin['Ataques'] != []:
            Pj.write('Ataques especiales: '+', '.join(p.aprin['Ataques'])+'.\n')
        if p.aprin['Cualidades'] != []:
            Pj.write('Cualidades especiales: '+', '.join(p.aprin['Cualidades'])+'.\n')
        Pj.write('TS: Fortaleza +'+str(round(p.stats[1]))+', Reflejos +'+str(round(p.stats[2]))
                 +', Voluntad +'+str(round(p.stats[3]))+'.\n')
        Pj.write('Características: Fuerza '+str(p.CARS[0])+', Destreza '+str(p.CARS[1])+
                 ', Constitución '+str(p.CARS[2])+', Inteligencia '+str(p.CARS[3])+
                 ', Sabuduría ' + str(p.CARS[4])+', Carisma '+str(p.CARS[5])+
                 '.\nHabilidades y Dotes: '+orden_habs_imprint(s.HABS,p.rng,p.sng,p.dts,p.rcl,p.obj,p.equipo,s.ARMDS)+
                 ' '+', '.join(ver_dotes(p.dotes,s.DOTES,s.ARMAS,s.HABS,s.ESCUELAS))+'.')
        sleep(3)
        print('\nPersonaje Guardado')
        Pj.close()
    sleep (2)

def autoguardar (datos):
    from time import localtime,strftime
    carpeta = 'Guardar/'
    ID = strftime("%d%m%Y%H%M%S", localtime())
    while True:
        if not os.path.exists(carpeta+str(ID)+'.json'):
            guardar_json(carpeta+str(ID)+'.json',datos)
            break
        else:
            ID = strftime("%d%m%Y%H%M%S", localtime())
