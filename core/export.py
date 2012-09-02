# coding=UTF-8
'''Modulo de Exportación'''
import data.setup as s
from gen.habs import HabMod
from gen.dotes import ver_dotes
from core.prsnj import Pj as p
from core.config import guardar_json
from time import sleep
import os

def aplicar_mods (lista_dts, lista_habs, raciales, dotes, rangos):
    # Raciales
    for r in raciales:
        p.rcl[r[0]]+=r[1]

    # Por Dotes
    for d in dotes:
        if d.isnumeric():
            if 'Hab_dt' in lista_dts[int(d)]:
                for i in lista_dts[int(d)]['Hab_dt']:
                    p.dts[i]+=2
        elif ':' in d:
            d = d.split(':')
            if 'Hab_dt' in lista_dts[int(d[0])]:
                p.dts[int(d[1])] += 3
    
    # Por Objetos
    ## aún no implementado
    
    # Por sinergias
    for r in range(len(rangos)):
        if rangos[r] >= 5:
            if 'Sinergias' in lista_habs[r]:
                for i in lista_habs[r]['Sinergias']:
                    p.sng[i]+=2

def orden_habs_imprint (lista_habs,rangos,sinergia,dotes,racial,objetos):
    '''Ordena las habilidades que se van a imprimir.'''
    
    Orden = [rangos,sinergia,dotes,racial]
    indexes = []
    imprimir = ''
    
    for lista in Orden:
        for index in range(len(lista)):
            if lista[index]!= 0:
                if index not in indexes:
                    indexes.append(index)
    
    indexes.sort()
    
    # Eliminar las habilidades 'solo entrenadas' sin rangos
    
    for i in indexes:
        if rangos[i] == 0:
            if 'Solo_entrenada' in lista_habs[i]:
                x = indexes.index(i)
                del indexes[x]
    
    for h in indexes:
        imprimir = imprimir+s.HABS[h]['Nombre']+' +'+str(round(HabMod(h,lista_habs,p.CARS_mods,rangos,
                                                                  racial,sinergia,dotes,objetos)))+', '
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

def imprimir_clases (cla,CLASES):
    texto = ''
    clases = sorted([clase for clase in CLASES.keys()])
    for i in clases:
        if i in cla:
            texto += i+' '+str(cla.count(i))+'º '
    return texto

def exportar_pj():
    if input('\nDesea Exportar este personaje? ').lower().startswith('s'):
        nombre = input('\nNombre: ').capitalize()
        Pj = open('Personajes/'+nombre+'.txt','w')
        Pj.write('Nombre: '+nombre+'\n')
        Pj.write('Clase y nivel: '+imprimir_clases(p.cla,s.CLASES)+' AL '+s.alinieamientos[p.alini]+'\n')
        Pj.write('Tipo y Tamaño: Humanoide '+p.tam['Nombre']+' ('+p.subtipo+')\n')
        Pj.write('DG: '+imprimir_DG(p.cla,s.CLASES,p.CARS_mods[2],p.PG)+'\n')
        Pj.write('Iniciativa: +'+str(p.iniciativa)+'\nVelocidad: '+p.velocidad+'\n\n')
        Pj.write("Ataque base: +"+str(p.stats[0])+"\nPresa: +"+str(p.stats[0]+p.CARS_mods[0])+
                 "\n\nE/A: 5'/5'.\n\n\n")
        Pj.write('TS: Fortaleza +'+str(round(p.stats[1]))+', Reflejos +'+str(round(p.stats[2]))
                 +', Voluntad +'+str(round(p.stats[3]))+'.\n')
        Pj.write('Características: Fuerza '+str(p.CARS[0])+', Destreza '+str(p.CARS[1])+
                 ', Constitución '+str(p.CARS[2])+', Inteligencia '+str(p.CARS[3])+
                 ', Sabuduría ' + str(p.CARS[4])+', Carisma '+str(p.CARS[5])+
                 '.\nHabilidades y Dotes: '+orden_habs_imprint(s.HABS,p.rng,p.sng,p.dts,p.rcl,p.obj)+
                 ' '+', '.join(ver_dotes(p.dotes,s.DOTES,s.ARMAS,s.HABS,s.ESCUELAS))+'.')
        sleep(3)
        print('\nPersonaje Guardado')
        Pj.close()
    sleep (2)

def autoguardar (datos):
    carpeta = 'Guardar/reciente/'
    ID = 0
    while True:
        if not os.path.exists(carpeta+str(ID)+'.json'):
            guardar_json(carpeta+str(ID)+'.json',datos)
            break
        else:
            ID += 1