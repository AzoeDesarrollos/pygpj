# coding=UTF-8
'''Estadísticas.py'''
from random import randint

def calcular_CA (tam,DES_mod,armds,ARMDS,natural=0):
    '''Calcula los tres valores de CA'''
    if len(armds) == 0:
        armd = {'Bon_CA':0}
        esc = {'Bon_CA':0}
    else:
        for i in range(len(armds)):
            if armds[i]['subgrupo'] == 'armd':
                armd = ARMDS[armds[i]['index']]
            if armds[i]['subgrupo'] == 'esc':
                esc = ARMDS[armds[i]['index']]
    
    if 'Bon_max_des' in (armd,esc):
        if DES_mod > armd['Bon_max_des']:
            DES_mod = armd['Bon_max_des']
        if 'Bon_max_des' in esc:
            if DES_mod > esc['Bon_max_des']:
                DES_mod = esc['Bon_max_des']
    
    bon = 0
    for i in range(len(armds)):
        bon += armds[i]['bon']
    
    normal = 10+tam['mod_gen']+DES_mod+natural+armd['Bon_CA']+esc['Bon_CA']+bon
    toque = 10+tam['mod_gen']+DES_mod
    desprevenido = 10+tam['mod_gen']+natural+armd['Bon_CA']+esc['Bon_CA']+bon
    
    return normal,toque,desprevenido

def calcular_ATKs (ATKb,FUE_mod,DES_mod,tam,armas,dotes,ARMAS):
    '''Cacula los mods de ataque para cada arma'''
    
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
        if ARMAS[arm]['Tipo'] == 'ad':
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