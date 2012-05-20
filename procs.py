# coding=UTF-8
import csv

def leerCSV (archivo):
    '''Lee archivos CSV y los devuelve como una lista.'''
    
    arch = csv.reader(open(archivo),dialect='myCSV')
    temp = []
    for t in arch:
        temp.append(t)
    if len(temp) == 1:
        temp = temp[0]
    return temp

def ProcRazas (razasCSV):
    razas = {}
    for R in razasCSV:
        razas[R[0]]=R[1:]
    
    for key in razas:
        razas[key][1] = razas[key][1].split(',')
        for i in range(len(razas[key][1])):
            razas[key][1][i] = int(razas[key][1][i])
        razas[key][4] = razas[key][4].split(',')
        for i in range(len(razas[key][4])):
            razas[key][4][i] = razas[key][4][i].split('b')
        for par in razas[key][4]:
            if par == ['']:
                pass
            else:
                for i in range(len(par)):
                    par[i]=int(par[i])
    
    return razas

def ProcHabCls (lista_de_clases):
    nom = lista_de_clases[0]
    hab = lista_de_clases[7]
    hab_cls = {}
    
    for i in range(len(nom)):
        hab_cls[nom[i]]=hab[i]

    for i in nom:
        hab_cls[i]=hab_cls[i].split(',')

    for i in range(len(nom)):
        for j in hab_cls[nom[i]]:
            hab_cls[nom[i]][hab_cls[nom[i]].index(j)] = int(hab_cls[nom[i]][hab_cls[nom[i]].index(j)])
    
    return hab_cls

def ProcApps (aptitudes):
    '''Procesa las Aptitudes Especiales en formato CSV'''
    
    AE = {}
    for A in aptitudes:
        AE[A[0]]=A[1:]

    for key in AE:
        for i in range(len(AE[key])):
            AE[key][i] = AE[key][i].split(',')

    return AE

def ProcDTcls (lista_de_clases):
    nom = lista_de_clases[0]
    dta = lista_de_clases[9]
    dt_cls = {}
    
    for i in range(len(nom)):
        dt_cls[nom[i]]=dta[i]
    
    for i in nom:
        dt_cls[i] = dt_cls[i].split(',')
    
    return dt_cls