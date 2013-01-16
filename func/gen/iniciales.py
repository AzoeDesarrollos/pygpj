# coding=UTF-8
# iniciales.py
from random import randint
from math import floor
from func.core.lang import t,probar_input
from func.core.viz import subselector
from func.core.intro import imprimir_titulo

def elegir_raza(RAZAS):
    '''Provee un selector de razas.'''
    
    razas = [RAZAS[str(i)]['Nombre'] for i in range(len(RAZAS))]

    print('\n'+t('Seleccione Raza'))
    for i in range(len(RAZAS)):
        if (i+1) % 4 == 0:
            print(str(i+1)+': '+razas[i],end = '\n')
        else:
            print(str(i+1)+': '+razas[i],end = ' ')
    
    raza = ''
    while raza == '':
        r = input('\n\n'+t('Raza: '))
        if r.isnumeric():
            r = int(r)
            if not 1 <= r <= len(RAZAS):
                print(t('Raza inválida, intente nuevamente'))
                continue
            else:
                r -= 1
        else:
            r = probar_input(r,razas)
            if r == '':
                print(t('Raza inválida o error ortográfico, intente nuevamente'))
                continue
            else:
                r = razas.index(r)
        print (t('Has elegido que este personaje sea')+' '+t('un '+razas[r])+'.', end = ' ')
        if input (t('¿Estas seguro? ')).lower().startswith(t('s')):
            return str(r)

def elegir_alineamiento (Alineamientos):
    '''Provee un selector de alineamientos.'''
    
    imprimir_titulo()
    print(t('Escoge un alineamiento para este personaje')+'\n')
    alinis = []
    for i in Alineamientos:
        print (str(i)+': '+t(Alineamientos[i]['Nom']))
        alinis.append(Alineamientos[i]['Nom'])
            
    while True:
        aling = input ('\n'+t('Alineamiento')+': ')
        if aling.isnumeric():
            aling = int(aling)
            if aling not in range(len(Alineamientos)):
                print(t('El numero elegido no representa ningún alineamiento'))
            else:
                print (t('Has elegido que este personaje sea ')+Alineamientos[aling]['Nom']+'.', end= ' ')
                if input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                    return aling
        else:
            if aling.capitalize() in alinis:
                aling = int(alinis.index(aling.capitalize()))
                print (t('Has elegido que este personaje sea ')+t(Alineamientos[aling]['Nom'])+'.', end= ' ')
                if input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                    return aling

def elegir_clase(claseprevia,CLASES,alineamiento):
    '''Provee un selector de clases.'''
    
    # genera dos listas con los nombres y abreviaturas compatibles con el alineamiento
    nom,abr = [],[]
    for i in range(len(CLASES)):
        if alineamiento in CLASES[str(i)]['Alineamientos']:
            nom.append(CLASES[str(i)]['Nombre'])
            abr.append(CLASES[str(i)]['Abr'])
    
    # genera un string que muestra las clases disponibles numeradas a partir de 0
    imprimir = ''
    for i in range(len(nom)):
        if (i+1)%4==0 and nom[i]!=nom[-1]:
            imprimir += str(i)+': '+nom[i]+'\n'
        else:
            imprimir += str(i)+': '+nom[i]+' '

    print (t('Elija una clase para este nivel'), end = ' ')
    if claseprevia != '':
        # claseprevia es la clase elegida en el nivel anterior.
        print ('[Enter: '+claseprevia+']')
        # presionando enter se autoelige esa clase, acelerando el proceso
    
    print ('\n\n'+t('Las clases disponibles según el alineamiento son')+': \n'+imprimir)
   
    cla = '?'
    while True:
        while cla == '?':
            cla = input('\n'+'Clase: ').capitalize()
            if cla == '':
                if claseprevia == '':
                    print ('\n'+t('Debe seleccionar una clase'))
                    cla = '?'
                else:
                    # si hubo una clase previa, entonces '' es esa clase.
                    cla = nom.index(claseprevia)
            elif cla.isnumeric():
                cla = int(cla)
                if not 0 <= cla <= len(nom):
                    print(t('Seleccione una clase válida.'))
                    cla = '?'
            elif cla in abr:
                cla = abr.index(cla)
            else:
                cla = probar_input()
                if cla == '':
                    print ('\n'+t('Seleccione una clase válida.'))
                    cla = '?'
                else:
                    cla = nom.index(cla)

        print (t("Has seleccionado '")+nom[cla]+t("' como clase para este nivel."),end= ' ')
        if not input (t('¿Estas seguro? ')).lower().startswith(t('s')):
            cla = '?'
        else:
            for Clase in CLASES:
                if nom[cla] == CLASES[Clase]['Nombre']:
                    break
            break
    
    return str(Clase)

def idiomas_iniciales (IDIOMAS,Clase,Raza,pool):
    
    lang = [IDIOMAS[str(i)]['Nombre'] for i in range(len(IDIOMAS))]
    
    autos = []
    adics = []
    nom = Clase['Nombre']
    for i in Raza['Idioma_auto']:
        autos.append(lang[i])
    for i in Raza['Idioma_adic']:
        adics.append(lang[i])
    
    if 'Idiomas' in Clase:
        idi_clas = Clase['Idiomas']
        for i in idi_clas:
            if lang[i] not in adics:
                adics.append(lang[i])
    print ('\n'+t('Los idiomas automáticos de tu raza son: ')+','.join(autos)+'.')
    
    idiomas = []
    if pool > 0:
        print ('\n'+t('Además, tu personaje puede conocer ')+str(pool)+
               t(' idiomas adicionales')+'.\n'+t('Eligelos de la siguiente lista:'))
        elecs = subselector (t('Idioma'),adics,dos_col=True,vueltas=pool)
        if type(elecs) == list:
            for i in elecs:
                idiomas.append(lang.index(adics[i]))
        else:
            idiomas.append(lang.index(adics[elecs]))
    
    for i in autos:
        idiomas.append(lang.index(i))

    idiomas.sort()
    
    input (t('\n[Presione Enter para continuar]\n'))
    return idiomas

def procesar_clase(Clase,nv_cls,stats):
    '''Procesa la lista de clases y obtiene ATKbase, y TSs.'''
    
    def calcular_TS (TScls,nv_cls):
        if TScls == 'b':
            TS = 1/2
            if nv_cls == 1:
                TS += 2
        else:
            TS = 1/3
        
        return TS
    
    if Clase['ATKb'] == 'b':
        A = 1
    elif Clase['ATKb'] == 'i':
        A = 3/4
    else:
        A = 1/2
    A = floor(A+stats['AtqB'])
    F = floor(calcular_TS (Clase['Fort'],nv_cls)+stats['TSFort'])
    R = floor(calcular_TS (Clase['Ref'],nv_cls)+stats['TSRef'])
    V = floor(calcular_TS (Clase['Vol'],nv_cls)+stats['TSVol'])
    
    bases = [A,F,R,V]
    return bases

def Competencias (clase,comprevia):
    '''Actualiza las competencias en armas o armaduras del personaje.'''
    
    for item in clase:
        if item not in comprevia:
            comprevia.append(item)

    comprevia.sort()
    
    return comprevia

def oro_inicial (clase,CLASES):
    cant = CLASES[clase]['po'][0]
    mult = CLASES[clase]['po'][1]
    po = randint(cant,cant*4)*mult

    return po