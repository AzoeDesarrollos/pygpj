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
        print ('\nElije una clase para este nivel')
        print ('\nLas clases disponibles según el alineamiento son: \n'+imprimir)
    else:
        print ('\nElije una clase para este nivel [Enter: '+claseprevia+']')
        print ('\nLas clases disponibles según el alineamiento son: \n'+imprimir)
   
    CLASES = ['Barbaro','Clerigo','Paladin','Picaro','']+numeros+pos+abp
    
    while True:
        cla = input('Clase: ').capitalize()
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

def Claseas (claseas,clase,lista_de_hab):
    '''Devuelve las habilidades cláseas de la clase citada.'''
    
    cls = []
    for i in claseas[clase]:
        cls.append(lista_de_hab[i])
    return cls

def RepRNG (PH,nv_cls,hab_cla,lista_de_hab,rangos):
    '''Devuelve un diccionario con la habilidad y sus rangos.'''
    
    print('\nTienes '+str(PH)+' puntos de habilidad para distribuir en este nivel.\n')
    b = ''
    if input('Deseas conocer tus habilidades de clase? ').lower().startswith('s'):
        print()
        DTaDosCol(hab_cla)

    print ('\nRecuerda que cualquier habilidad transclásea cuesta dos puntos en lugar de uno.\nEscribe una habilidad y los puntos que desees invertir en ella.\n')
    
    rng = {}
    for i in range(len(rangos)):
        rng[lista_de_hab[i]] = rangos[i]
        
    rng_max = nv_cls+3
    rng_max_tc = round(rng_max/2)
    
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
                if rng[hab] + puntos >= rng_max_tc:
                    print(hab+' ha alcanzado el rango máximo ('+str(rng_max_tc)+').')
                    PH -= rng_max_tc - rng[hab]
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
    
    return rng

def HabcR (rangos):
    c1 = []
    c2 = []
    cR = []
    for i in range(len(rangos)):
        if rangos[i] > 0:
            cR.append(HABS[0][i])

    for i in range(len(cR)):
        if i%2 == 0:
            c1.append(cR[i])
        else:
            c2.append(cR[i])

    for i in range(len(c1)):
        if len(c1[i]+' '+str(rangos[i])) > 23:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t')
        elif len(c1[i]+' '+str(rangos[i])) > 15:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t\t')
        else:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t\t\t')

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

def ProcDTS (mecCSV):
    ID,tipo,r_cls = [],[],[]
    r_nv,r_dts,r_rng = [],[],[]
    r_app,r_stat,r_car, = [],[],[]
    
    for D in mecCSV:
        ID.append(D[0])
        tipo.append(D[1])
        r_cls.append(D[2])
        r_nv.append(D[3])
        r_dts.append(D[4])
        r_rng.append(D[5])
        r_app.append(D[6])
        r_stat.append(D[7])
        r_car.append(D[8])
    
    for i in range(len(ID)):
        ID[i] = int(ID[i])
    
    general = [ID,tipo,r_cls,r_nv,r_dts,r_rng,r_app,r_stat,r_car]
    
    return general

def ProcRazas (razasCSV):
    razas = {}
    for R in razasCSV:
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
    
    return razas

def ProcHabCls (lista_de_clases):
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
    
    return hab_cls

def ValPreReq (ID,mecanicas,nv_cls,nivel,dotes,rangos,aptitudes,stats,caract):
    
    IDs = mecanicas[0]
    tipo = mecanicas[1]
    r_cls = mecanicas[2]
    r_nv = mecanicas[3]
    r_dts = mecanicas[4]
    r_rng = mecanicas[5]
    r_app = mecanicas[6]
    r_stat = mecanicas[7]
    r_car = mecanicas[8]
    
    valido = 0
    
    if tipo[ID] == 'u':
        if ID in dotes:
            valido = 0
        else:
            valido = 1
    elif tipo[ID] == 's':
        valido = 1
    else:
        valido = 0 ## provisional
    
    if valido == 1:
        if r_cls[ID] == '':
            valido = 1
        else:
            Req = r_cls[ID].split(' ')
            if Req[0] in nv_cls:
                if nv_cls.count(Req[0]) >= int(Req[1]):
                    valido = 1
                else:
                    valido = 0

        if valido == 1:
            if r_nv[ID] == '':
                valido = 1
            else:
                if len(nv_cls)>= int(r_nv[ID]):
                    valido = 1
                else:
                    valido = 0

            if valido == 1:
                if r_dts[ID] == '':
                    valido = 1
                else:
                    Reqs = r_dts[ID].split(',')
                    for Req in Reqs:
                        if int(Req) in dotes: ## capaz quedaria mejor un for i
                            valido = 1
                        else:
                            valido = 0

                if valido == 1:
                    if r_rng[ID] == '':
                        valido = 1
                    else:
                        Req = r_rng[ID].split(':')
                        if rangos[int(Req[0])] >= int(Req[1]):
                            valido = 1
                        else:
                            valido = 0

                    if valido == 1:
                        if r_app[ID] == '':
                            valido = 1
                        else:
                            valido = 0 ## más que provisional...
                        
                        if r_stat[ID] == '':
                            valido = 1
                        else:
                            Req = r_stat[ID].split(':')
                            if Req[0] == '0': ## Requisito de ataque base
                                if stats[0] >= int(Req[1]):
                                    valido = 1
                                else:
                                    valido = 0
                            if Req[0] == '1': ## Requisito de TS Fort
                                if stats[1] >= int(Req[1]):
                                    valido = 1
                                else:
                                    valido = 0        
                            if Req[0] == '2': ## Requisito de TS Ref
                                if stats[2] >= int(Req[1]):
                                    valido = 1
                                else:
                                    valido = 0
                            if Req[0] == '3': ## Requisito de TS Vol
                                if stats[3] >= int(Req[1]):
                                    valido = 1
                                else:
                                    valido = 0

                        if valido == 1:
                            if r_car[ID] == '':
                                valido = 1
                            else:
                                Reqs = r_car[ID].split(',')
                                for Req in Reqs:
                                    car = Req.split(':')[0]
                                    val = Req.split(':')[1]
                                    if caract[int(car)] >= int(val):
                                        valido = 1
                                    else:
                                        valido = 0
    
    
    if valido == 1:
        return True
    else:
        return False

def SelDot (lista_de_dotes,posibles,nivel):
    '''Provee un selector de dotes.'''
    
    nom = lista_de_dotes[0]
    pre = lista_de_dotes[1]
    des = lista_de_dotes[2]
    while True:
        dt = input('\nDote: ').rstrip(' ').capitalize()
        if dt not in nom:
            print ('Por favor, escribe la dote correctamente\n')
        elif dt not in posibles:
            print ('Actualmente el personaje no cumple con los prrerequisitos para la dote seleccionada', 'Elija otra', sep = '\n')
        else:
            print ('Prerrequisitos: '+pre[nom.index(dt)]+'(cumplidos)\n'+des[nom.index(dt)])
        
            if input('\n¿Esta seguro? ').lower().startswith('s'):
                return nom.index(dt)

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

def HabDosCol (rangos):
    c1 = []
    c2 = []
    cR = []
    for i in range(len(rangos)):
        if rangos[i] > 0:
            cR.append(HABS[0][i])

    for i in range(len(cR)):
        if i%2 == 0:
            c1.append(cR[i])
        else:
            c2.append(cR[i])

    for i in range(len(c1)):
        if len(c1[i]+' '+str(rangos[i])) > 23:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t')
        elif len(c1[i]+' '+str(rangos[i])) > 15:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t\t')
        else:
            print (c1[i]+' '+str(rangos[i]),c2[i]+' '+str(rangos[i]),sep='\t\t\t')

def DTaDosCol(dotes):
    c1 = []
    c2 = []
    
    for i in range(len(dotes)):
        if i%2 == 0:
            c1.append(dotes[i])
        else:
            c2.append(dotes[i])

    if len(c1)>len(c2):
        c2.append(''*(len(c1)-len(c2)))

    for i in range(len(c1)):
        if len(c1[i]) > 32:
            print (c1[i],c2[i],sep='\t')
        elif len(c1[i]) > 23:
            print (c1[i],c2[i],sep='\t\t')
        elif len(c1[i]) > 15:
            print (c1[i],c2[i],sep='\t\t\t')
        elif len(c1[i]) > 7:
            print (c1[i],c2[i],sep='\t\t\t\t')
        else:
            print (c1[i],c2[i],sep='\t\t\t\t\t')

def SelRaza(lista_de_razas):
    '''Provee un selector de razas.'''
    
    print('\nSeleccione Raza \n1: Humano 2: Enano 3: Elfo 4: Gnomo\n5: Mediano 6: Semielfo 7: Semiorco\n')

    raza = ''
    while raza not in lista_de_razas:
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
        if raza not in lista_de_razas:
            print('Raza inválida o error ortográfico, intente nuevamente\n')
        print ('Has elegido que este personaje sea un '+lista_de_razas[raza][0]+'.', end = ' ')
        if not input ('¿Estas seguro? ').lower().startswith('s'):
            raza = ''
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

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

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