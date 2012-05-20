# coding=UTF-8
from func import *
from setup import *
from time import sleep
from setup import DOTES,compW,ARMAS,HABS,dt_cls
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
                print ('Has elegido que este personaje sea un '+lista_de_razas[raza][0]+'.', end = ' ')
                if not input ('¿Estas seguro? ').lower().startswith('s'):
                    raza = ''
                else:
                    return lista_de_razas[raza]
        elif raza not in lista_de_razas:
            print('Raza inválida o error ortográfico, intente nuevamente')
        else:
            print ('Has elegido que este personaje sea un '+lista_de_razas[raza][0]+'.', end = ' ')
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
    
    Alineamientos = ('Legal bueno','Neutral bueno','Caótico bueno','Legal neutral','Neutral auténtico','Neutral bueno','Legal maligno','Neutral maligno','Caótico maligno')
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
    
    abr = lista_de_clases[0]
    nom = lista_de_clases[5]
    ali = lista_de_clases[8]
    pos = []
    abp = []
    for i in range(len(ali)):
        if str(alineamiento) in ali[i]:
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
    
    
    while True:
        cla = input('\nClase: ').capitalize()
        if cla not in CLASES:
            print ('\nSeleccione una clase válida.')
        elif cla == '':
            if claseprevia == '':
                print ('\nDebe seleccionar una clase')
            else:
                cla = claseprevia
        else:
            if cla in abr: Clase = cla
            elif cla.capitalize() in nom: Clase = abr[nom.index(cla)]
            elif cla == '': Clase = ''
            elif cla == 'Barbaro': Clase = 'Brb'
            elif cla == 'Clerigo': Clase = 'Clr'
            elif cla == 'Paladin': Clase = 'Pld'
            elif cla == 'Picaro': Clase = 'Pcr'
            elif cla.isnumeric(): Clase = abp[int(cla)]
            
            print ("Has seleccionado '"+nom[abr.index(Clase)]+"' como clase para este nivel.",end= ' ')
            if input ('¿Estas seguro? ').lower().startswith('s'):
                return Clase

def AumentaCar (nivel):
    CARS = ('FUE','DES','CON','INT','SAB','CAR','Fuerza','Destreza','Constitución','Constitucion','Inteligencia','Sabiduría','Sabiduria','Carisma')

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
        print()
        Paginar(10,DTaDosCol(hab_cla))

    print ('\nRecuerda que cualquier habilidad transclásea cuesta dos puntos en lugar de uno.\nEscribe una habilidad y los puntos que desees invertir en ella.\n')
    
    rng = {}
    for i in range(len(rangos)):
        rng[lista_de_hab[i]] = rangos[i]
        
    rng_max = nv_cls+3
    rng_max_tc = rng_max/2
    
    while PH > 0:
        hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        while hab not in lista_de_hab:
            print('Por favor, escribe la habilidad correctamente')
            hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        if rng[hab] >0:
            print (hab+' ya posee '+str(rng[hab])+' rangos.')
       
        while True:
            puntos = input('Puntos: ')
            if not puntos.isnumeric():
                print ('Los rangos deben ser numéricos')
            elif int(puntos) > PH:
                print('No posees tantos puntos de habilidad')
            else:
                puntos = int(puntos)
                break
        
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
    input ('\n[Presione Enter para continuar]')
    return rng

def SelDot (nivel,lista_de_dotes,comp_armas,ARMAS,lista_de_habilidades,spec,clase,dotes_clase):
    '''Provee un selector de dotes.'''
    
    if spec == False:
        print ('\nEn el '+str(nivel)+'º nivel, tienes una dote para elegir')
        posibles = GenerarListadeAyuda(AutoDot(DOTES,[],compW,ARMAS[0],HABS[0]),DOTES)
    else:
        print ('\nComo aptitud de clase, en este nivel tienes una dote adicional para elegir')
        posibles = GenerarListadeAyuda(AutoDot(DOTES,dt_cls[clase],compW,ARMAS[0],HABS[0]),DOTES)
    
    nom = lista_de_dotes[0]
    pre = lista_de_dotes[1]
    des = lista_de_dotes[2]
    mec = lista_de_dotes[3] # Puede ser: 'u', 's', 'u:h','u:w','u:m','u:e' y, de momento, 'u:?' 
    # 'u' y 's' no tienen implicancia (solo indican si la dote se puede repetir, o no'
    # 'u:h' (Soltura con una habilidad) indica que debe elegirse una habilidad que NO se haya elegido antes.
    # 'u:w' indica que debe elegirse un arma que figure dentro de las competencias en armas del personaje.
    # 'u:m' indica que debe elegirse un arma que NO figure dentro de las competencias del personaje.
    # 'u:e' indica que debe elegirse una escuela de magia.
    
    dote = ''
    while dote == '':
        dt = input('\nDote: ').rstrip(' ').capitalize()
        if dt not in nom:
            print ('Por favor, escribe la dote correctamente\n')
        elif dt not in posibles:
            print ('Actualmente el personaje no cumple con los prrerequisitos para la dote seleccionada', 'Elija otra', sep = '\n')
        elif mec[nom.index(dt)] == 'u:w':
            print ('Para la dote seleccionada debes elegir un arma con la que seas competente', 'Elije una: ', sep = '\n')
            for i in range(len(comp_armas)):
                print (str(i)+': '+comp_armas[i])
            arma = ''
            while arma == '':
                arma = input ('\nArma: ').capitalize()
                if arma.isnumeric():
                    if int(arma) not in range(len(comp_armas)):
                        print('La selección es incorrecta, intente nuevamente')
                        arma = ''
                    else:
                        dote = str(nom.index(dt))+':'+arma
                        print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
                elif arma not in comp_armas:
                    print('La selección es incorrecta, intente nuevamente')
                    arma = ''
                else:
                    dote = str(nom.index(dt))+':'+str(comp_armas.index(arma))
                    print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])

        elif mec[nom.index(dt)] == 'u:m':
            print ('Para la dote seleccionada debes elegir un arma con la que no seas competente', 'Elije una: ', sep = '\n')
            i = 0
            armas = []
            for a in range(len(ARMAS[0])):
                if ARMAS[2][a] == str(nom.index(dt)):
                    if a not in comp_armas:                   
                        print (str(i)+': '+ARMAS[0][a])
                        armas.append(ARMAS[0][a])
                        i+=1
            arma = ''
            while arma == '':
                arma = input ('\nArma: ').capitalize()
                if arma.isnumeric():
                    if int(arma) not in range(len(armas)):
                        print('La selección es incorrecta, intente nuevamente')
                        arma = ''
                    else:
                        dote = str(nom.index(dt))+':'+arma
                        print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
                elif arma not in armas:
                    print('La selección es incorrecta, intente nuevamente')
                    arma = ''
                else:
                    dote = str(nom.index(dt))+':'+str(armas.index(arma))
                    print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])

        elif mec[nom.index(dt)] == 'u:e':
            print ('Para la dote seleccionada debes elegir una escuela de magia', 'Elije una: ', sep = '\n')
            escuelas = 'Abjuración','Adivinación','Conjuración','Encantamiento',
            'Evocación','Ilusión','Nigromancia','Transmutación' ## TEMPORAL y TRANSITORIA
            for i in range(len(escuelas)):
                print (str(i)+': '+escuelas[i])
            esc = ''
            while esc == '':
                esc = input ('Escuela: ').capitalize()
                if esc.isnumeric():
                    if int(esc) not in range(len(escuelas)):
                        print('La selección es incorrecta, intente nuevamente')
                        esc = ''
                    else:
                        dote = str(nom.index(dt))+':'+esc
                        print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
                elif esc not in escuelas:
                    print('La selección es incorrecta, intente nuevamente')
                    esc = ''
                else:
                    dote = str(nom.index(dt))+':'+str(escuelas.index(esc))
                    print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
        
        elif mec[nom.index(dt)] == 'u:h':
            print ('Para la dote seleccionada debes elegir una habilidad', 'Elije una: ', sep = '\n')
            hab = ''
            while hab == '':
                hab = input ('Habilidad: ').capitalize()
                if hab not in lista_de_habilidades:
                    print('La selección es incorrecta, intente nuevamente')
                    hab = ''
                else:
                    dote = str(nom.index(dt))+':'+str(lista_de_habilidades.index(hab))
                    print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
        else:
            dote = str(nom.index(dt))
            print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])
        if input('\n¿Esta seguro? ').lower().startswith('s'):
            return dote
        else:
            dote = ''

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

    for i in range(len(elegibles)):
        print (str(i)+': '+elegibles[i])

    seleccion = ''
    while seleccion == '':
        AE = input ('\nAE: ').capitalize()
        if AE in elegibles:
            seleccion = AE
        elif AE.isnumeric():
            for i in range(len(elegibles)):
                if i == int(AE):
                    seleccion = elegibles[int(AE)]
        else:
            print ('\nSelección inválida, intente nuevamente\n')

    if seleccion == 'Dote general':
        return 'd'
    else:
        return seleccion
        
def SelTirs (tirs):
    print('Sus tiradas son: '+PrepPrint(tirs))
    sleep (2)
    if input ('¿Desea tirar de nuevo? ').lower().startswith('s'):
        os.system(['clear','cls'][os.name == 'nt'])
        return False
    else:
        return True
