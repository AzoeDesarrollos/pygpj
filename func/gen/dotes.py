# coding=UTF-8
# dotes.py
import func.gen.viz as v
from func.data.setup import data as s
from func.core.lang import t,probar_input
from func.core.prsnj import Pj as p
from func.core.intro import imprimir_titulo
import os

def elegir_dotes (dotes,clase):
    
    opciones = [t('Elegir una nueva dote'),
                t('Ver las dotes que ya se tienen'),
                t('Ver una lista de las dotes elegibles'),
                t('Ver información sobre una dote específica'),
                t('Ver una lista de todas las dotes')]
    
    while True:
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (v.barra(p.CARS,s.alinis[p.alini],p.raza['Nombre']))
        print(t('Seleccione sus Dotes para este nivel'))
        sublista = posicion(p.e_dts,clase,len(p.cla),s.CLASES,s.DOTES)
        print ('\n'+t('¿Que desea hacer?'))
        op = v.subselector(t('Opción'),opciones)
        if op == 0: # Elegir una nueva dote
            if not any(p.e_dts.values()):
                print('\n'+t('No se pueden elegir más dotes por el momento'))
            else:
                posibles = GenerarListadeAyuda(p,AutoDot(s.DOTES,sublista[0],p.compW,p.conjuros,
                                                         s.ARMAS,s.HABS,s.ESCUELAS),s.DOTES)
                dote = SelDot(p,s.DOTES,posibles)
                if dote != '':
                    dotes.append(dote)
                    p.e_dts[sublista[1]] = False
                if not any(p.e_dts.values()):
                    opciones.append(t('Nada más'))
        elif op == 1: # Ver las dotes que ya se tienen
            if len(dotes) < 1:
                print(t('No hay dotes elegidas de momento'))
            else:
                lista = ver_dotes (dotes,s.DOTES,s.ARMAS,s.HABS,s.ESCUELAS)
                v.paginar_dos_columnas(15,lista)
        elif op == 2: # Ver una lista de las dotes elegibles
            if not any(p.e_dts.values()):
                print('\n'+t('No se pueden elegir más dotes por el momento'))
            else:
                posibles = GenerarListadeAyuda(p,AutoDot(s.DOTES,sublista[0],p.compW,p.conjuros,
                                                       s.ARMAS,s.HABS,s.ESCUELAS),s.DOTES)
                v.paginar_dos_columnas(15,[s.DOTES[i]['Nombre'] for i in posibles])
        elif op == 3: # Ver información sobre una dote específica
            print(info_dote (s.DOTES))
        elif op == 4: # Ver una lista de todas las dotes
            lista_de_dotes(s.DOTES)
        elif op == 5:
            return dotes

        input (t('\n[Presione Enter para continuar]\n'))

def posicion (espacios,clase,nivel,CLASES,DOTES):
    i,d = -1,0
    sublista = [[0,''],[0,''],[0,'']]
    
    if any(espacios.values()):
        i += 1
        if espacios['dt_rcl'] == True:
            if d == 0: ind = '> '
            else: ind = '* '
            print('\n'+ind+t('Como aptitud racial, tienes una dote adicional para elegir.'))
            sublista[0][0] = [i for i in range(len(DOTES))]
            sublista[0][1] = 'dt_rcl'
        else:
            d += 1
        
        if espacios['dt_nv'] == True:
            if d == 1: ind = '> '
            else: ind = '* '
            print('\n'+ind+t('En el ')+t(str(nivel)+'º')+t(' nivel, tienes una dote para elegir.'))
            sublista[1][0] = [i for i in range(len(DOTES))]
            sublista[1][1] = 'dt_nv'
        else:
            d += 1

        if espacios['dt_cls'] == True:
            if d == 2: ind = '> '
            else: ind = '* '
            print('\n'+ind+t('Como aptitud de clase, tienes una dote adicional para elegir.'))
            sublista[2][0] = CLASES[clase]['dt_cls']
            sublista[2][1] = 'dt_cls'
                   
    return sublista[d]

def SelDot (p,DOTES, posibles):
    nom = [DOTES[i]['Nombre'] for i in range(len(DOTES))]
    des = [DOTES[i]['Descripcion'] for i in range(len(DOTES))]
    mec = [DOTES[i]['Tipo'] for i in range(len(DOTES))]
    pre = []
    for i in range(len(DOTES)):
        if 'PreReq' in DOTES[i]:
            pre.append(DOTES[i]['PreReq'])
        else:
            pre.append('')
            
    dote = ''
    while dote == '':
        dt = ''
        while dt == '':
            dt = input(t('\nDote')+': ').strip().capitalize()
            dt = probar_input (dt,nom)
            if dt == '':
                print (t('Escriba el nombre de una dote')+'\n')
        
        if dt in (t('Volver'),t('Salir')):
            break
        
        
        if nom.index(dt) not in posibles:
            print (t('Actualmente el personaje no cumple con los prerrequisitos para la dote seleccionada'),
                   t('Elija otra'), sep = '\n')
        elif ':' in mec[nom.index(dt)]:
            sub = mec[nom.index(dt)].split(':')[1]
            if sub == 'w':
                dote = u_w (dt,p.compW,p.dotes,s.ARMAS,nom,pre,des)
            elif sub == 'w?':
                dote = u_w2 (dt,nom,pre,des)
            elif sub == 'm':
                dote = u_m (dt,p.compW,p.dotes,nom,pre,des,s.ARMAS)
                aplicar_dote (dote,s.DOTES,s.ARMAS,s.ARMDS)
            elif sub == 'e':
                dote = u_e (dt,p.dotes,s.ESCUELAS,nom,pre,des)
            elif sub == 'e?':
                dote = (dt,nom,pre,des)
            elif sub == 'c':
                dote = u_c (dt,p.CARS_mods[3],p.conjuros,s.CONJUROS,nom,pre,des)
        else:
            dote = str(nom.index(dt))
            prinfo (dt,nom,pre,des)
        
        if dote != '':
            if not input('\n'+t('¿Estas seguro? ')).lower().startswith(t('s')):
                dote = ''
    
    return dote

def u_w (dt,comp_armas,dotes_pj,ARMAS,nom,pre,des):
    print ('Para la dote seleccionada debes elegir un arma con la que seas competente',
           'Elije una: ', sep = '\n')
    armas = []
    for i in comp_armas:
        if  str(nom.index(dt))+':'+str(i) not in dotes_pj:
            armas.append(ARMAS[i]['Nombre'])
    armas.sort()
    arma = v.subselector('Arma',armas,dos_col=True)
    prinfo (dt,nom,pre,des)
    dote = comprobacion (dt,nom,ARMAS,armas,arma)
    return dote

def u_w2 (dt,nom,pre,des):
    print ('Para la dote seleccionada debes elegir un arma de entre las siguientes',
           'Elije una',sep = '\n')
    subs = AutoDot(DOTES,[nom.index(dt)],p.compW,p.conjuros,s.ARMAS,s.HABS,s.ESCUELAS)
    armas = []
    for ID in subs:
        if validar_requisitos(ID,DOTES):
            armas.append(int(ID.split(':')[1]))
    arma = v.subselector('Arma',armas)
    prinfo (dt,nom,pre,des)
    dote = comprobacion (dt,nom,ARMAS,armas,arma)
    return dote

def u_m (dt,comp_armas,dotes_pj,nom,pre,des,ARMAS):
    print ('Para la dote seleccionada debes elegir un arma con la que no seas competente',
           'Elije una: ', sep = '\n')
    armas = []
    for i in range(len(ARMAS)):
        if ARMAS[i]['Competencia'] == nom.index(dt):
            if i not in comp_armas:
                if str(nom.index(dt))+':'+str(i) not in dotes_pj:
                    armas.append(ARMAS[i]['Nombre'])

    arma = v.subselector('Arma',armas,dos_col=True)
    prinfo (dt,nom,pre,des)
    dote = comprobacion (dt,nom,ARMAS,armas,arma)
    return dote

def u_e (dt,dotes_pj,ESCUELAS,nom,pre,des):
    print ('Para la dote seleccionada debes elegir una escuela de magia',
           'Elije una: ', sep = '\n')
    escuelas = []
    for i in range(len(ESCUELAS)):
        if str(nom.index(dt))+':'+str(i) not in dotes_pj:
            escuelas.append(ESCUELAS[i]["Nombre"])
    
    esc = v.subselector('Escuela',escuelas,dos_col=True)
    prinfo (dt,nom,pre,des)
    dote = str(nom.index(dt))+':'+str(ESCUELAS.index(escuelas[esc]))
    return dote

def u_e2 (dt,nom,pre,des):
    print ('Para la dote seleccionada debes elegir una escuela de magia'+
           ' de entre las siguientes','Elije una',sep = '\n')
    subs = AutoDot(s.DOTES,[nom.index(dt)],p.compW,p.conjuros,s.ARMAS,s.HABS,s.ESCUELAS)
    escuelas = []
    for ID in subs:
        if validar_requisitos(ID,s.DOTES):
            escuelas.append(int(ID.split(':')[1]))
    esc = v.subselector('Escuela',escuelas)
    prinfo (dt,nom,pre,des)
    dote = comprobacion (dt,nom,s.ESCUELAS,escuelas,esc)
    return dote

def u_c (dt,INT_mod,cnj_pj,CONJUROS,nom,pre,des):
    print ('Para la dote seleccionada debes elegir un conjuro')
    subs = AutoDot(s.DOTES,[nom.index(dt)],p.compW,p.conjuros,s.ARMAS,s.HABS,s.ESCUELAS)
    conjs = []
    for ID in subs:
        if validar_requisitos(ID,DOTES):
            conjs.append(CONJUROS[int(ID.split(':')[1])]['Nombre'])
    cnj = v.subselector('Conjuro',conjs,vueltas=INT_mod)
    prinfo (dt,nom,pre,des)
    dote = comprobacion (dt,nom,CONJUROS,conjs,cnj)
    return dote

def prinfo (dt,nom,pre,des):
    print ('Prerrequisitos: '+pre[nom.index(dt)]+' (cumplidos)\n'+des[nom.index(dt)])

def comprobacion (dt,nom,GRUPO,lista,item):
    for i in range(len(GRUPO)):
        if GRUPO[i]['Nombre'] == lista[item]:
            dote = str(nom.index(dt))+':'+str(i)
    return dote

def validar_requisitos (p,ID_dote,DOTES):
    '''Verifica que se cumplan los prerrequisitos de la dote seleccionada.'''
    
    ID = int(ID_dote.split(':')[0])
    if len(ID_dote.split(':'))>1:
        sub = int(ID_dote.split(':')[1])
    else:
        sub = None

    if not req_tipo (ID,ID_dote,p.dotes,DOTES):
        return False

    if 'Consideracion' in DOTES[ID]:
        if not req_considera (ID,p.cla,DOTES):
            return False
        
    if 'Req_Cls' in DOTES[ID]: 
        if not req_clase (ID,p.cla,DOTES):
            return False
        
    if 'Req_NvPj' in DOTES[ID]:
        if not req_nv_pj (ID,p.cla,DOTES):
            return False
        
    if 'Req_NL' in DOTES[ID]:
        if not req_nl (ID,p.NL,DOTES):
            return False
        
    if 'Req_Dts' in DOTES[ID]:
        if not req_dotes(ID,p.dotes,DOTES):
            return False
        
    if 'Req_Comp' in DOTES[ID]:
        if not req_competencia (ID,p.compW,sub,DOTES):
            return False
        
    if 'Req_Hab' in DOTES[ID]:
        if not req_habilidad (ID,p.rng,DOTES):
            return False
        
    if 'Req_Apts' in DOTES[ID]:
        if not req_aptitudes (ID,p.apps,DOTES):
            return False
        
    if 'Req_Stats' in DOTES[ID]:
        if not req_stats (ID,p.stats,DOTES):
            return False
        
    if 'Req_Car' in DOTES[ID]:
        if not req_caracteristica (ID,p.CARS,DOTES):
            return False
    
    return True
    
def req_tipo (ID,ID_dote,dotes_pj,DOTES):
    Req = DOTES[ID]['Tipo'].split(':')
    if Req[0] == 'u': ## Requisito de Tipo (Presencia/Ausencia de Dotes)
        if ID_dote in dotes_pj:
            return False
        else:
            return True
    elif Req[0] == 's':
        return True

def req_considera (ID,nv_cls,DOTES): ## Consideración de Clase ('se considera que ya posee
    Reqs = DOTES[ID]['Consideracion']## esta dote, por lo que no necesita elegirla')
    for Req in Reqs:
        Req = Req.split(' ')
        if Req[0] in nv_cls:
            if nv_cls.count(Req[0]) >= int(Req[1]):
                return False            
    return True

def req_clase (ID,nv_cls,DOTES): ## Requisito de Nivel de Clase
    Req = DOTES[ID]['Req_Cls'].split(' ')
    if Req[0] in nv_cls:
        if nv_cls.count(Req[0]) >= int(Req[1]):
            return True
        else:
            return False
    else:
        return False

def req_nv_pj (ID,nv_cls,DOTES): ## Requisito de Nivel de Personaje
    if len(nv_cls)>= int(DOTES[ID]['Req_NvPj']):
        return True
    else:
        return False

def req_nl (ID,NL,DOTES): ## Requisito de nivel de lanzador
    if any([True for i in NL.values() if i > DOTES[ID]['Req_NL']]):
        return True

def req_dotes (ID,dotes_pj,DOTES): ## Requisito de Dotes
    Reqs = DOTES[ID]['Req_Dts']
    for Req in Reqs:
        if ':' in Req:
            dt = str(Req.split(':')[0])
            sb = str(Req.split(':')[1])
            if sb == 'sub':
                if dt+':'+sb in dotes_pj:
                    return True
                else:
                    return False
            else:
                if Req.split(':')[0]+':'+sb in dotes_pj:
                    return True
                else:
                    return False
        else:
            if Req in dotes_pj:
                return True
            else:
                return False

def req_competencia (ID,comp_armas,sub,DOTES): ## Requisito de Competencias en Armas
    if DOTES[ID]['Req_Comp'] == '#':
        if sub in comp_armas:
            return True
        else:
            return False
    else:
        Reqs = DOTES[ID]['Req_Comp']
        for Req in Reqs:
            if Req in comp_armas:
                return True
            else:
                return False

def req_habilidad (ID,rangos,DOTES): ## Requisito de Rangos de Habilidad
    Req = DOTES[ID]['Req_Hab'].split(':')
    hab = int(Req[0])
    val = int(Req[1])
    if rangos[hab] >= val:
        return True
    else:
        return False

def req_aptitudes (ID,apts_pj,DOTES):## Requisito de Aptitudes Especiales
    Reqs = DOTES[ID]['Req_Apts']
    for Req in Reqs:
        if Req in apts_pj:
            return True
        else:
            return False

def req_stats (ID,stats,DOTES): ## Requisito de Ataque base y TSs
    Req = DOTES[ID]['Req_Stats'].split(':')
    if stats[int(Req[0])] >= int(Req[1]):
        return True
    else:
        return False

def req_caracteristica (ID,caract,DOTES):## Requisito de Puntuaciones de Caracteristica
    Reqs = DOTES[ID]['Req_Car']
    for Req in Reqs:
        car = int(Req.split(':')[0])
        val = int(Req.split(':')[1])
        if caract[car] >= val:
            return True
        else:
            return False
    Reqs = DOTES[ID]['Req_Car']
    for Req in Reqs:
        car = int(Req.split(':')[0])
        val = int(Req.split(':')[1])
        if caract[car] >= val:
            return True
        else:
            return False

def AutoDot (DOTES,sublista,comp_armas,conjuros,ARMAS,HABS,ESCUELAS):
    '''Autoelige dotes como si no tuvieran prerrequisitos. '''

    mec = [DOTES[i]['Tipo'] for i in range(len(DOTES))]
    dotes = []
    
    if sublista == DOTES:
        indexes = range(len(DOTES))
    else:
        indexes = [i for i in sublista]
    
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
        elif mec[i] == 'u:e':
            for e in range(len(ESCUELAS)):
                dotes.append(str(i)+':'+str(e))
        elif mec[i] == 'u:c':
            for c in conjuros:
                dotes.append(str(i)+':'+str(c))
        else:
            dotes.append(str(i))

    return dotes

def GenerarListadeAyuda (p,todas_las_dotes,lista_de_dotes):
    '''Evalúa las dotes autoelegidas verificando prerrequisitos. '''
    
    posibles = []
    for ID in todas_las_dotes:
        if validar_requisitos(p,ID,lista_de_dotes):
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

def ver_dotes (dotes_pj,DOTES,ARMAS,HABS,ESCUELAS):
    _dotes_ = [DOTES[i]['Nombre'] for i in range(len(DOTES))]
    _armas_ = [ARMAS[i]['Nombre'] for i in range(len(ARMAS))]
    _habs_ = [HABS[i]['Nombre'] for i in range(len(HABS))]
    mec = [DOTES[i]['Tipo'] for i in range(len(DOTES))]
    imprimir = []
    for i in dotes_pj:
        if i.isnumeric():
            imprimir.append(_dotes_[int(i)])
        elif ':' in i:
            dt = int(i.split(':')[0])
            sub = int(i.split(':')[1])
            if mec[dt].split(':')[1] in ('m','w','w?'):
                imprimir.append(_dotes_[dt]+' ('+_armas_[sub]+')')
            elif mec[dt].split(':')[1] == 'h':
                imprimir.append(_dotes_[dt]+' ('+_habs_[sub]+')')
            elif mec[dt].split(':')[1] in ('e','e?'):
                imprimir.append(_dotes_[dt]+' ('+ESCUELAS[sub]+')')
    return imprimir

def lista_de_dotes(DOTES):
	lista = [DOTES[i]['Nombre'] for i in range(len(DOTES))]
	v.paginar_dos_columnas(15,lista)

def info_dote (DOTES):
    '''Devuelve la info completa de una dote por su nombre.'''
    
    dotes = [DOTES[i]['Nombre'] for i in range(len(DOTES))]

    dote = input('\nDote: ').capitalize()
    dote = probar_input (nom,'Dote',dote)
            
    for i in range(len(DOTES)):
        if DOTES[i]['Nombre'] == dote:
            if 'PreReq' in DOTES[i]:
                texto = '\n'.join(('Prerrequisitos: '+DOTES[i]['PreReq'],
                                   DOTES[i]['Descripcion']))
            else:
                texto = DOTES[i]['Descripcion']
    return texto

def aplicar_dote (nueva_dote,DOTES,ARMAS,ARMDS):
    if ':' in nueva_dote:
        if nueva_dote.split(':')[0] in ('26','27'):
            if int(nueva_dote.split(':')[1]) not in p.compW:
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
