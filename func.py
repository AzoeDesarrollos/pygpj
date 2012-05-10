# coding=UTF-8
from random import randint

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

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

def AppClas (APPdict,clase,nv_cls):
    '''Devuelve las aptitudes de la clase al nivel dado.'''
    
    nv_cls -= 1
    return APPdict[clase][nv_cls]