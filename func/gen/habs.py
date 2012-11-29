# coding=UTF-8
# habs.py
from func.core.lang import t,probar_input
from func.data.setup import data as s
from func.core.intro import imprimir_titulo
from func.core.prsnj import Pj as p
import func.gen.viz as v
import os

def elegir_habs (PH_cls,rangos,HABS,clase,PH):
    '''Proporciona un más completo selector de habilidades.'''
    
    opciones = [t('Maximizar/actualizar habilidades'),
                t('Repartir rango por rango'),
                t('Ver las habilidades que tienen rangos'),
                t('Ver las habilidades que no tienen rangos'),
                t('Ver las habilidades de clase'),
                t('Ver una lista de todas las habilidades')]
    op = ''
    hab_rng = rangos
    while op == '':
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (v.barra(p.CARS,s.alinis[p.alini],p.raza['Nombre']))
        print(t('Seleccione sus Habiliades para este nivel'),end = '\n\n')
        print (t('¿Que desea hacer?'))
        op = v.subselector(t('Opción'),opciones)
        print()
        if op == 0: # Maximizar/actualizar habilidades
            if t('Nada más') in opciones:
                print ('\n'+t('Ya has repartido todos los rangos de habilidad disponibles.')+'\n')
            else:
                hab_rng = maximizar_habs(PH_cls,p.CARS_mods[3],Claseas(s.CLASES,clase,s.HABS),
                                         s.HABS,hab_rng,p.cla.count(clase),p.subtipo)
                opciones.append(t('Nada más'))
        elif op == 1: # Repartir rango por rango
            if t('Nada más') in opciones:
                print ('\n'+t('Ya has repartido todos los rangos de habilidad disponibles.')+'\n')
            else:
                hab_rng = repartir_rangos (PH,p.cla.count(clase),Claseas(s.CLASES,clase,s.HABS),
                                           s.HABS,hab_rng)
                opciones.append(t('Nada más'))
        elif op == 2: # Ver las habilidades que tienen rangos
            lineas = v.a_dos_columnas(HabcR (hab_rng,HABS))
            if len(lineas) == 0:
                print ('\n'+t('Ninguna habilidad tiene rangos por el momento'))
            else:
                for i in lineas:
                    print (i)
        elif op == 3: # Ver las habilidades que no tienen rangos
            for i in v.a_dos_columnas(HabcR (hab_rng,HABS,inverso=True)):
                print (i)
        elif op == 4: # Ver las habilidades de clase
            for i in v.a_dos_columnas(Claseas(s.CLASES,clase,s.HABS)):
                print (i)        
        elif op == 5: # Ver una lista de todas las habilidades
            habs = [HABS[str(i)]['Nombre'] for i in range(len(s.HABS))]
            del habs[-1]
            for i in v.a_dos_columnas(habs):
                print (i)
        elif op == 6: ## Nada más ##
            return hab_rng
        
        op = ''
        input(t('\n[Presione Enter para continuar]\n'))

def maximizar_habs (PH_cls,INT_mod,hab_cla,HABS,rangos,nv_cls,subtipo):
    '''Maximiza o actualiza las habilidades maximizadas del nivel anterior.'''
    
    nom_hab = [HABS[str(i)]['Nombre'] for i in range(len(HABS))]
    puntos = PH_cls + INT_mod
    if subtipo == 'humano':
        puntos += 1
    anterior = puntos
    
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    idiomas = []
    
    pool = 0
    for i in range(len(rangos)):
        if not HABS[str(i)]['Nombre'] in hab_cla:
            pool += rangos[i]*2
        else:
            pool += rangos[i]
    pool = pool/(rng_max-1)
    if pool == puntos:
        for i in range(len(rangos)):
            if not HABS[str(i)]['Nombre'] in hab_cla:
                if rangos[i] == rng_max_tc-0.5:
                    rangos[i]+= 0.5
                    puntos -= 1
            else:
                if rangos[i] == rng_max-1:
                    rangos[i]+=1
                    puntos -= 1
        if puntos == 0:
            print ('\nSe han actualizado todas las habilidades previamente maximizadas.\n')
        elif puntos == anterior:
            print ('\nNo se han encontrado habilidades maximizadas para actualizar.\n')
        else:
            print ('\nSe han actualizado sólo las habilidades previamente maximizadas.\n')
    
    rng = {}
    for i in range(len(rangos)):
        rng[HABS[str(i)]['Nombre']] = rangos[i]
    
    if puntos >0:
        print ('Escoge '+str(puntos)+ ' habilidades')
        while puntos > 0:
            hab = input('\nHabilidad: ').strip(' ').capitalize()
            hab = probar_input (hab,nom_hab)
            if hab == '':
                print(t('Escriba el nombre de una habilidad'))
            elif hab not in hab_cla:
                if rng[hab] == rng_max_tc:
                    print (hab+' está maximizada. No se pueden agregar más rangos en este nivel')
                else:
                    puntos -= 1
                    rng[hab] += rng_max_tc - rng[hab]
            else:
                if rng[hab] == rng_max:
                    print (hab+' está maximizada. No se pueden agregar más rangos en este nivel')
                else:
                    puntos -= 1
                    rng[hab] += rng_max - rng[hab]
                        
            if hab == 'Hablar un idioma':
                p.idiomas = nuevos_idiomas(s.IDIOMAS,p.idiomas,round(rng[hab]))
        
    rng_hab = []
    for i in range(len(nom_hab)):
        if nom_hab[i] in rng:
            rng_hab.append(rng[nom_hab[i]])
    
    return rng_hab

def repartir_rangos (PH,nv_cls,hab_cla,HABS,rangos):
    '''Reparte los puntos de habilidad manualmente, uno por uno.'''
    
    print('\nTienes '+str(PH)+' puntos de habilidad para distribuir en este nivel.\n')

    print ('\nRecuerda que cualquier habilidad transclásea cuesta dos puntos en lugar de uno.',
           'Escribe una habilidad, y luego los puntos de habilidad que desees invertir en','ella.',
           sep='\n')
    
    rng = {}
    for i in range(len(rangos)):
        rng[HABS[str(i)]['Nombre']] = rangos[i]
    
    nom_hab = [HABS[str(i)]['Nombre'] for i in range(len(HABS))]
    
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    while PH > 0:
        hab = ''
        while hab == '':
            hab = input('\nHabilidad: ').strip(' ').capitalize()
            hab = probar_input (hab,nom_hab)
            if hab == '':
                print ('\nDebe elegir una habilidad')
            
        if rng[hab] >0:
            print (hab+' ya posee '+str(rng[hab])+' rangos.')
        
        puntos = ''
        while puntos == '':
            puntos = input('Puntos: ')
            if not puntos.isnumeric():
                print ('Los rangos deben ser numéricos')
                puntos = ''
            elif int(puntos) > PH:
                print('No posees tantos puntos de habilidad')
                puntos = ''
            else:
                puntos = int(puntos)
                        
        if hab not in hab_cla:                                     ## Habilidad Transclásea
            print (hab+' es una habilidad transclásea')
            if rng[hab] == rng_max_tc:
                print (hab+' está maximizada. No se pueden agregar más rangos en este nivel')
            else:
                if rng[hab] + (puntos/2) >= rng_max_tc:
                    print(hab+' ha alcanzado el rango máximo ('+str(rng_max_tc)+').')
                    PH -= (rng_max_tc - rng[hab])*2
                    rng[hab] += rng_max_tc - rng[hab]
                else:
                    PH -= puntos
                    rng[hab] += puntos/2
                print('\nPuntos restantes: '+str(int(PH)))
            
        else:                                                     ## Habilidad Clásea
            print (hab+' es una habilidad clásea')
            if rng[hab] == rng_max:
                print (hab+' está maximizada. No se pueden agregar más rangos en este nivel')
            else:
                if rng[hab] + puntos >= rng_max:
                    print(hab+' ha alcanzado el rango máximo ('+str(rng_max)+').')
                    PH -= rng_max - rng[hab]
                    rng[hab] += rng_max - rng[hab]
                else:
                    PH -= puntos
                    rng[hab] += puntos
                print('\nPuntos restantes: '+str(int(PH)))
        
        if hab == 'Hablar un idioma':
            p.idiomas = nuevos_idiomas(s.IDIOMAS,p.idiomas,round(rng[hab]))
    
    rng_hab = []
    for i in range(len(nom_hab)):
        if nom_hab[i] in rng:
            rng_hab.append(rng[nom_hab[i]])
    
    return rng_hab

def PuntHab (lista_de_clases,clase,nivel,INT_mod,subtipo):
    '''Devuelve los puntos de habilidad a repartir para el nivel de clase.'''
    
    PH = lista_de_clases[clase]['PH']+INT_mod
    if nivel == 1:
        PH *= 4
        if subtipo == 'humano':
            PH += 4
    else:
        if subtipo == 'humano':
            PH += 1
    return PH

def Claseas (CLASES,clase,HABS):
    '''Devuelve las habilidades cláseas de la clase citada.'''
    
    cls = []
    for i in CLASES[clase]['Claseas']:
        cls.append(HABS[str(i)]['Nombre'])
    return cls

def HabMod(hb,HABS,CARS_mods,rangos, raciales, sinergias, dotes, objetos,pen_armd):
    '''Calcula el modificador final de habilidad.'''
    if 'Modificador' not in HABS[hb]:
        return None
    else:
        mod = CARS_mods[HABS[hb]['Modificador']]
        pen = 0
        if 'Pen_armd' in HABS[hb]:
            pen = pen_armd * HABS[hb]['Pen_armd']
        
        hb = int(hb)
        total = rangos[hb]+mod+raciales[hb]+sinergias[hb]+dotes[hb]+objetos[hb]+pen
        
        return total

def nuevos_idiomas (IDIOMAS,idi_pj,pool):
    lista = []
    for i in idi_pj:
        lista.append(IDIOMAS[i])
    print ('Sus idiomas actuales son: '+', '.join(lista)+'.'+
           '\nPuede elegir '+str(pool)+' idiomas nuevos, de entre los siguientes:\n')
    posibles = []
    for i in range(len(IDIOMAS)):
        if i not in idi_pj:
            posibles.append(IDIOMAS[i])

    sels = v.subselector ('Idioma',posibles,dos_col=True,vueltas=pool)
    if type(sels) == list:
        for i in sels:
            idi_pj.append(IDIOMAS.index(posibles[i]))
    else:
        idi_pj.append(IDIOMAS.index(posibles[sels]))
    
    idi_pj.sort()
    return idi_pj

def HabcR (rang,HABS,inverso=False):
    ''' Genera una lista de habiliades, solo si tienen rangos, lista para paginar.'''
    
    if type(rang) == dict:
        rangos = []
        for i in range(len(HABS)):
            rangos[i] = rang[HABS[str(i)]['Nombre']]
    else:
        rangos = rang
        
    cR = []
    nombres = [HABS[str(i)]['Nombre'] for i in range(len(HABS))]
    if inverso == True:
        for i in range(len(rangos)):
            if rangos[i] == 0:
                cR.append(nombres[i])
    else:
        for i in range(len(rangos)):
            if rangos[i] > 0:
                cR.append(nombres[i]+' '+str(rangos[i]))

    return cR