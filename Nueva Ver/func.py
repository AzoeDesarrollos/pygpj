# coding=UTF-8
from random import randint
import os
import csv

def leerCSV (archivo):
    '''Lee archivos CSV y los devuelve como una lista.'''
    
    arch = csv.reader(open(archivo),dialect='myCSV')
    temp = []
    for t in arch:
        temp.append(t)
    if len(temp) == 1:
        temp = temp[0]
    return temp

def SelCla(claseprevia):
    '''Provee un selector de clases.'''
    
    if claseprevia == '':
        print ('Elije una clase para este nivel')
    else:
        print ('Elije una clase para este nivel [Enter: '+claseprevia+']')
    CLASES = ('Barbaro','Bardo','Brb','Brd','Bárbaro','Clerigo','Clr','Clérigo','Drd','Druida','Exp','Explorador','Gue','Guerrero','Hcr','Hechicero','Mag','Mago','Mnj','Monje','Paladin','Paladín','Pcr','Picaro','Pld','Pícaro','barbaro','bardo','brb','brd','bárbaro','clerigo','clr','clérigo','drd','druida','exp','explorador','gue','guerrero','hcr','hechicero','mag','mago','mnj','monje','paladin','paladín','pcr','picaro','pld','pícaro','')
    while True:
        cla = input('Clase: ')
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
    
    CLASES = ('Brb','Brd','Clr','Drd','Exp','Gue','Hcr','Mag','Mnj','Pld','Pcr')
    if cla in CLASES: Clase = cla
    elif cla.capitalize() in CLASES: Clase = cla.capitalize()
    elif cla == '': Clase = ''
    elif cla in ('Bárbaro','bárbaro','barbaro','Barbaro'): Clase = 'Brb'
    elif cla in ('Bardo','bardo'): Clase = 'Brd'
    elif cla in ('Clérigo','clérigo','clerigo','Clerigo'): Clase = 'Clr'
    elif cla in ('Druida','druida'): Clase = 'Drd'
    elif cla in ('Explorador','explorador'): Clase = 'Exp'
    elif cla in ('Guerrero','guerrero'): Clase = 'Gue'
    elif cla in ('Hechicero','hechicero'): Clase = 'Hcr'
    elif cla in ('Mago','mago'): Clase = 'Mag'
    elif cla in ('Monje','monje'): Clase = 'Mnj'
    elif cla in ('Paladín','paladín','paladin','Paladin'): Clase = 'Pld'
    elif cla in ('Pícaro','pícaro','picaro','Picaro'): Clase = 'Pcr'
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

def Claseas (clase):
    '''Devuelve las habilidades cláseas de la clase citada.'''
    
    hab_cls = {'Brb':(1,14,17,20,22,36,38,40,41),'Brd':(1,2,5,6,7,8,9,10,11,12,13,14,16,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,39,41),'Clr':(1,5,6,8,23,26,30,32,35,37),'Drd':(1,3,5,6,8,14,20,22,23,33,37,38,40,44),'Exp':(1,3,4,5,13,14,20,21,22,23,28,29,33,36,37,38,40,41,43,44),'Gue':(1,17,20,22,23,36,40,41),'Hcr':(1,5,6,10,23,26),'Mag':(1,5,6,7,23,26,27,28,29,30,31,32,33,34,35),'Mnj':(1,2,3,5,8,11,12,13,14,16,21,22,23,24,26,35,36,41),'Pld':(1,2,5,8,20,23,34,35,37,40),'Pcr':(0,1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,31,36,39,41,42,43)}
    cls = []
    for i in hab_cls[clase]:
        cls.append(habs[i])
    return cls

def RepRNG (PH,nv_cls,hab_cla,habilidades):
    '''Devuelve un diccionario con la habilidad y sus rangos.'''
    
    os.system(['clear','cls'][os.name == 'nt'])
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
        if hab not in habilidades:
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
        dt = input('\nDote: ').rstrip(' ').capitalize()
        while dt not in nom:
            print ('Por favor, escribe la dote correctamente\n')
            dt = input('\nDote: ').rstrip(' ').capitalize()
        print ('Prerrequisitos: '+pre[nom.index(dt)]+'\n'+des[nom.index(dt)])
        if input('\n¿Esta seguro?').lower().startswith('s'):
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
    ''''Genera las 7 tiradas y descarta la más baja.
    
    También, imprime la lista en un lindo formato.'''
    
    A,B,C = UnaCar(),UnaCar(),UnaCar()
    D,E,F = UnaCar(),UnaCar(),UnaCar()
    G = UnaCar()
    TirList = [A,B,C,D,E,F,G]
    TirList.sort(reverse=True)
    del TirList[-1]
    
    imprimir = ''
    for elemento in TirList:
        imprimir = imprimir+str(elemento)+', '
    imprimir = imprimir.rstrip(', ')+'.'
    return imprimir
    
def SelRaza():
    '''Provee un selector de razas.'''
    
    raza = ''
    razas = {'Humano':((0,0,0,0,0,0),'Mediano','humano',(),"30'"),
             'Elfo':((0,2,-2,0,0,0),'Mediano','elfo',((3,2),(4,2),(14,2)),"30'"),
             'Enano':((0,0,2,0,0,-2),'Mediano','enano',((1,2),(4,2),(39,2)),"20'"),
             'Gnomo':((-2,0,2,0,0,0),'Pequeño','gnomo',((1,2),(14,2)),"20'"),
             'Mediano':((-2,2,0,0,0,0),'Pequeño','mediano',((14,2),(21,2),(36,2),(41,2)),"20'"),
             'Semielfo':((0,0,0,0,0,0),'Mediano','elfo',((3,1),(4,1),(8,2),(14,1),(25,2)),"30'"),
             'Semiorco':((2,0,0,2,0,-2),'Mediano','orco',(),"30'")}
    while raza not in razas:
        raza = input('Raza: ').capitalize()
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