# coding=UTF-8
'''Estadísticas.py'''
from random import randint

def calcular_CA (tam,DES_mod,equipo,ARMDS,natural=0):
    '''Calcula los tres valores de CA'''
    bon = 0
    if equipo['armd'] != '':
        armd = equipo['armd']
        
        if 'Bon_max_des' in armd:
            if DES_mod > ARMDS[armd['index']]['Bon_max_des']:
                DES_mod = ARMDS[armd['index']]['Bon_max_des']
        
        armd['Bon_CA'] = ARMDS[armd['index']]['Bon_CA']
    else:
        armd = {'Bon_CA':0,'bon':0}
        
    if equipo['mm'] != '':
        if equipo['mm']['subgrupo'] == 'esc':
            esc = equipo['mm']
        
        if 'Bon_max_des' in esc:
            if DES_mod > ARMDS[esc['index']]['Bon_max_des']:
                DES_mod = ARMDS[esc['index']]['Bon_max_des']
        
        esc['Bon_CA'] = ARMDS[esc['index']]['Bon_CA']
    else:
        esc = {'Bon_CA':0,'bon':0}
     
    bon = 0
    for i in (armd, esc):
        if 'bon' in i:
            bon += i['bon']
    
    normal = 10+tam['mod_gen']+DES_mod+natural+armd['Bon_CA']+esc['Bon_CA']+bon
    toque = 10+tam['mod_gen']+DES_mod
    desprevenido = 10+tam['mod_gen']+natural+armd['Bon_CA']+esc['Bon_CA']+bon
    
    return normal,toque,desprevenido

def calcular_ATKs (ATKb,FUE_mod,DES_mod,tam,equipo,dotes,ARMAS):
    '''Cacula los mods de ataque para cada arma'''
    
    armas = []
    for mano in ('mb','mm'):
        if equipo[mano] != '':
            if equipo[mano]['subgrupo'] in ('cc','ad'):
                armas.append(equipo[mano])
            
    ataques = []
    if ATKb == 0:
        ataques.append(ATKb)
    else:
        while ATKb > 0:
            ataques.append(ATKb)
            ATKb -= 5
        
    ATK_C,ATK_D = [],[]
    for i in ataques:
        ATK_C.append(i+FUE_mod+tam['mod_gen'])
        ATK_D.append(i+DES_mod+tam['mod_gen'])

    ATKs = {}
    for arma in armas:
        arm = arma['index']
        bon = arma['bon']
        for i in dotes:
            if ':' in i:
                dt = i.split(':')[0]
                sb = i.split(':')[1]
                if sb == str(arm):
                    if dt == '83': # Soltura con un arma
                        bon += 1
                    elif dt == '85': # Soltura mayor con un arma
                        bon += 2
                
        ATKs[arm] = []
        if arma['subgrupo'] == 'ad':
            for i in ATK_D:
                ATKs[arm].append(i+bon)
        else:
            for i in ATK_C:
                ATKs[arm].append(i+bon)
    
    return ATKs

def calcular_PG (PG,CON_mod,DG,nivel,dotes):
    '''Calcula los Puntos de Golpe'''
    
    adic = (dotes.count('51'))*3
        
    if nivel == 1:
        PG += DG+CON_mod+adic
    else:
        PG += randint(1,DG)+CON_mod+adic

    return PG

def calcular_inic (DES_mod,dotes):
    '''Caclula el valor de iniciativa'''
    
    inic = DES_mod
    if '65' in dotes:
        inic += 4
    return inic