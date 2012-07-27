# coding=UTF-8
import func as f
import setup as s
import prsnj as p
from time import sleep
import os

def SelRaza(lista_de_razas):
    '''Provee un selector de razas.'''
    
    print('\nSeleccione Raza \n1: Humano 2: Elfo 3: Enano 4: Gnomo\n5: Mediano 6: Semielfo 7: Semiorco')

    raza = ''
    while raza not in lista_de_razas:
        raza = input('\nRaza: ').capitalize()
        if raza.isnumeric():
            if int(raza) not in (1,2,3,4,5,6,7):
                print('Raza inválida, intente nuevamente')
            else:
                if raza == '1': raza = 'Humano'
                elif raza == '2': raza = 'Elfo'
                elif raza == '3': raza = 'Enano'
                elif raza == '4': raza = 'Gnomo'
                elif raza == '5': raza = 'Mediano'
                elif raza == '6': raza = 'Semielfo'
                elif raza == '7': raza = 'Semiorco'
                print ('Has elegido que este personaje sea un '+lista_de_razas[raza]['Nombre']+'.', end = ' ')
                if not input ('¿Estas seguro? ').lower().startswith('s'):
                    raza = ''
                else:
                    return lista_de_razas[raza]
        elif raza not in lista_de_razas:
            print('Raza inválida o error ortográfico, intente nuevamente')
        else:
            print ('Has elegido que este personaje sea un '+lista_de_razas[raza]['Nombre']+'.', end = ' ')
            if not input ('¿Estas seguro? ').lower().startswith('s'):
                raza = ''
            else:
                return lista_de_razas[raza]

def RepPunto(lista,Car):
    '''Ordena la distribución de valores de característica.'''
    
    CarVal = 0
    while CarVal == 0:
        entrada = input(Car+': ')
        if not entrada.isdigit():
            print('Por favor ingrese sólo números\n')
        elif int(entrada) not in lista:
            print('No hay tiradas con ese valor\n')
        else:
            CarVal = int(entrada)
            del lista[lista.index(int(entrada))]
    return CarVal

def Alinear ():
    '''Provee un selector de alineamientos.'''
    
    Alineamientos = ('Legal bueno','Neutral bueno','Caótico bueno',
                     'Legal neutral','Neutral auténtico','Neutral bueno',
                     'Legal maligno','Neutral maligno','Caótico maligno')
    print('\nEscoge un alineamiento para este personaje')
    for i in range(len(Alineamientos)):
        if (i+1)%3==0:
            print(str(i)+': '+Alineamientos[i],end='\n')
        elif i == 0:
            print(str(i)+': '+Alineamientos[i],end='\t\t')
        else:
            print(str(i)+': '+Alineamientos[i],end='\t')
    while True:
        aling = input ('\nAlineamiento: ')
        if aling.isnumeric():
            aling = int(aling)
            if aling not in range(len(Alineamientos)):
                print('El numero elegido no representa ningún alineamiento')
            else:
                print ('Has elegido que este personaje sea '+Alineamientos[aling]+'.', end= ' ')
                if input ('¿Estas seguro? ').lower().startswith('s'):
                    return aling
        else:
            if aling.capitalize() in Alineamientos:
                aling = int(Alineamientos.index(aling.capitalize()))
                print ('Has elegido que este personaje sea '+Alineamientos[aling]+'.', end= ' ')
                if input ('¿Estas seguro? ').lower().startswith('s'):
                    return aling

def SelCla(claseprevia,lista_de_clases,alineamiento):
    '''Provee un selector de clases.'''

    abr = [lista_de_clases[i]['Abr'] for i in range(len(lista_de_clases))]
    nom = [lista_de_clases[i]['Nombre'] for i in range(len(lista_de_clases))]
    ali = [lista_de_clases[i]['Alineamientos'] for i in range(len(lista_de_clases))]
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
        print ('Elije una clase para este nivel')
        print ('\nLas clases disponibles según el alineamiento son: \n'+imprimir)
    else:
        print ('Elije una clase para este nivel [Enter: '+claseprevia+']')
        print ('\nLas clases disponibles según el alineamiento son: \n'+imprimir)
   
    CLASES = ['Barbaro','Clerigo','Paladin','Picaro','']+numeros+pos+abp
    cla = '?'
    while True:
        while cla == '?':
            cla = input('\nClase: ').capitalize()
            if cla not in CLASES:
                print ('\nSeleccione una clase válida.')
                cla = '?'
            elif cla == '':
                if claseprevia == '':
                    print ('\nDebe seleccionar una clase')
                    cla = '?'
                else:
                    cla = claseprevia
            
        if cla in abr: Clase = abr.index(cla)
        elif cla.capitalize() in nom: Clase = nom.index(cla)
        elif cla == '': Clase = ''
        elif cla == 'Barbaro': Clase = 0
        elif cla == 'Clerigo': Clase = 2
        elif cla == 'Paladin': Clase = 9
        elif cla == 'Picaro': Clase = 10
        elif cla.isnumeric(): Clase = abr.index(abp[int(cla)])
            
        print ("Has seleccionado '"+nom[Clase]+"' como clase para este nivel.",end= ' ')
        if not input ('¿Estas seguro? ').lower().startswith('s'):
            cla = '?'
        else:
            break
    
    return Clase

def AumentaCar (nivel):
    CARS = ('FUE','DES','CON','INT','SAB','CAR','Fuerza','Destreza',
            'Constitución','Constitucion','Inteligencia','Sabiduría','Sabiduria','Carisma')

    print ('\nEn el '+str(nivel)+'º nivel, tienes un aumento de características')
    print ('Selecciona la característica que quieres aumentar')
    Car = input('Característica: ')
    while True:
        if Car.capitalize() not in CARS:
            if Car.upper() not in CARS:
                print ('La característica es inválida o inexistente')
                Car = input('Característica: ')
            else:
                break
        else:
            break
    if len(Car) > 3:
        Car = Car.capitalize()
        if Car in ('Fuerza'): Car = 0
        elif Car in ('Destreza'): Car = 1
        elif Car in ('Constitución','Constitucion'): Car = 2
        elif Car in ('Inteligencia'): Car = 3
        elif Car in ('Sabiduría','Sabiduria') : Car = 4
        elif Car in ('Carisma'): Car = 5
    else:
        Car = Car.upper()
        if Car == 'FUE': Car = 0
        elif Car == 'DES': Car = 1
        elif Car == 'CON': Car = 2
        elif Car == 'INT': Car = 3
        elif Car == 'SAB': Car = 4
        elif Car == 'CAR': Car = 5
    
    return Car

def RepRNG (PH,nv_cls,hab_cla,lista_de_hab,rangos):
    '''Devuelve un diccionario con la habilidad y sus rangos.'''
    
    print('\nTienes '+str(PH)+' puntos de habilidad para distribuir en este nivel.\n')
    
    if input('Deseas conocer tus habilidades de clase? ').lower().startswith('s'):
        print(f.PrepPrint(hab_cla))

    print ('\nRecuerda que cualquier habilidad transclásea cuesta dos puntos en lugar de uno.',
           'Escribe una habilidad, y luego los puntos de habilidad que desees invertir en','ella',sep='\n')
    
    rng = {}
    for i in range(len(rangos)):
        rng[lista_de_hab[i]['Nombre']] = rangos[i]
    nom_hab = []
    for i in range(len(lista_de_hab)):
        nom_hab.append(lista_de_hab[i]['Nombre'])
    
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    idiomas = []
    while PH > 0:
        hab = input('\nHabilidad: ').strip(' ').capitalize()
        while hab not in nom_hab:
            print('Por favor, escribe la habilidad correctamente')
            hab = input('\nHabilidad: ').rstrip(' ').capitalize()
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
                print('\nPuntos restantes: '+str(PH))
            
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
                print('\nPuntos restantes: '+str(PH))
        
        if hab == 'Hablar un idioma':
            idiomas = NuevosIdiomas(s.IDIOMAS,p.idiomas,round(rng[hab]))
    
    rng_hab = {}
    for i in range(len(nom_hab)):
        if nom_hab[i] in rng:
            rng_hab[i] = rng[nom_hab[i]]
    
    input ('\n[Presione Enter para continuar]')
    return rng_hab,idiomas

def SelDot (nivel,dotes_pj,lista_de_dotes,comp_armas,ARMAS,lista_de_habilidades,spec,clase,*dotes_clase):
    '''Provee un selector de dotes.'''
    
    nom = [lista_de_dotes[i]['Nombre'] for i in range(len(lista_de_dotes))]
    des = [lista_de_dotes[i]['Descripcion'] for i in range(len(lista_de_dotes))]
    mec = [lista_de_dotes[i]['Tipo'] for i in range(len(lista_de_dotes))]
    pre = []
    for i in range(len(lista_de_dotes)):
        if 'PreReq' in lista_de_dotes[i]:
            pre.append(lista_de_dotes[i]['PreReq'])
        else:
            pre.append('')
    
    
    if spec == False:
        print ('\nEn el '+str(nivel)+'º nivel, tienes una dote para elegir.\n')
        posibles = f.GenerarListadeAyuda(f.AutoDot(lista_de_dotes,comp_armas,ARMAS,
                                                   lista_de_habilidades),lista_de_dotes)
    else:
        print ('\nComo aptitud de clase, en este nivel tienes una dote adicional para elegir.\n')
        posibles = f.GenerarListadeAyuda(f.AutoDot(lista_de_dotes,comp_armas,ARMAS,
                                                   lista_de_habilidades,sub=dotes_clase[0]),
                                         lista_de_dotes)
    
    print ('Escribe el nombre de la dote elegida. Si deseas información sobre una dote en',
           'particular, escribe <dote>?. Si deseas información sobre todas las dotes', 'escribe *?.'
           ,sep = '\n')
    
    dote = ''
    while dote == '':
        dt = input('\nDote: ').strip().capitalize()
        if '?' in dt:
            if '?' not in dt[-1]:
                print ('Por favor, escribe el comando correctamente\n')
            elif dt == '*?':
                lineas = []
                for ID in posibles:
                    if pre[ID] != '':
                        lineas.append(nom[ID]+'\nPrerrequisitos: '+pre[ID]+'\nBeneficio: '+des[ID]+'\n')
                    else:
                        lineas.append(nom[ID]+'\nBeneficio: '+des[ID]+'\n')
                f.paginar(5,lineas)
            elif dt.split('?')[0] not in nom:
                print ('Por favor, escribe la dote correctamente\n')
            else:
                dt = dt.split('?')[0]
                print (nom[nom.index(dt)])
                if nom.index(dt) not in posibles:
                    print ('Prerrequisitos: '+pre[nom.index(dt)]+'(no cumplidos)')
                else:
                    print ('Prerrequisitos: '+pre[nom.index(dt)])
                print('Beneficio: '+des[nom.index(dt)])
        elif dt not in nom:
            print ('Por favor, escribe la dote correctamente\n')
        elif nom.index(dt) not in posibles:
            print ('Actualmente el personaje no cumple con los prerrequisitos para la dote seleccionada',
                   'Elija otra', sep = '\n')
            print ('Prerrequisitos: '+pre[nom.index(dt)])
        
        elif mec[nom.index(dt)] == 'u:w':
            print ('Para la dote seleccionada debes elegir un arma con la que seas competente',
                   'Elije una: ', sep = '\n')
            armas = []
            for i in comp_armas:
                if  str(nom.index(dt))+':'+str(i) not in dotes_pj:
                    armas.append(ARMAS[i]['Nombre'])
            
            arma = subselector('Arma',armas,dos_col=True)
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
            for i in range(len(ARMAS)):
                if ARMAS[i]['Nombre'] == armas[arma]:
                    dote = str(nom.index(dt))+':'+str(i)
        
        elif mec[nom.index(dt)] == 'u:w?':
            print ('Para la dote seleccionada debes elegir un arma de entre las siguientes',
                   'Elije una',sep = '\n')
            subs = f.AutoDot(lista_de_dotes,comp_armas,ARMAS,
                             lista_de_habilidades,sub=[nom.index(dt)])
            armas = []
            for ID in subs:
                if f.ValPreReq(ID,lista_de_dotes,p.clases,nivel,
                               dotes_pj,p.rng,p.apps,p.stats,p.CARS,comp_armas):
                    armas.append(int(ID.split(':')[1]))
            arma = subselector('Arma',armas)
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
            for i in range(len(ARMAS)):
                if ARMAS[i]['Nombre'] == armas[arma]:
                    dote = str(nom.index(dt))+':'+str(i)
            
        elif mec[nom.index(dt)] == 'u:m':
            print ('Para la dote seleccionada debes elegir un arma con la que no seas competente',
                   'Elije una: ', sep = '\n')
            armas = []
            for i in range(len(ARMAS)):
                if ARMAS[i]['Competencia'] == nom.index(dt):
                    if i not in comp_armas:
                        if str(nom.index(dt))+':'+str(i) not in dotes_pj:
                            armas.append(ARMAS[i]['Nombre'])

            arma = subselector('Arma',armas,dos_col=True)
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
            for i in range(len(ARMAS)):
                if ARMAS[i]['Nombre'] == armas[arma]:
                    dote = str(nom.index(dt))+':'+str(i)

        elif mec[nom.index(dt)] == 'u:e':
            print ('Para la dote seleccionada debes elegir una escuela de magia',
                   'Elije una: ', sep = '\n')
            ESCUELAS = 'Abjuración','Adivinación','Conjuración','Encantamiento',
            'Evocación','Ilusión','Nigromancia','Transmutación' ## TEMPORAL y TRANSITORIA
            escuelas = []
            for i in range(len(ESCUELAS)):
                if str(nom.index(dt))+':'+i not in dotes_pj:
                    escuelas.append(ESCUELAS[i])
            
            esc = subselector('Escuela',escuelas,dos_col=True)
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
            dote = str(nom.index(dt))+':'+str(ESCUELAS.index(escuelas[esc]))
        
        elif mec[nom.index(dt)] == 'u:h':
            print ('Para la dote seleccionada debes elegir una habilidad', 'Elije una: ', sep = '\n')
            habs = []
            for i in range(len(lista_de_habilidades)):
                if str(nom.index(dt))+':'+str(i) not in dotes_pj:
                    habs.append(lista_de_habilidades[i])
            
            hab = subselector('Habilidad',habs,dos_col=True)
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
            dote = str(nom.index(dt))+':'+str(lista_de_habilidades.index(habs[hab]))

        else:
            dote = str(nom.index(dt))
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
        if dote == '':
            pass
        else:
            if not input('\n¿Esta seguro? ').lower().startswith('s'):
                dote = ''
    
    return dote
    
def SelAE (mecanicas,app_pj):
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
    
    seleccion = subselector('AE',elegibles)
        
    if seleccion == 'Dote general':
        return 'd'
    else:
        return seleccion
        
def SelTirs (tirs):
    print('Sus tiradas son: '+f.PrepPrint(tirs))
    sleep (2)
    if input ('¿Desea tirar de nuevo? ').lower().startswith('s'):
        os.system(['clear','cls'][os.name == 'nt'])
        return False
    else:
        return True

def subselector (prompt,lista,dos_col=False,vueltas=1):
    items = []
    pool = vueltas
    for vuelta in range(vueltas):
        if vuelta == 0:
            paginado = []
            for i in range(len(lista)):
                paginado.append(str(i)+': '+str(lista[i]))
            if dos_col == False:
                f.paginar (10,paginado)
            else:
                f.paginar (10,f.a_dos_columnas(paginado))
          
        
        while pool > 0:
            item = ''
            while item == '':
                item = input ('\n'+prompt+': ').capitalize()
                if item.isnumeric():
                    item = int(item)
                    if item in items:
                        print ('Ya ha realizado esa selección, intente nuevamente')
                        item = ''
                    elif item not in range(len(lista)):
                        print('La selección es incorrecta, intente nuevamente')
                        item = ''
                    else:
                        items.append(item)
                        print ('Ha elegido '+lista[int(item)],end = ' ')
                        pool -= 1
                elif item not in lista:
                    print('La selección es incorrecta, intente nuevamente')
                    item = ''
                elif lista.index(item) in items:
                    print ('Ya ha realizado esa selección, intente nuevamente')
                    item = ''
                else:
                    print ('Ha elegido '+item,end = ' ')
                    items.append(lista.index(item))
                    pool -= 1
            if not input('¿Está seguro? ').strip().lower().startswith('s'):
                pool += 1
                del items[-1]
    
    if vueltas == 1:
        return items[0]
    else:
        return items

def SelIdiomas (IDIOMAS,Clase,Raza,pool):
    autos = []
    adics = []
    nom = Clase['Nombre']
    for i in Raza['Idioma_auto']:
        autos.append(IDIOMAS[i])
    for i in Raza['Idioma_adic']:
        adics.append(IDIOMAS[i])
    
    if 'Idiomas' in Clase:
        idi_clas = Clase['Idiomas']
        for i in idi_clas:
            if IDIOMAS[i] not in adics:
                adics.append(IDIOMAS[i])
    print ('\nLos idiomas automáticos de tu raza son: '+f.PrepPrint(autos))
    
    idiomas = []
    if pool > 0:
        print ('\nAdemás, tu personaje puede conocer '+str(pool)+
               ' idiomas adicionales.\nEligelos de la siguiente lista:')
        elecs = subselector ('Idioma',adics,dos_col=True,vueltas=pool)
        if type(elecs) == list:
            for i in elecs:
                idiomas.append(IDIOMAS.index(adics[i]))
        else:
            idiomas.append(IDIOMAS.index(adics[elecs]))
    
    for i in autos:
        idiomas.append(IDIOMAS.index(i))

    idiomas.sort()
    return idiomas

def NuevosIdiomas (IDIOMAS,idi_pj,pool):
    lista = []
    for i in idi_pj:
        lista.append(IDIOMAS[i])
    print ('Sus idiomas actuales son: '+f.PrepPrint(lista)+
           '\nPuede elegir '+str(pool)+' idiomas nuevos, de entre los siguientes:\n')
    posibles = []
    for i in range(len(IDIOMAS)):
        if i not in idi_pj:
            posibles.append(IDIOMAS[i])

    sels = subselector ('Idioma',posibles,dos_col=True,vueltas=pool)
    if type(sels) == list:
        for i in sels:
            idi_pj.append(IDIOMAS.index(posibles[i]))
    else:
        idi_pj.append(IDIOMAS.index(posibles[sels]))
    
    idi_pj.sort()
    return idi_pj