# coding=UTF-8
# Viz.py
import os
from math import ceil
from core.lang import t

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

def subselector (prompt,lista,dos_col=False,vueltas=1):
    items = []
    pool = vueltas
    for vuelta in range(vueltas):
        if vuelta == 0:
            paginado = []
            for i in range(len(lista)):
                paginado.append(str(i)+': '+str(t(lista[i])))
            if dos_col == False:
                paginar (10,paginado)
            else:
                paginar_dos_columnas(10,paginado)
          
        while pool > 0:
            item = ''
            while item == '':
                item = input ('\n'+prompt+': ').capitalize()
                if item.isnumeric():
                    item = int(item)
                    if item in items:
                        print (t('Ya ha realizado esa selección, intente nuevamente'))
                        item = ''
                    elif item not in range(len(lista)):
                        print(t('La selección es incorrecta, intente nuevamente'))
                        item = ''
                    else:
                        items.append(item)
                        print (t('Ha elegido ')+lista[int(item)],end = '. ')
                        pool -= 1
                elif item not in lista:
                    print(t('La selección es incorrecta, intente nuevamente'))
                    item = ''
                elif lista.index(item) in items:
                    print (t('Ya ha realizado esa selección, intente nuevamente'))
                    item = ''
                else:
                    print (t('Ha elegido ')+item,end = '. ')
                    items.append(lista.index(item))
                    pool -= 1
            if not input(t('¿Estas seguro? ')).strip().lower().startswith(t('s')):
                pool += 1
                del items[-1]
    if vueltas == 1:
        return items[0]
    else:
        return items

def barra (caracteristicas, alineamiento, raza):
    '''Genera la barra superior de previsualización'''
    
    FUE = str(caracteristicas[0])
    DES = str(caracteristicas[1])
    CON = str(caracteristicas[2])
    INT = str(caracteristicas[3])
    SAB = str(caracteristicas[4])
    CAR = str(caracteristicas[5])
    
    barra = ' | '.join([raza,' '.join([t('FUE'),FUE,t('DES'),DES,t('CON'),CON,
                                         t('INT'),INT,t('SAB'),SAB,t('CAR'),CAR]),
                        'Al '+alineamiento])
    
    return barra

def paginar (tam_pag,lineas):
    '''Sencilla función para mostrar lineas de texto paginadas.'''
    
    for i in range(len(lineas)):
        print (lineas[i])
        if lineas[i] != lineas[-1]:
            if (i+1) % tam_pag == 0:
                input ('\n[Presione Enter para continuar]\n')
                #os.system(['clear','cls'][os.name == 'nt'])

def a_dos_columnas(items):
    '''Separa una lista de items en dos columnas para paginar en una sola página.'''
    
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

def paginar_dos_columnas(tam_pag,lista):
    pags = ceil((len(lista)/2)/tam_pag)
    c1 = [[] for i in range(pags)]
    c2 = [[] for i in range(pags)]

    j = 0
    for i in range(len(lista)):
        if i == tam_pag*2*(j+1):
            j += 1
        if i <  tam_pag+(tam_pag*2)*j:
            c1[j].append(lista[i])
        else:
            c2[j].append(lista[i])

    if  len(c1[-1]) > len(c2[-1]):
        for i in range(len(c1[-1])-len(c2[-1])):
            c2[-1].append('')

    lineas = []
    for i in range(pags):
        for j in range(len(c1[i])):
            if len(c1[i][j]) > 31:
                lineas.append(c1[i][j] +'\t'+ c2[i][j])
            elif len(c1[i][j]) > 23:
                lineas.append(c1[i][j] +'\t'*2+ c2[i][j])
            elif len(c1[i][j]) > 15:
                lineas.append(c1[i][j] +'\t'*3+ c2[i][j])
            elif len(c1[i][j]) > 7:
                lineas.append(c1[i][j] +'\t'*4+ c2[i][j])
            else:
                lineas.append(c1[i][j] +'\t'*5+ c2[i][j])

    for i in range(len(lineas)):
        print (lineas[i])
        if lineas[i] != lineas[-1]:
            if (i+1) % tam_pag == 0:
                input ('\n[Presione Enter para continuar]\n')
                #os.system(['clear','cls'][os.name == 'nt'])
