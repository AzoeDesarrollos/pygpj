# coding=UTF-8
'''Módulo de visualización

Contiene funciones relativas a la visualización del programa'''

def barra (caracteristicas, alineamiento, raza):
    '''Genera la barra superior de previsualización'''
    
    FUE = str(caracteristicas[0])
    DES = str(caracteristicas[1])
    CON = str(caracteristicas[2])
    INT = str(caracteristicas[3])
    SAB = str(caracteristicas[4])
    CAR = str(caracteristicas[5])
    
    barra = ''.join([raza,'| FUE '+FUE,' DES '+DES,' CON '+CON,
                    ' INT '+INT,' SAB '+SAB,' CAR '+CAR,'| Al '+alineamiento])
    
    return barra

def HabcR (rang,HABS,inverso=False):
    if type(rang) == dict:
        rangos = []
        for i in range(len(HABS)):
            rangos[i] = rang[HABS[i]['Nombre']]
    else:
        rangos = rang
        
    cR = []
    nombres = [HABS[i]['Nombre'] for i in range(len(HABS))]
    if inverso == True:
        for i in range(len(rangos)):
            if rangos[i] == 0:
                cR.append(nombres[i])
    else:
        for i in range(len(rangos)):
            if rangos[i] > 0:
                cR.append(nombres[i]+' '+str(rangos[i]))

    return cR

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