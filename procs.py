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

def ProcDTS (mecCSV):
    ID,tipo,r_cls = [],[],[]
    r_nv,r_dts,r_rng = [],[],[]
    r_app,r_stat,r_car, = [],[],[]
    
    for D in mecCSV:
        ID.append(D[0])
        tipo.append(D[1])
        r_cls.append(D[2])
        r_nv.append(D[3])
        r_dts.append(D[4])
        r_rng.append(D[5])
        r_app.append(D[6])
        r_stat.append(D[7])
        r_car.append(D[8])
    
    for i in range(len(ID)):
        ID[i] = int(ID[i])
    
    general = [ID,tipo,r_cls,r_nv,r_dts,r_rng,r_app,r_stat,r_car]
    
    return general

def ProcApps (aptitudes):
    '''Procesa las Aptitudes Especiales en formato CSV'''
    
    AE = {}
    for A in aptitudes:
        AE[A[0]]=A[1:]

    for key in AE:
        for i in range(len(AE[key])):
            AE[key][i] = AE[key][i].split(',')

    return AE