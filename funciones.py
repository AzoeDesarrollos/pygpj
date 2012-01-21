# coding=UTF-8
from random import randint

# Función Tirar Definitiva #
# Puede tirar cualquier combinación de dados.
def Tirar(losdados,Max=False):
        # Primero descompone el string con las tiradas. Créditos a Ein.
        lista_de_dados = []
        temp = -1
        indexes = []
        for i in range (losdados.count('+')):
                temp = losdados.find('+',temp+1)
                indexes.append(temp)
        temp = -1
        for i in range (losdados.count('-')):
                temp = losdados.find('-',temp+1)
                indexes.append(temp)
        temp = 0
        indexes.sort()
        for i in indexes:
                lista_de_dados.append(losdados[temp:i])
                temp = i
        lista_de_dados.append(losdados[temp:])

        # Luego descompone las tiradas en tuples con la cantidad y el tipo.
        if lista_de_dados[0] == '': # en caso de notación -#d#
                del lista_de_dados[0]
        individuales = []
        total = 0
        for dados in lista_de_dados:
                if 'd' not in dados: # Modificador
                        individuales.append(int(dados))
                else:
                        temp = dados.split('d')
                        if temp[0] == '':
                                Cantidad = 1
                        elif temp[0] == '-': # en caso de notación -d#
                                Cantidad = -1
                        else:
                                Cantidad = int(temp[0])
                        Tipo = int(temp[1])
                        individuales.append((Cantidad,Tipo))

        # Finalmente realiza todas las tiradas y suma los resultados.
        for tirada in individuales:
                if type(tirada)==int: # Modificador
                        total += tirada
                else:
                        Cantidad = tirada[0]
                        Tipo = tirada[1]
                        if Max == True:
                            resultado = Cantidad*Tipo
                        elif Cantidad < 0:
                            resultado = -(randint(-Cantidad, Tipo*(-Cantidad)))
                        else:
                            resultado = randint(Cantidad, Tipo*Cantidad)
                        total += resultado
        return total

def UnaCar ():
    car = [Tirar('d6'),Tirar('d6'),Tirar('d6'),Tirar('d6')]
    car.sort(reverse=True)
    del car[-1]
    Car = sum(car)
    return Car

def GenTir():
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

def RepPunto(lista,Car):
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

def SelCla(nv_pj): # Selector de Clases
    clases = []
    temp = nv_pj
    nv = 1
    CLASES = ('Barbaro','Bardo','Brb','Brd','Bárbaro','Clerigo','Clr','Clérigo','Drd','Druida','Exp','Explorador','Gue',
              'Guerrero','Hcr','Hechicero','Mag','Mago','Mnj','Monje','Paladin','Paladín','Pcr','Picaro','Pld','Pícaro',
              'barbaro','bardo','brb','brd','bárbaro','clerigo','clr','clérigo','drd','druida','exp','explorador','gue',
              'guerrero','hcr','hechicero','mag','mago','mnj','monje','paladin','paladín','pcr','picaro','pld','pícaro')
    while temp > 0:
        cla = input('Nv '+str(nv)+'º: ')
        if cla not in CLASES:
            print ('seleccione una clase válida.')
        else:
            clases.append(cla)
            temp -= 1
            nv += 1
    CLASES = ('Brb','Brd','Clr','Drd','Exp','Gue','Hcr','Mag','Mnj','Pld','Pcr')
    fin_cla = []
    for cla in clases:
        if cla in CLASES:
            fin_cla.append(cla)
        elif cla.capitalize() in CLASES:
            fin_cla.append(cla.capitalize())
        elif cla in ('Bárbaro','bárbaro','barbaro','Barbaro'):
            fin_cla.append('Brb')
        elif cla in ('Bardo','bardo'):
            fin_cla.append('Brd')
        elif cla in ('Clérigo','clérigo','clerigo','Clerigo'):
            fin_cla.append('Clr')
        elif cla in ('Druida','druida'):
            fin_cla.append('Drd')
        elif cla in ('Explorador','explorador'):
            fin_cla.append('Exp')
        elif cla in ('Guerrero','guerrero'):
            fin_cla.append('Gue')
        elif cla in ('Hechicero','hechicero'):
            fin_cla.append('Hcr')
        elif cla in ('Mago','mago'):
            fin_cla.append('Mag')
        elif cla in ('Monje','monje'):
            fin_cla.append('Mnj')
        elif cla in ('Paladín','paladín','paladin','Paladin'):
            fin_cla.append('Pld')
        elif cla in ('Pícaro','pícaro','picaro','Picaro'):
            fin_cla.append('Pcr')
    return fin_cla

def ProCla(INT_mod,lista_de_clases): # Procesador de Clases y Niveles
    # Primero, procesaremos los niveles de clase
    temp, nv_cls = [],[]
    for clase in lista_de_clases:
        if clase in temp:
            nv = temp.count(clase)
            nv +=1
            temp.append(clase)
            nv_cls.append(nv)
        else:
            temp.append(clase)
            nv_cls.append(1)
        
    # a continuación, usamos el calculador de personajes para calcular los TSs y el Ataque base
    ATKb, TS_Fort, TS_Ref, TS_Vol = 0,0,0,0
    
    for clase in lista_de_clases: # Ataque base
        if clase in ('Brb','Exp','Gue','Pld'):
            ATKb += 1
        elif clase in ('Brd','Clr','Drd','Mnj','Pcr'):
            ATKb += 3/4
        elif clase in ('Hcr','Mag'):
            ATKb += 1/2
    temp = -1
    for clase in lista_de_clases: # TS de Fortaleza
        if clase in ('Brb','Clr','Drd','Exp','Gue','Mnj','Pld'):
            TS_Fort += 1/2
            temp = lista_de_clases.index(clase,temp+1)
            if nv_cls[temp] == 1:
                TS_Fort += 2 
        else:
            TS_Fort += 1/3
    temp = -1
    for clase in lista_de_clases: # TS de Reflejos
        if clase in ('Brd','Exp','Mnj','Pcr'):
            TS_Ref += 1/2
            temp = lista_de_clases.index(clase,temp+1)
            if nv_cls[temp] == 1:
                TS_Ref += 2 
        else:
            TS_Ref += 1/3
    temp = -1
    for clase in lista_de_clases: # TS de Voluntad
        if clase in ('Brd','Clr','Drd','Hcr','Mag','Mnj'):
            TS_Vol += 1/2
            temp = lista_de_clases.index(clase,temp+1)
            if nv_cls[temp] == 1:
                TS_Vol += 2
        else: 
            TS_Vol += 1/3

    # Ahora los puntos de habilidad
    PH = 0
    PH_nv = []
    nv_pj = list(range(1,len(lista_de_clases)+1))
    temp = -1

    for clase in lista_de_clases:
        if clase in ('Clr','Gue','Hcr','Mag','Pld'): # 2 + INT por nivel
            PH += INT_mod + 2
            temp = lista_de_clases.index(clase,temp+1)
            if nv_pj[temp] == 1:
                PH *= 4
        elif clase in ('Brb', 'Drd','Mnj'): # 4 + INT por nivel
            PH += INT_mod + 4
            temp = lista_de_clases.index(clase,temp+1)
            if nv_pj[temp] == 1:
                PH *= 4
        elif clase in ('Brd','Exp'): # 6 + INT por nivel
            PH += INT_mod + 6
            temp = lista_de_clases.index(clase,temp+1)
            if nv_pj[temp] == 1:
                PH *= 4
        elif clase in ('Pcr'): # 8 + INT por nivel
            PH += INT_mod + 8
            temp = lista_de_clases.index(clase,temp+1)
            if nv_pj[temp] == 1:
                PH *= 4
        PH_nv.append(PH)
        PH = 0

    # Dotes por nivel
    dts = 1
    for i in range (2, len(lista_de_clases)+1):
        if i%3==0:
            dts += 1
    # de momento, el programa devuelve lo calculado hasta ahora...
    return (int(ATKb),int(TS_Fort),int(TS_Ref),int(TS_Vol),PH_nv,dts)

def PG (lista_de_clases,CON_Mod):
    DG = {'Hcr':'d4','Mag':'d4','Brd':'d6','Pcr':'d6','Clr':'d8','Drd':'d8',
          'Exp':'d8','Mnj':'d8','Gue':'d10','Pld':'d10','Brb':'d12'}
    temp = []
    PGs = 0
    PrimDG = True
    impr = []
    for clase in lista_de_clases:
        impr.append(DG[clase])
        if CON_Mod < 0:
                temp.append(DG[clase]+str(CON_Mod))
        else:
                temp.append(DG[clase]+'+'+str(CON_Mod))

    for t in temp:
        if PrimDG == True:
            PGs += Tirar(t,Max=True)
            PrimDG = False
        else:
            PGs += Tirar(t)
    
    tempD,tempN,tempF = [],[],[]
    modif = CON_Mod*len(lista_de_clases)
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
        prim = prim.rstrip(' más ')+'+'+str(modif)
        
    return PGs,prim

def SelRaza():
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

def CarMod(car):
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)
