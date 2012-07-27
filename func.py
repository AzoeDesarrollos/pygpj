# coding=UTF-8
from random import randint
from sels import subselector , SelDot
import os
import setup as s
import prsnj as p

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

def PuntHab (lista_de_clases,clase,nivel,INT_mod,subtipo):
    '''Devuelve los puntos de habilidad a repartir para el nivel de clase.'''
    
    PH = lista_de_clases[clase]['PH']+INT_mod
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
    
    cls = []
    for i in lista_de_clases[clase]['Claseas']:
        cls.append(lista_de_hab[i]['Nombre'])
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

def ValPreReq (ID_dote,lista_de_dotes,nv_cls,nivel,dotes,rangos,aptitudes,stats,caract,comp_armas):
    '''Verifica que se cumplan los prerrequisitos de la dote seleccionada.'''
    
    
    ID = int(ID_dote.split(':')[0])
    if len(ID_dote.split(':'))>1:
        sub = int(ID_dote.split(':')[1])
    
    Req = lista_de_dotes[ID]['Tipo'].split(':')
    if Req[0] == 'u': ## Requisito de Tipo (Presencia/Ausencia de Dotes)
        if ID_dote in dotes:
            return False
        else:
            valido = 1
    elif Req[0] == 's':
        valido = 1
    
    if 'Consideracion' in lista_de_dotes[ID]: ## Consideración de Clase ('se considera que ya posee
        Reqs = lista_de_dotes[ID]['Consideracion']## esta dote, por lo que no necesita elegirla')
        for Req in Reqs:
            Req = Req.split(' ')
            if Req[0] in nv_cls:
                if nv_cls.count(Req[0]) >= int(Req[1]):
                    return False
                else:
                    valido = 1
            else:
                valido = 1
    
    if 'Req_Cls' in lista_de_dotes[ID]: ## Requisito de Nivel de Clase
        Req = lista_de_dotes[ID]['Req_Cls']
        if Req[0] in nv_cls:
            if nv_cls.count(Req[0]) >= int(Req[1]):
                valido = 1
            else:
                return False
        else:
            return False
    
    if 'Req_NvPj' in lista_de_dotes[ID]: ## Requisito de Nivel de Personaje
        if len(nv_cls)>= int(lista_de_dotes[ID]['Req_NvPj']):
            valido = 1
        else:
            return False
    
    if 'Req_NL' in lista_de_dotes[ID]: ## Requisito de nivel de lanzador
        valido = 1
    
    if 'Req_Dts' in lista_de_dotes[ID]: ## Requisito de Dotes
        Reqs = lista_de_dotes[ID]['Req_Dts']
        for Req in Reqs:
            if ':' in Req:
                dt = str(Req.split(':')[0])
                sb = str(Req.split(':')[1])
                if sb == 'sub':
                    if dt+':'+sb in dotes:
                        valido = 1
                    else:
                        return False
                else:
                    if Req.split(':')[0]+':'+sb in dotes:
                        valido = 1
                    else:
                        return False
            else:
                if Req in dotes:
                    valido = 1
                else:
                    return False
    
    if 'Req_Comp' in lista_de_dotes[ID]: ## Requisito de Competencias en Armas
        if lista_de_dotes[ID]['Req_Comp'] == '#':
            if sub in comp_armas:
                valido = 1
            else:
                return False
        else:
            Reqs = lista_de_dotes[ID]['Req_Comp']
            for Req in Reqs:
                if Req in comp_armas:
                    valido = 1
                else:
                    return False
    
    if 'Req_Hab' in lista_de_dotes[ID]: ## Requisito de Rangos de Habilidad
        Req = lista_de_dotes[ID]['Req_Hab'].split(':')
        hab = int(Req[0])
        val = int(Req[1])
        if rangos[hab] >= val:
            valido = 1
        else:
            return False
    
    if 'Req_Apts' in lista_de_dotes[ID]: ## Requisito de Aptitudes Especiales
        Reqs = lista_de_dotes[ID]['Req_Apts']
        for Req in Reqs:
            if Req in aptitudes:
                valido = 1
            else:
                return False
    
    if 'Req_Stats' in lista_de_dotes[ID]: ## Requisito de Ataque base y TSs
        Req = lista_de_dotes[ID]['Req_Stats'].split(':')
        if stats[int(Req[0])] >= int(Req[1]):
            valido = 1
        else:
            return False
    
    if 'Req_Car' in lista_de_dotes[ID]: ## Requisito de Puntuaciones de Caracteristica
        Reqs = lista_de_dotes[ID]['Req_Car']
        for Req in Reqs:
            car = Req.split(':')[0]
            val = Req.split(':')[1]
            if caract[int(car)] >= int(val):
                valido = 1
            else:
                return False
            
    if valido == 1:
        return True
    else:
        return False

def AutoDot (DOTES,comp_armas,ARMAS,lista_de_habilidades,sub=None):
    '''Autoelige dotes como si no tuvieran prerrequisitos. '''

    mec = [DOTES[i]['Tipo'] for i in range(len(DOTES))]

    escuelas = ['Abjuración','Adivinación','Conjuración','Encantamiento','Evocación',
                'Ilusión','Nigromancia','Transmutación'] ## TEMPORAL y TRANSITORIA
    dotes = []
    
    if sub == None:
        indexes = range(len(DOTES))
    else:
        indexes = [i for i in sub]
    
    for i in indexes:
        if mec[i] == 'u:h':
            for h in range(len(lista_de_habilidades)):
                dotes.append(str(i)+':'+str(h))
        elif mec[i] in ('u:w','u:w?'):
            for w in comp_armas:
                dotes.append(str(i)+':'+str(w))
        elif mec[i] == 'u:m':
            for m in range(len(ARMAS)):
                if ARMAS[m]['Competencia'] == i:
                    if m not in comp_armas:
                        dotes.append(str(i)+':'+str(m))
        elif mec[i] == 'u:e':
            for e in range(len(escuelas)):
                dotes.append(str(i)+':'+str(e))
        else:
            dotes.append(str(i))

    return dotes

def GenerarListadeAyuda (todas_las_dotes,lista_de_dotes):
    '''Evalúa las dotes autoelegidas verificando prerrequisitos. '''
    
    posibles = []
    for ID in todas_las_dotes:
        if ValPreReq(ID,lista_de_dotes,p.clases,p.nivel,p.dotes,p.rng,p.apps,p.stats,p.CARS,p.compW):
            posibles.append(ID)
    
    ayuda = []
    for i in posibles:
        if i.isnumeric():
            ayuda.append(int(i))
        else:
            ID = int(i.split(':')[0])
            if ID not in ayuda:
                ayuda.append(ID)

    return ayuda

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
    imp = ''
    lineas = []
    for elemento in lista:
        imp += str(elemento)+', '
        if len(imp) > 75:
            lineas.append(imp)
            imp = ''
            
    lineas.append(imp)
    imprimir = '\n'.join(lineas).rstrip(', ')+'.'

    return imprimir

def paginar (tam_pag,lineas):
    for i in range(len(lineas)):
        if (i+1) % tam_pag == 0:
            input ('\n[Presione Enter para continuar]\n')
            #os.system(['clear','cls'][os.name == 'nt'])
        print (lineas[i])

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

def a_dos_columnas(items):
    c1 = []
    c2 = []

    for i in range(len(items)):
        if i < len(items)/2:
            c1.append(items[i])
        else:
            c2.append(items[i])

    if len(c1) > len(c2):
        for i in range(len(c1)-len(c2)):
            c2.append('')

    lineas = []
    for i in range(len(c1)):
        if len(c1[i]) > 32:
            lineas.append(c1[i] +'\t'+ c2[i])
        elif len(c1[i]) > 23:
            lineas.append(c1[i] +'\t'*2+ c2[i])
        elif len(c1[i]) > 15:
            lineas.append(c1[i] +'\t'*3+ c2[i])
        elif len(c1[i]) > 7:
            lineas.append(c1[i] +'\t'*4+ c2[i])
        else:
            lineas.append(c1[i] +'\t'*5+ c2[i])

    return lineas

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

def actualizar_aptitudes (ap,APSmc,apps_pj,dotes,DOTES,HABS,clase,sub = ''):
    '''Actuliza la lista de aptitudes del personaje.'''
    
    nom = APSmc[ap]['Nombre']
    tipo = APSmc[ap]['Tipo'].split(':')[0]
    if ':' in APSmc[ap]['Tipo']:
        mec = APSmc[ap]['Tipo'].split(':')[1]
    if 'Sublista' in APSmc[ap]:
        sub = APSmc[ap]['Sublista']
        prompt = APSmc[ap]['Sub_Sel']
    
    if tipo == 'u':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub)
            p.apps.append(str(ap)+':'+str(elec))
        else:
            p.apps.append(str(ap))

    elif tipo == 'v':
        p.apps.append(ap)
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub,dos_col=True)
            p.apps.append(str(ap)+':'+str(elec))
        else:
            p.apps.append(str(ap))

    elif tipo == 'r':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub,dos_col=True)
            p.apps[apps.index(mec)] = str(ap)+':'+str(elec)
        else:
            p.apps[apps.index(mec)] = str(ap)
        
    elif tipo == 'a':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub)
            p.dotes.append(str(DOTES.index(sub[elec])))
        else:
            p.dotes.append(str(APSmc[ap]['ID_dt']))

    elif tipo == 'd':
        p.dt_cl = True

    elif tipo == 'x':
        e = SelAE (APSmc,apps_pj)
        if e == 'd':
            p.dotes.append(SelDot(p.nivel,dotes,DOTES,p.compW,s.ARMAS,s.HABS,False,clase))
        else:
            p.apps.append(e)
