# coding=UTF-8
# habs.py
from func.core.lang import t,probar_input
from func.data.setup import data as s
from func.core.intro import imprimir_titulo
from func.core.prsnj import Pj as p
import func.gen.viz as v
import os
from random import choice

def elegir_habs (rangos,clase,nivel,HABS):
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
        imprimir_titulo()
        print (v.barra(p.CARS,s.alins[p.alini]['Abr'],p.raza['Nombre']))
        print(t('Seleccione sus Habiliades para este nivel'),end = '\n\n')
        print (t('¿Que desea hacer?'))
        op = v.subselector(t('Opción'),opciones)
        print()
        if op == 0: # Maximizar/actualizar habilidades
            if t('Nada más') in opciones:
                print ('\n'+t('Ya has repartido todos los rangos de habilidad disponibles.')+'\n')
            else:
                puntos = PuntHab(s.CLASES,clase,nivel,p.CARS['INT']['Mod'],p.subtipo,True)
                hab_cla = Claseas(s.CLASES,clase,HABS)
                if nivel == 1:
                    act = maximizar_habs(puntos,p.cla.count(clase),hab_cla,HABS)
                    hab_rng = act[0]
                    restante = act[1]
                else:
                    act = actualizar_habs_max (hab_rng,p.cla.count(clase),hab_cla,puntos,HABS)
                    hab_rng = act[0]
                    restante = act[1]
                
                if restante == 0:
                    opciones.append(t('Nada más'))
                else:
                    print('Se han repatido '+str(puntos-restante)+' puntos. Quedan '+str(restante)+' puntos.')

        elif op == 1: # Repartir rango por rango
            if t('Nada más') in opciones:
                print ('\n'+t('Ya has repartido todos los rangos de habilidad disponibles.')+'\n')
            else:
                hab_cla = Claseas(s.CLASES,clase,s.HABS)
                puntos = PuntHab (lista_de_clases,clase,nivel,p.CARS['INT']['Mod'],p.subtipo)
                hab_rng = repartir_rangos (puntos,p.cla.count(clase),hab_cla,HABS,hab_rng)
                if puntos <= 0:
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
            for i in v.a_dos_columnas(habs):
                print (i)

        elif op == 6: ## Nada más ##
            return hab_rng
        
        op = ''
        input(t('\n[Presione Enter para continuar]\n'))

def actualizar_habs_max (habs_pj,nv_cls,hab_cla,puntos,HABS):    
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    
    rng = {}
    for i in range(len(HABS)):
        rng[str(i)] = habs_pj[str(i)]['rng']
    
    #1: construye una lista con las habilidades previamente maximizadas (4 rangos en nivel 2)
    habs_max = sorted([i for i in habs_pj if habs_pj[i]['rng'] >= (rng_max-1)])
    
    #2: verifica que se tengan suficientes puntos para repartir 1 punto para cada habilidad.
    if not puntos == len(habs_max):
        #3: si lo anterior no se cumple (hay más puntos):
        prefs = habilidades_preferidas(habs_max,habs_pj,habs_cla,nv_cls,HABS,s.CARS)
        #3.1: utiliza el algoritmo de preferencia para elegir las habilidades más favorables
    else:
        prefs = habs_max *1
    
    for p in range(puntos):
        #3.2: elige aleatoriamente dentro de las habilidades con mayor preferencia
        h = choice(prefs)
        #4: con las habilidades previamente maximizadas elegidas, reparte los puntos.
        if not HABS[h]['Nombre'] in hab_cla:
            if rng[h] == rng_max_tc-0.5:
                rng[h]+= 0.5
                puntos -= 1
        else:
            if rng[h] == rng_max-1:
                rng[h]+=1
                puntos -= 1
        i = prefs.index(h)
        del prefs[i]
    
    rng_hab = []
    for i in range(len(HABS)):
        rng_hab.append(rng[str(i)])
    
    return rng_hab,puntos

def habilidades_preferidas(habs_max,habs_pj,habs_cla,nv_cls,HABS,CARS):
    '''Determina cuales son las habilidades con mayor prioridad para ser actualizadas'''
    
    prefs = {}
    for h in habs_max:
        prefs[h] = 0
    
    for hab in prefs:
        if HABS[hab]['Nombre'] in habs_cla:
            prefs[hab] += 1
        if 'Solo_entrenada' in HABS[hab]:
            prefs[hab] += 1
        if 'Sinergia' in HABS[hab]:
            prefs[hab] += 1
        if habs_pj[hab]['sng'] > 0:
            prefs[hab] += 1
        if CARS[HABS[hab]['Modificador']]['Mod'] > 0:
            prefs[hab] += CARS[HABS[hab]['Modificador']]['Mod']
        if habs_pj[hab]['rng'] == nv_cls+2:
            prefs[hab] += 1
    dev = []
    for h in prefs:
        dev.append(h)
    dev.sort()
    return dev

def maximizar_habs (puntos,nv_cls,hab_cla,HABS):
    
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    nom_hab = [HABS[str(i)]['Nombre'] for i in range(len(HABS))]
  
    rng = {}
    for h in nom_hab:
        rng[h] = 0
    
    if puntos > 0:
        print ('Escoge '+str(puntos)+ ' habilidades')
        while puntos > 0:
            hab = input('\n'+'Habilidad: ').strip(' ').capitalize()
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
    
    return rng_hab,puntos

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

def PuntHab (lista_de_clases,clase,nivel,INT_mod,subtipo,puntos = False):
    '''Devuelve los puntos de habilidad a repartir para el nivel de clase.'''
    
    PH = lista_de_clases[clase]['PH']+INT_mod
    if puntos != True:
        if nivel == 1:
            PH *= 4
            if subtipo == 'humano':
                PH += 4
        else:
            if subtipo == 'humano':
                PH += 1
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

def HabMod(hb,habs_pj,pen_armd,CARS,HABS):
    '''Calcula el modificador final de habilidad.'''

    mod = CARS[HABS[hb]['Modificador']]['Mod']
    pen = 0
    if 'Pen_armd' in HABS[hb]:
        pen = pen_armd * HABS[hb]['Pen_armd']
    
    total = sum(habs_pj[hb].values())+mod+pen
    
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

def HabcR (habs_pj,HABS,inverso=False):
    ''' Genera una lista de habiliades, solo si tienen rangos, lista para paginar.'''
    
    if type(habs_pj) == dict:
        rangos = []
        for i in range(len(HABS)):
            rangos.append(habs_pj[str(i)]['rng'])
    else:
        rangos = habs_pj
        
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
