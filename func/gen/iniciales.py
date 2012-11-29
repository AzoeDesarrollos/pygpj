# coding=UTF-8
# iniciales.py
from random import randint
from func.core.lang import t
from func.gen.viz import subselector

def elegir_raza(RAZAS):
    '''Provee un selector de razas.'''
    
    razas = [RAZAS[str(i)]['Nombre'] for i in range(len(RAZAS))]    

    print('\n'+t('Seleccione Raza')+'\n1: '+razas[0]+' 2: '+razas[1]+' 3: '+razas[2]
          +' 4: '+razas[3]+'\n5: '+razas[4]+' 6: '+razas[5]+' 7: '+razas[6])
    
    raza = ''
    while raza == '':
        raza = input('\n'+t('Raza')+': ').capitalize()
        if raza.isnumeric():
            raza = int(raza)
            if raza not in range(1,len(razas)):
                print(t('Raza inválida, intente nuevamente'))
                raza = ''
            else:
                key = razas[raza-1]
                print (t('Has elegido que este personaje sea ')+t('un '+key)+'.', end = ' ')
                if not input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                    raza = ''
                else:
                    return RAZAS[str(raza-1)]
        elif raza not in razas:
            print(t('Raza inválida o error ortográfico, intente nuevamente'))
            raza = ''
        else:
            print (t('Has elegido que este personaje sea')+' un '+raza+'.', end = ' ')
            if not input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                raza = ''
            else:
                return RAZAS[str(razas.index(raza))]

def elegir_alineamiento (Alineamientos):
    '''Provee un selector de alineamientos.'''
    
    print('\n'+t('Escoge un alineamiento para este personaje'))
    for i in range(len(Alineamientos)):
        print (str(i)+': '+t(Alineamientos[i]))
            
    while True:
        aling = input ('\n'+t('Alineamiento')+': ')
        if aling.isnumeric():
            aling = int(aling)
            if aling not in range(len(Alineamientos)):
                print(t('El numero elegido no representa ningún alineamiento'))
            else:
                print (t('Has elegido que este personaje sea ')+Alineamientos[aling]+'.', end= ' ')
                if input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                    return aling
        else:
            if aling.capitalize() in Alineamientos:
                aling = int(Alineamientos.index(aling.capitalize()))
                print (t('Has elegido que este personaje sea ')+t(Alineamientos[aling])+'.', end= ' ')
                if input (t('¿Estas seguro? ')).lower().startswith(t('s')):
                    return aling

def elegir_clase(claseprevia,CLASES,alineamiento):
    '''Provee un selector de clases.'''
    
    nom = [CLASES[str(i)]['Nombre'] for i in range(len(CLASES))]
    abr = [CLASES[str(i)]['Abr'] for i in range(len(CLASES)) if CLASES[str(i)]['Nombre'] == nom[i]]
    ali = [CLASES[str(i)]['Alineamientos'] for i in range(len(CLASES)) if CLASES[str(i)]['Nombre'] == nom[i]]
    pos = []
    abp = []
    for i in range(len(ali)):
        if alineamiento in ali[i]:
            pos.append(nom[i])
            abp.append(abr[i])

            
    imprimir = ''
    numeros = []
    for i in range(len(pos)):
        if (i+1)%4==0:
            imprimir += str(i)+': '+pos[i]+'\n'
        else:
            imprimir += str(i)+': '+pos[i]+' '
        numeros.append(str(i))
        
    if claseprevia == '':
        print (t('Elija una clase para este nivel'))
    else:
        print (t('Elija una clase para este nivel')+' [Enter: '+claseprevia+']')
    print ('\n'+t('Las clases disponibles según el alineamiento son')+': \n'+imprimir)
   
    CLASES = ['Barbaro','Clerigo','Paladin','Picaro','']+numeros+pos+abp
    cla = '?'
    while True:
        while cla == '?':
            cla = input('\nClase: ').capitalize()
            if cla not in CLASES:
                print ('\n'+t('Seleccione una clase válida.'))
                cla = '?'
            elif cla == '':
                if claseprevia == '':
                    print ('\n'+t('Debe seleccionar una clase'))
                    cla = '?'
                else:
                    cla = claseprevia
            
        if cla in abr: Clase = abr.index(cla)
        elif cla.capitalize() in nom: Clase = nom.index(cla)
        elif cla == '': Clase = ''
        elif cla == 'Barbaro': Clase = abr.index('Brb')
        elif cla == 'Clerigo': Clase = abr.index('Clr')
        elif cla == 'Paladin': Clase = abr.index('Pld')
        elif cla == 'Picaro': Clase = abr.index('Pcr')
        elif cla.isnumeric(): Clase = abr.index(abp[int(cla)])
            
        print (t("Has seleccionado '")+nom[Clase]+t("' como clase para este nivel."),
               end= ' ')
        if not input (t('¿Estas seguro? ')).lower().startswith(t('s')):
            cla = '?'
        else:
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
    return idiomas

def procesar_clase(Clase,nv_cls,stats):
    '''Procesa la lista de clases y obtiene ATKbase, y TSs.'''
    
    if Clase['ATKb'] == 'b':
        A = 1
    elif Clase['ATKb'] == 'i':
        A = 3/4
    else:
        A = 1/2
    
    if Clase['Fort'] == 'b':
        F = 1/2
        if nv_cls == 1:
            F += 2
    else:
        F = 1/3
    
    if Clase['Ref'] == 'b':
        R = 1/2
        if nv_cls == 1:
            R += 2
    else:
        R = 1/3
    
    if Clase['Vol']== 'b':
        V = 1/2
        if nv_cls == 1:
            V += 2
    else:
        V = 1/3
    
    bases = [A,F,R,V]
    for i in range(len(bases)):
        bases[i]+=stats[i]
    
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