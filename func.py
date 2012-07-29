# coding=UTF-8
from random import randint
from sels import subselector , SelDot, SelAE
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

def Claseas (CLASES,clase,HABS):
    '''Devuelve las habilidades cláseas de la clase citada.'''
    
    cls = []
    for i in CLASES[clase]['Claseas']:
        cls.append(HABS[i]['Nombre'])
    return cls

def HabMod(hab_num,lista_habs,mods_de_caract,rangos, raciales, sinergias, dotes, objetos):
    '''Calcula el modificador final de habilidad.'''
    if 'Modificador' in lista_habs[hab_num]:
        mod = mods_de_caract[lista_habs[hab_num]['Modificador']]
        total = rangos[hab_num]+mod+raciales[hab_num]+sinergias[hab_num]+dotes[hab_num]+objetos[hab_num]
    
    return total

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

def AutoDot (DOTES,comp_armas,ARMAS,HABS,ESCUELAS,sub=None):
    '''Autoelige dotes como si no tuvieran prerrequisitos. '''

    mec = [DOTES[i]['Tipo'] for i in range(len(DOTES))]
    dotes = []
    
    if sub == None:
        indexes = range(len(DOTES))
    else:
        indexes = [i for i in sub]
    
    for i in indexes:
        if mec[i] == 'u:h':
            for h in range(len(HABS)):
                dotes.append(str(i)+':'+str(h))
        elif mec[i] in ('u:w','u:w?'):
            for w in comp_armas:
                dotes.append(str(i)+':'+str(w))
        elif mec[i] == 'u:m':
            for m in range(len(ARMAS)):
                if ARMAS[m]['Competencia'] == i:
                    if m not in comp_armas:
                        dotes.append(str(i)+':'+str(m))
        elif mec[i] in ('u:e','u:e?'):
            for e in range(len(ESCUELAS)):
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
            elec = subselector(prompt,sub,dos_col=True)
            p.apps.append(str(ap)+':'+str(elec))
        else:
            p.apps.append(str(ap))

    elif tipo == 'v':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub,dos_col=True)
            p.apps.append(str(ap)+':'+str(elec))
        elif ap == '83': ## Chapuza.. no me gusta
            p.apps.append(str(ap))
        else:
            p.apps.append(str(ap))

    elif tipo == 'r':
        if sub != '':
            print ('\n'+APSmc[ap]['Intro'])
            elec = subselector(prompt,sub,dos_col=True)
            p.apps[p.apps.index(mec)] = str(ap)+':'+str(elec)
        elif apps_pj.count(mec) > 1:
            while apps_pj.count(mec) >1:
                del p.apps[p.apps.index(mec)]
            p.apps[p.apps.index(mec)] = str(ap)
        else:
            p.apps[p.apps.index(mec)] = str(ap)
        
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
            p.dotes.append(SelDot(p.nivel,dotes,DOTES,p.compW,s.ARMAS,s.ESCUELAS,s.HABS,False,clase))
        else:
            p.apps.append(e)

def PG (CON_mod,DG,nivel):
    PG = 0
    if nivel == 1:
        PG += DG+CON_mod
    else:
        PG += randint(1,DG)+CON_mod

    return PG

def aplicar_dote (nueva_dote,DOTES,ARMAS,ARMDS):
    if ':' in nueva_dote:
        if nueva_dote.split(':')[0] in ('26','27'):
            p.compW.append(int(nueva_dote.split(':')[1]))
        elif nueva_dote.split(':')[0] == '28':
            for i in range(len(ARMAS)):
                if ARMAS[i]['Competencia'] == 28:
                    if i not in p.compW:
                        p.compW.append(i)
            p.compW.sort()
        elif nueva_dote.split(':')[0] in ('29','30','31'):
            for i in range(len(ARMDS)):
                if ARMDS[i]['Competencia'] == int(nueva_dote.split(':')[0]):
                    if i not in p.compA:
                        p.compA.append(i)
            p.compA.sort()
    elif nueva_dote.isnumeric:
        if 'Stat' in DOTES[int(nueva_dote)]:
            p.stats [DOTES[int(nueva_dote)]['Stat']] += 2
        elif nueva_dote == '65': ## especificidades que me gustaría eliminar
            p.iniciativa += 4
        elif nueva_dote == '51': ## especificidades que me gustaría eliminar
            p.PG += 3
