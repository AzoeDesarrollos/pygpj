# coding=UTF-8
'''Modulo de Exportación'''
from func.data.setup import data as s
from func.gen.habs import HabMod
from func.gen.dotes import ver_dotes
from func.core.config import guardar_json
from func.core.prsnj import Pj as p
from func.gen.objetos import imprimir_nom_objmag
from func.core.lang import t
from time import sleep,localtime,strftime
from math import floor
import os

def orden_habs_imprint (habs_pj,equipo,HABS,ARMDS):
    '''Ordena las habilidades que se van a imprimir.'''
    
    indexes = []
    imprimir = ''
    
    for hab in habs_pj:
        if any (habs_pj[hab].values()):
            indexes.append(hab)
    indexes.sort()
    
    # Eliminar las habilidades 'solo entrenadas' sin rangos
    for hab in indexes:
        if habs_pj[hab]['rng'] == 0:
            if 'Solo_entrenada' in HABS[hab]:
                x = indexes.index(hab)
                del indexes[x]
    
    pen_armd = 0
    if equipo['armd'] != '':
        pen_armd += ARMDS[equipo['armd']['index']]['Penalizador']
    if equipo['mm'] != '':
        if equipo['mm']['subgrupo'] == 'esc':
            pen_armd += ARMDS[equipo['mm']['index']]['Penalizador']
    
    for h in indexes:
        if 'Modificador' in HABS[h]:
            imprimir = imprimir+s.HABS[h]['Nombre']+' {:+}'.format(floor(HabMod(h,habs_pj,pen_armd,p.CARS,HABS)))+', '
    imprimir = imprimir.rstrip(', ')+'.'
    
    return imprimir

def imprimir_DG(clases_pj,CLASES,CON_mod,PG,dotes):
    tempD,tempN,tempF = [],[],[]
    modif = CON_mod*len(clases_pj)
    impr = []
    for d in clases_pj:
        impr.append('d'+str(CLASES[d]['DG']))
    
    for p in impr:
        if not p in tempD:
            tempD.append(p)
            tempN.append(str(impr.count(p)))

    for e in range(len(tempD)):
        tempF.append(tempN[e]+tempD[e])
    
    prim = ''
    for p in tempF:
        prim = prim+p+' más '

    if modif != 0:
        prim = prim.rstrip(' más ')+' {0:+}'.format(modif)
    else:
        prim = prim.rstrip(' más ')

    prim += ' ('+str(PG)+' pg)'
    return prim

def imprimir_apts (apts,APTS,aprin):
    for ap in apts:
        if 'Aptitud' in APTS[ap]:
            if 'Formato' in APTS[ap]:
                nom = APTS[ap]['Nombre']
                cant = apts[ap]['cant']
                if '2' in APTS[ap]['Formato']:
                    texto = APTS[ap]['Formato'].format(nom,cant,sub)
                else:
                    texto = APTS[ap]['Formato'].format(nom,cant)
            else:
                texto = APTS[ap]['Nombre']
        
        if APTS[ap]['Aptitud'] == 'Ataque especial':
            if texto not in aprin['Ataques']:
                aprin['Ataques'].append(texto)
        else:
            if texto not in aprin['Cualidades']:
                aprin['Cualidades'].append(texto)
    return aprin

def imprimir_clases (cla,CLASES):
    texto = []
    clases = [CLASES[str(i)]['Nombre'] for i in range(len(CLASES))]
    for i in range(len(clases)):
        if str(i) in cla:
            texto.append(clases[i]+' '+str(cla.count(str(i)))+'º')
    
    return ' '.join(texto)

def imprimir_ATK (equipo,ATKs,ARMAS,tam_pj,FUE_mod):
    
    imprimir = []
    for mano in ('mb','mm','dm'):
        if equipo[mano] != '' and equipo[mano]['grupo'] == 'armas':
            arma = equipo[mano]
        
            arm = arma['index']
            nombre = imprimir_nom_objmag(arma,s.OBJMAG,s.ARMAS).rstrip()
            bon_atk = ATKs[arm]
            categoria = ARMAS[arm]['Tipo']
            if categoria == 'ad':
                ataque = '/'.join('+'+str(i) for i in bon_atk)+' '+t('a distancia')
                if ARMAS[arm]['Subtipo'] == 'ar':
                    mod = FUE_mod
            else:
                ataque ='/'.join('+'+str(i) for i in bon_atk)+' '+t('c/c')
                if mano == 'dm':
                    mod = round(FUE_mod*1.5)
                elif mano == 'mm':
                    mod = round(FUE_mod*0.5)
                else:
                    mod = FUE_mod
                    
            if tam_pj['Nombre'] == 'Mediano':
                danio = ARMAS[arm]['Daño_M'] # podria ser Daño: {mediano:1d4, pequeño:1d3}
            else:                            # para usar directemte el nombre del tamaño
                danio = ARMAS[arm]['Daño_P'] # sin necesitar un elif
            
            if mod != '0':
                imprimir.append(nombre+' '+ataque+' ('+danio+'{0:+}'.format(mod)+')')
            else:
                imprimir.append(nombre+' '+ataque+' ('+danio+')')
        
        
    if imprimir == []:
        return ''
    else:
        return ', '.join(imprimir)+'.'

def imprimir_CA (tam,DES_mod,equipo,ARMDS,natural=0):
    '''Calcula e imprime la CA y sus componentes'''
    
    prnts = {0:{'nom': 'tam', 'val': tam['Mod']},
             1:{'nom': 'Des','val':DES_mod},
             4:{'nom':'nat','val':natural}}
    
    bon = 0
    if equipo['armd'] != '':
        armd = equipo['armd']
        
        if 'Bon_max_des' in armd:
            if DES_mod > ARMDS[armd['index']]['Bon_max_des']:
                DES_mod = ARMDS[armd['index']]['Bon_max_des']
                prnts[1]['val'] = DES_mod
        
        armd['Bon_CA'] = ARMDS[armd['index']]['Bon_CA']
    else:
        armd = {'index':None,'Bon_CA':0,'bon':0}
    
            
    if equipo['mm'] != '':
        if equipo['mm']['subgrupo'] == 'esc':
            esc = equipo['mm']
        
        if 'Bon_max_des' in esc:
            if DES_mod > ARMDS[esc['index']]['Bon_max_des']:
                DES_mod = ARMDS[esc['index']]['Bon_max_des']
                prnts[1]['val'] = DES_mod
        
        esc['Bon_CA'] = ARMDS[esc['index']]['Bon_CA']
    else:
        esc = {'index':None,'Bon_CA':0,'bon':0}
        
    for i in (armd, esc):
        if 'bon' in i:
            i['Bon_CA'] += i['bon']
        
    if armd['index'] != None: prnts[2] = {'nom':imprimir_nom_objmag(armd,s.OBJMAG,ARMDS).rstrip(),'val':armd['Bon_CA']}
    if esc['index'] != None: prnts[3] = {'nom':imprimir_nom_objmag(esc,s.OBJMAG,ARMDS).rstrip(),'val':esc['Bon_CA']}
    
    CA_normal = 10+tam['Mod']+DES_mod+natural+armd['Bon_CA']+esc['Bon_CA']
    CA_toque = 10+tam['Mod']+DES_mod
    CA_desprevenido = 10+tam['Mod']+natural+armd['Bon_CA']+esc['Bon_CA']
    
    parentesis = []
    for i in range(len(prnts)):
        if i in prnts:
            if prnts[i]['val'] != 0:
                parentesis.append('{:+}'.format(prnts[i]['val'])+' '+prnts[i]['nom'])
    
    p = '{!s}'.format(CA_normal)+' ('+', '.join(parentesis)+') '+t('toque')+' {!s}, '.format(CA_toque)+t('desprevenido')+' {!s}.'.format(CA_desprevenido)
    return p

def imprimir_CARS (Cars_Pj,Cars):
    imprimir = []
    for c in range(len(Cars)):
        imprimir.append(Cars[c]['Nom']+' '+str(Cars_Pj[Cars[c]['Abr']]['Punt']))
    
    return ', '.join(imprimir)+'.'

def imprimir_idiomas (idiomas):
    pass

def exportar_pj():
    if input('\n'+t('Desea Exportar este personaje? ')).lower().startswith('s'):
        try:
            Pj = open('Personajes/'+p.nombre+'.txt','w')
        except IOError:
            os.mkdir('Personajes/')
            Pj = open('Personajes/'+p.nombre+'.txt','w')
            
        Pj.write(t('Nombre')+': '+p.nombre+'\n')
        Pj.write(t('Clase y nivel')+': '+imprimir_clases(p.cla,s.CLASES)+' AL '+s.alins[p.alini]['Abr']+'\n')
        Pj.write(t('Tipo y Tamaño')+': '+t('Humanoide')+' '+p.tam['Nombre'])
        if p.subtipo != '':
            Pj.write(' ('+p.subtipo+')\n')
        Pj.write(t('DG')+': '+imprimir_DG(p.cla,s.CLASES,p.CARS['CON']['Mod'],p.stats['PG'],p.dotes)+'\n')
        Pj.write(t('Iniciativa')+': {0:+}'.format(p.stats['Init'])+'\n'+t('Velocidad')+': '+p.velocidad+'\n')
        Pj.write(t('CA')+': '+imprimir_CA(p.tam,p.CARS['DES']['Mod'],p.equipo,s.ARMDS)+'\n')
        Pj.write(t('Ataque base/Presa')+': {0:+}/{1:+}'.format(p.stats['AtqB'],p.stats['AtqB']+p.CARS['FUE']['Mod'])+'\n')
        atks = imprimir_ATK (p.equipo,p.ataques,s.ARMAS,p.tam,p.CARS['FUE']['Mod'])
        if atks != '':
            Pj.write(t('Ataque')+': '+atks+'\n')
        Pj.write(t('Ataque completo')+': '+''+'\n')
        Pj.write(t("E/A")+": 5'/5'.\n")
        if p.aprin['Ataques'] != []:
            Pj.write(t('Ataques especiales')+': '+', '.join(p.aprin['Ataques'])+'.\n')
        if p.aprin['Cualidades'] != []:
            Pj.write(t('Cualidades especiales')+': '+', '.join(p.aprin['Cualidades'])+'.\n')
        Pj.write('TS: '+
                 t('Fortaleza')+' {:+}, '.format(p.stats['TSFort'])+
                 t('Reflejos')+' {:+}, '.format(p.stats['TSRef'])+
                 t('Voluntad')+' {:+}.\n'.format(p.stats['TSVol']))
        Pj.write(t('Características')+': '+imprimir_CARS(p.CARS,s.Cars)+
                 '\n'+t('Habilidades y Dotes')+': '+orden_habs_imprint(p.habs,p.equipo,s.HABS,s.ARMDS)+
                 ' '+', '.join(ver_dotes(p.dotes,s.DOTES,s.ARMAS,s.HABS,s.ESCUELAS))+'.')
        sleep(3)
        print('\n'+t('Personaje Guardado'))
        Pj.close()
    sleep (2)

def autoguardar (datos):
    from time import localtime,strftime
    carpeta = 'Guardar/'
    ID = strftime("%d%m%Y%H%M%S", localtime())
    while True:
        if not os.path.exists(carpeta+str(ID)+'.json'):
            guardar_json(carpeta+str(ID)+'.json',datos)
            break
        else:
            ID = strftime("%d%m%Y%H%M%S", localtime())

