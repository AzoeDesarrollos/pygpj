# coding=UTF-8
'''Modulo de Exportación'''
import prsnj as p
import setup as s
from func import HabMod
from time import sleep

def Aplicar_mods (lista_dts, lista_habs, raciales, dotes, rangos):
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

def OrdHabPrint (lista_habs,rangos,sinergia,dotes,racial,objetos):
    '''Ordena las habilidades que se van a imprimir.'''
    
    Orden = [rangos,sinergia,dotes,racial]
    indexes = []
    imprimir = ''
    
    for lista in Orden:
        for index in range(len(lista)):
            if lista[index]>0:
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

def imprimir_clases (cla_abr,CLASES):
    texto = ''
    clases = [CLASES[i]['Abr'] for i in range(len(CLASES))]
    for i in clases:
        if i in cla_abr:
            texto += i+' '+str(cla_abr.count(i))+'º '
    return texto

def imprimir_dotes (dotes_pj,DOTES,ARMAS,HABS,ESCUELAS):
    _dotes_ = [DOTES[i]['Nombre'] for i in range(len(DOTES))]
    _armas_ = [ARMAS[i]['Nombre'] for i in range(len(ARMAS))]
    _habs_ = [HABS[i]['Nombre'] for i in range(len(HABS))]
    imprimir = []
    for i in dotes_pj:
        if i.isnumeric():
            imprimir.append(_dotes_[int(i)])
        elif ':' in i:
            dt = int(i.split(':')[0])
            sub = int(i.split(':')[1])
            if mec[dt].split(':')[1] in ('m','w','w?'):
                imprimir.append(_dotes_[dt]+' ('+_armas_[sub]+')')
            elif mec[dt].split(':')[1] == 'h':
                imprimir.append(_dotes_[dt]+' ('+_habs_[sub]+')')
            elif mec[dt].split(':')[1] in ('e','e?'):
                imprimir.append(_dotes_[dt]+' ('+ESCUELAS[sub]+')')
    return ', '.join(imprimir)+'.'

def Guardar():
    if input('\nDeseas Guardar este personaje? ').lower().startswith('s'):
        nombre = input('\nNombre: ').capitalize()
        Pj = open('Personajes/'+nombre+'.txt','w')
        Pj.write('Nombre: '+nombre+'\n')
        Pj.write('Clase y nivel: '+imprimir_clases(p.clases,s.CLASES)+' AL '+s.alinieamientos[p.alini]+'\n')
        Pj.write('Tipo y Tamaño: Humanoide '+p.tam_nom+' ('+p.subtipo+')')
        Pj.write('DG: '+imprimir_DG(p.cla,s.CLASES,p.CARS_mods[2],p.PG)+'\n')
        Pj.write('Iniciativa: +'+str(p.iniciativa)+'\nVelocidad: '+p.velocidad+'\n\n')
        Pj.write("Ataque base: +"+str(p.stats[0])+"\nPresa: +"+str(p.stats[0]+p.CARS_mods[0])+
                 "\n\nE/A: 5'/5'.\n\n\n")
        Pj.write('TS: Fortaleza +'+str(round(p.stats[1]))+', Reflejos +'+str(round(p.stats[2]))
                 +', Voluntad +'+str(round(p.stats[3]))+'.\n')
        Pj.write('Características: Fuerza '+str(p.CARS[0])+', Destreza '+str(p.CARS[1])+
                 ', Constitución '+str(p.CARS[2])+', Inteligencia '+str(p.CARS[3])+
                 ', Sabuduría ' + str(p.CARS[4])+', Carisma '+str(p.CARS[5])+
                 '.\nHabilidades y Dotes: '+OrdHabPrint(s.HABS,p.rng,p.sng,p.dts,p.rcl,p.obj)+
                 ' '+imprimir_dotes(p.dotes,s.DOTES,s.ARMAS,s.HABS,s.ESCUELAS))
        sleep(3)
        print('\nPersonaje Guardado')
        Pj.close()
    print ('Gracias')
    sleep (2)

def autoguardar ():
    pass