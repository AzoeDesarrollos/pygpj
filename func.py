# coding=UTF-8
from random import randint
import os
import csv
from time import sleep

def leerCSV (archivo):
    '''Lee archivos CSV y los devuelve como una lista.'''
    
    arch = csv.reader(open(archivo),dialect='myCSV')
    temp = []
    for t in arch:
        temp.append(t)
    if len(temp) == 1:
        temp = temp[0]
    return temp

def Alinear ():
    Alineamientos = ('Legal bueno','Neutral bueno','Caótico bueno','Legal neutral','Neutral auténtico','Neutral bueno','Legal maligno','Neutral maligno','Caótico maligno')
    while True:
        aling = input ('\nEscoge un alineamiento para este personaje\n1: Legal bueno     2: Neutral bueno       3: Caótico bueno\n4: Legal neutral   5: Neutral auténtico   6: Caótico neutral\n7: Legal maligno   8: Neutral maligno     9: Caótico maligno\n\n')
        if not aling.isnumeric():
            if aling.capitalize() in Alineamientos:
                aling = Alineamientos.index(aling.capitalize())
            else:
                print ('Escriba correctamente el alineamiento, o el numero que lo representa')
        else:
            aling = int (aling) -1
        
        if aling not in (0,1,2,3,4,5,6,7,8):
            print ('El numero elegido no representa ningún alineamiento')
        else:
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
        print ('\nElije una clase para este nivel')
        print ('\nLas clases disponibles según el alineamiento son: \n'+imprimir)
    else:
        print ('\nElije una clase para este nivel [Enter: '+claseprevia+']')
   
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
                break
        else:
            break
    
    if cla in abr: Clase = cla
    elif cla.capitalize() in nom: Clase = abr[nom.index(cla)]
    elif cla == '': Clase = ''
    elif cla == 'Barbaro': Clase = 'Brb'
    elif cla == 'Clerigo': Clase = 'Clr'
    elif cla == 'Paladin': Clase = 'Pld'
    elif cla == 'Picaro': Clase = 'Pcr'
    elif cla.isnumeric(): Clase = abp[int(cla)]
    
    return Clase

def ProCla(lista_de_clases,clase,nv_cls):
    '''Procesa la lista de clases y otiene ATKbase, y TSs.'''
    
    nom = lista_de_clases[0]
    ATKb = lista_de_clases[1]
    Fort = lista_de_clases[2]
    Ref = lista_de_clases[3]
    Vol = lista_de_clases[4]
    if ATKb[nom.index(clase)] == 'b':
        A = 1
    elif ATKb[nom.index(clase)] == 'i':
        A = 3/4
    else:
        A = 1/2
    
    if Fort[nom.index(clase)] == 'b':
        F = 1/2
        if nv_cls == 1:
            F += 2
    else:
        F = 1/3
    
    if Ref[nom.index(clase)] == 'b':
        R = 1/2
        if nv_cls == 1:
            R += 2
    else:
        R = 1/3
    
    if Vol[nom.index(clase)] == 'b':
        V = 1/2
        if nv_cls == 1:
            V += 2
    else:
        V = 1/3
    
    return A,F,R,V

def PuntHab (lista_de_clases,clase,nivel,INT_mod,subtipo):
    '''Devuelve los puntos de habilidad a repartir para el nivel de clase.'''
    
    nom = lista_de_clases[0]
    PHs = lista_de_clases[6]
    for i in range(len(PHs)):
        PHs[i] = int(PHs[i])
    PH = PHs[nom.index(clase)]+INT_mod
    if nivel == 1:
        PH *= 4
        if subtipo == 'humano':
            PH += 4
    else:
        if subtipo == 'humano':
            PH += 1
    return PH

def Claseas (lista_de_clases,clase,lista_de_hab):
    '''Devuelve las habilidades cláseas de la clase citada.'''
    
    nom = lista_de_clases[0]
    hab = lista_de_clases[7]
    hab_cls = {}
    
    for i in range(len(nom)):
        hab_cls[nom[i]]=hab[i]

    for i in nom:
        hab_cls[i]=hab_cls[i].split(',')

    for i in range(len(nom)):
        for j in hab_cls[nom[i]]:
            hab_cls[nom[i]][hab_cls[nom[i]].index(j)] = int(hab_cls[nom[i]][hab_cls[nom[i]].index(j)])
    
    cls = []
    for i in hab_cls[clase]:
        cls.append(lista_de_hab[i])
    return cls

def RepRNG (PH,nv_cls,hab_cla,lista_de_hab):
    '''Devuelve un diccionario con la habilidad y sus rangos.'''
    
    print('\nTienes '+str(PH)+' puntos de habilidad para distribuir en este nivel.\n')
    b = ''
    if input('Deseas conocer tus habilidades de clase?\n').lower().startswith('s'):
        for hab in hab_cla:
            b = b+hab+', '
        print(b.rstrip(', ')+'.\n')
    print ('Recuerda que cualquier habildiad transclásea cuesta dos puntos en lugar de uno.\nEscribe una habilidad y los puntos que desees invertir en ella.\n')
    
    rng_max = nv_cls+3
    rng_max_tc = round(rng_max/2)
    rng = {}
    while PH > 0:
        hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        if hab not in lista_de_hab:
            print('Por favor, escribe la habilidad correctamente')
            hab = input('\nHabilidad: ').rstrip(' ').capitalize()
        rng[hab]=0
        puntos = input('Puntos: ')
        while not puntos.isnumeric():
            print ('Los rangos deben ser numéricos')
            puntos = input('Puntos: ')
        puntos = int(puntos)
        
        if hab not in hab_cla:
            PH -= puntos
            rng[hab] += puntos/2
            print('\nPuntos restantes: '+str(PH))
            if PH < 0:
                print('no alcanzan los puntos')
                PH += puntos*2
                rng[hab] -= puntos/2
        else:
            if rng[hab] + puntos > rng_max:
                print(hab+' ha alcanzado el rango máximo ('+str(rng_max)+').')
                PH -= rng_max
                rng[hab] += rng_max
                print('\nPuntos restantes: '+str(PH))
                if PH < 0:
                    print('no alcanzan los puntos')
                    PH += rng_max
                    rng[habs.index(hab)] -= rng_max
            else:
                PH -= puntos
                rng[hab] += puntos
                print('\nPuntos restantes: '+str(PH))
                if PH < 0:
                    print('no alcanzan los puntos')
                    PH += puntos
                    rng[hab] -= puntos
    return rng

def HabMod(mods,hab_num,mods_de_caract):
    '''Calcula el modificador final de habilidad.'''
    
    mod = 0
    temp = mods[hab_num]
    if temp == 'FUE': mod = mods_de_caract[0]
    elif temp == 'DES': mod = mods_de_caract[1]
    elif temp == 'CON': mod = mods_de_caract[2]
    elif temp == 'INT': mod = mods_de_caract[3]
    elif temp == 'SAB': mod = mods_de_caract[4]
    elif temp == 'CAR': mod = mods_de_caract[5]
    
    return rng[hab_num]+mod+rcl[hab_num]+sng[hab_num]+dts[hab_num]+obj[hab_num]

def SelDot (lista_de_dotes,nivel):
    '''Provee un selector de dotes.'''
    
    nom = lista_de_dotes[0]
    pre = lista_de_dotes[1]
    des = lista_de_dotes[2]
    if nivel in (1,3,6,9,12,15,18):
        print ('\nEn el '+str(nivel)+'º nivel, tienes una dote para elegir')
        while True:
            dt = input('\nDote: ').rstrip(' ').capitalize()
            if dt not in nom:
                print ('Por favor, escribe la dote correctamente\n')
            else:
                print ('Prerrequisitos: '+pre[nom.index(dt)]+'\n'+des[nom.index(dt)])
            
            if input('\n¿Esta seguro? ').lower().startswith('s'):
                return dt
    else:
        pass

def UnaCar ():
    '''Un simple generador para una caracterítica.'''
    
    car = [randint(1,6),randint(1,6),randint(1,6),randint(1,6)]
    car.sort(reverse=True)
    del car[-1]
    Car = sum(car)
    return Car
    
def GenTir():
    ''''Genera las 7 tiradas y descarta la más baja.'''
    
    A,B,C = UnaCar(),UnaCar(),UnaCar()
    D,E,F = UnaCar(),UnaCar(),UnaCar()
    G = UnaCar()
    TirList = [A,B,C,D,E,F,G]
    TirList.sort(reverse=True)
    del TirList[-1]
    return TirList
    
def PrepPrint(lista):
    imprimir = ''
    for elemento in lista:
        imprimir = imprimir+str(elemento)+', '
    imprimir = imprimir.rstrip(', ')+'.'
    return imprimir
    
def SelRaza(lista_de_razas):
    '''Provee un selector de razas.'''
    
    print('\nSeleccione Raza \n1: Humano 2: Enano 3: Elfo 4: Gnomo\n5: Mediano 6: Semielfo 7: Semiorco\n')
    
    razas = {}
    for R in lista_de_razas:
        razas[R[0]]=R[1:]
    
    for key in razas:
        razas[key][1] = razas[key][1].split(',')
        for i in range(len(razas[key][1])):
            razas[key][1][i] = int(razas[key][1][i])
        razas[key][4] = razas[key][4].split(',')
        for i in range(len(razas[key][4])):
            razas[key][4][i] = razas[key][4][i].split('b')
        for par in razas[key][4]:
            if par == ['']:
                pass
            else:
                for i in range(len(par)):
                    par[i]=int(par[i])
    
    raza = ''
    while raza not in razas:
        raza = input('Raza: ').capitalize()
        if raza.isnumeric():
            if raza == '1': raza = 'Humano'
            elif raza == '2': raza = 'Elfo'
            elif raza == '3': raza = 'Enano'
            elif raza == '4': raza = 'Gnomo'
            elif raza == '5': raza = 'Mediano'
            elif raza == '6': raza = 'Semielfo'
            elif raza == '7': raza = 'Semiorco'
            else:
                print('Raza inválida, intente nuevamente\n')
        if raza not in razas:
            print('Raza inválida o error ortográfico, intente nuevamente\n')
    return razas[raza]

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

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

def AumentaCar (nivel):
    CARS = ('FUE','DES','CON','INT','SAB','CAR','Fuerza','Destreza','Constitución','Constitucion','Inteligencia','Sabiduría','Sabiduria','Carisma')
    if nivel % 4 == 0:
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
            elif Car in 'DES': Car = 1
            elif Car in 'CON': Car = 2
            elif Car in 'INT': Car = 3
            elif Car in 'SAB': Car = 4
            elif Car in 'CAR': Car = 5
        
        return Car
    else:
        return ''

def ProcApps (aptitudes):
    '''Procesa las Aptitudes Especiales en formato CSV'''
    
    AE = {}
    for A in aptitudes:
        AE[A[0]]=A[1:]

    for key in AE:
        for i in range(len(AE[key])):
            AE[key][i] = AE[key][i].split(',')

    return AE

def AppClas (APPdict,clase,nv_cls):
    '''Devuelve las aptitudes de la clase al nivel dado.'''
    
    nv_cls -= 1
    return APPdict[clase][nv_cls]