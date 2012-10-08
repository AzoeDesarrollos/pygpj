# coding=UTF-8
from func.gen.viz import subselector,barra
from func.core.lang import t
from func.data.setup import data as s
from func.core.prsnj import Pj as p
from func.core.intro import imprimir_titulo
from random import randint
import os

def riqueza (clase,CLASES,nivel):
    if nivel == 1:
        cant = CLASES[clase]['po'][0]
        mult = CLASES[clase]['po'][1]
        po = randint(cant,cant*4)*mult
    else:
        riqueza = [0, 900, 2700, 5400, 9000, 13000, 19000, 27000,
                   36000, 49000, 66000, 88000, 110000, 150000,
                   200000, 260000, 340000, 440000, 580000, 760000]
        po = riqueza[nivel-1]

    return po

def convertir_precio (precio):
    '''Tranforma precios de una nomenclatura a otra'''
    
    valores = [10,1,0.1,0.01]
    # ppt, po, pp, pc, en ese orden

    if type(precio) in (int,float): # decimales a monedas
        monedas = [0,0,0,0] 
        for i in range(len(valores)):
            valor = valores[i]
            while precio >= valor:
                precio = round(precio - valor ,2)
                monedas[i] += 1

        return monedas
    
    elif type(precio) == list:# monedas a decimales
        coste = 0
        for i in range(len(precio)):
            coste += precio[i]*valores[i]
        return coste

    else:
        raise TypeError ('El precio deber ser Int, Float o List')

def unificar_precio(valor,unidad='po',modo='B'):
    monedas = ['ppt','po','pp','pc']
    i = monedas.index(unidad)
    imprimir = []
    
    # calcula la unidad
    base = sum([valor[j]*(10**(i-j)) for j in range(i+1)])
    imprimir.append(str(base)+' '+unidad)
    
    # añade el resto
    total = base + sum([valor[i+1:][j] /(10**(j+1)) for j in range(len(valor[i+1:]))])
    for j in range(len(valor[i+1:])):
        if valor[i+1:][j] != 0:
            imprimir.append(str(valor[i+1:][j])+' '+monedas[i+1:][j])
    
    if modo == 'A':
        return total
    elif modo == 'B':
        return ' '.join(imprimir)
    else:
        raise ValueError('El modo debe ser A o B')

def calcular_precio (objeto,GRUPO,OBJMAG):
    index = objeto['index']
    
    precio = GRUPO[index]['Precio'] # 15
    if objeto['gc'] == True:
        if objeto['grupo'] == 'armas':
            precio += 300
        else:
            precio += 150

        if objeto['bon'] > 0:
            bon = objeto['bon']
            if len(objeto['apts']) > 0:
                for i in objeto['apts']:
                    if not OBJMAG[i]['Precio'].isnumeric():
                        bon += int(OBJMAG[i]['Precio'].split('+')[1])
                        precio += precio_base(objeto['grupo'],bon)
                    else:
                        precio += precio_base(objeto['grupo'],bon)
                        precio += int(OBJMAG[i]['Precio'])
            else:
                precio += precio_base(objeto['grupo'],bon)
    return precio

def precio_base(grupo,bonificador):
    if grupo == 'armas':
        mult = 2
    elif grupo == 'armds':
        mult = 1
    
    return ((bonificador**2)*1000)*mult

def objeto_magico (obj,subgrupo,GRUPO,OBJMAG):
    objeto = {}
    
    objeto['index'] = obj
    objeto['subgrupo'] = subgrupo
    if subgrupo in ('cc','ad'):
        objeto['grupo'] = 'armas'
    elif subgrupo in ('armd','esc'):
        objeto['grupo'] = 'armds'
    
    op1 = ['Gran Calidad','Mágico']
    
    while True:
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (barra(p.CARS,s.alinis[p.alini],p.raza['Nombre']))
        print (GRUPO[obj]['Nombre'])
        op = subselector('Tipo',op1)
        if op == 0:
            objeto['gc'] = True
            objeto['bon'] = 0
            objeto['apts'] = []
        elif op == 1:
            objeto['gc'] = True
            while True:
                bon = input ('\nBonificador de mejora: ')
                try: bon = int(bon)
                except ValueError:
                    print ('El bonificador de mejora debe ser numerico')
                finally:                    
                    bon = int(bon)
                    if bon > 5:
                        print ('No se puede tener un bonificador de mejora mayor a 5')
                    if bon < 1:
                        print ('El bonificador de mejora debe ser al menos de +1')
                    else:
                        objeto['bon'] = bon
                        break
            if input('\n¿Desea agregar aptitudes especiales a este objeto? ').lower().startswith('s'):
                os.system(['clear','cls'][os.name == 'nt'])
                objeto['apts'] = []
                op2,nom = [],[]
                for i in range(len(OBJMAG)):
                    nom.append(OBJMAG[i]['Nombre'])
                    if subgrupo in OBJMAG[i]['Subgrupo']:
                        op2.append(nom[i])
                    copia = op2 *1
                
                while bon < 10:
                    print ('\nEl bonificador de mejora actual es de +'+str(bon))
                    print ('\n'+GRUPO[obj]['Nombre']+' +'+str(objeto['bon'])+' '+
                           ' '.join(sorted([OBJMAG[i]['Nombre'] for i in objeto['apts'] if len(objeto['apts']) > 0])))
                    op = subselector('Aptitud',op2,True)
                    for i in range(len(nom)):
                        if op2[op] == nom[i]:
                            sel = i
                    if not OBJMAG[sel]['Precio'].isnumeric():
                        bon +=  int(OBJMAG[sel]['Precio'].split('+')[1])
                        del op2[op]
                    objeto['apts'].append(sel)
                    
                    if not input('Desea continuar? ').lower().startswith('s'):
                        break
            else:
                objeto['apts'] = []
            os.system(['clear','cls'][os.name == 'nt'])
        return objeto

def comprar(dinero,objetos,grupo):
    # crea una lista maestra con todos los índices de la lista OBJETOS
    _nom_ = [objetos[i]['Nombre'] for i in range(len(objetos))]
    
    # crea dos nuevas listas, filtrando los objetos que no tienen precio
    nom = [objetos[i]['Nombre'] for i in range(len(objetos)) if 'Precio' in objetos[i]]
    pre = [objetos[i]['Precio'] for i in range(len(objetos)) if 'Precio' in objetos[i]]
    
    compras = []
    while dinero > 0:
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (barra(p.CARS,s.alinis[p.alini],p.raza['Nombre']))
        print('\nTe quedan '+unificar_precio(convertir_precio(dinero))+' para gastar')
        op = subselector('Objeto',nom,True)
        if input('Deseas una versión mágica/de gran calidad de este objeto? ').lower().startswith('s'):
            if objetos[op]['Tipo'] in ('cc','ad'):
                obj = objeto_magico (op,objetos[op]['Tipo'],s.ARMAS,s.OBJMAG)
                precio = calcular_precio (obj,s.ARMAS,s.OBJMAG)
            elif objetos[op]['Tipo'] in ('armd','esc'):
                obj = objeto_magico (op,objetos[op]['Tipo'],s.ARMDS,s.OBJMAG)
                precio = calcular_precio (obj,s.ARMDS,s.OBJMAG)
            costo = unificar_precio(convertir_precio(precio))
        else:
            costo = unificar_precio(convertir_precio(pre[op]))
            precio = pre[op]
            obj = {'index':op,'subgrupo':objetos[op]['Tipo'],'gc':False,'bon':0,'apts':[]}
        
        print('Te quedan '+unificar_precio(convertir_precio(dinero))+' para gastar')
        
        print ('\n'+objetos[op]['Nombre'], end = '')
        if obj['bon'] > 0: print(' +'+str(obj['bon'])+' ',end = ' ')
        elif obj['gc'] == True: print(' GC',end ='')
        print(' '.join(sorted([s.OBJMAG[i]['Nombre'] for i in obj['apts'] if len(obj['apts']) > 0])))
        
        print ('\nEste objeto cuesta '+costo+'.')
        if precio > dinero:
            print('\nNecesitas más riqueza para poder pagarlo.')
        else:
            if input('\nEstas seguro de querer adquirirlo? ').lower().startswith('s'):
                compras.append(obj)
                dinero -= precio

        if not input('\n¿Deseas continuar comprando? ').lower().startswith('s'):
            return compras

def elegir_equipo (clase,compras):
    
    opciones = ['Comprar armas y munición',
                'Comprar armaduras y escudos',
                'Comprar equipo de aventura',
                'Ver las propiedades de un objeto, arma o armadura',
                'Ver los objetos poseídos',
                'Devolver objetos comprados']
    # 'compras' es un diccionario que incluye separadamente los índices de armas, armaduras y objetos
    dinero = riqueza(clase,s.CLASES,len(p.cla))
    while True:
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (barra(p.CARS,s.alinis[p.alini],p.raza['Nombre']))
        print ('\nTienes '+unificar_precio(convertir_precio(dinero))+ ' para gastar')
        op = subselector('Opción',opciones)
        if op == 0: # Comprar armas y munición
            nuevas = comprar(dinero,s.ARMAS,'armas')
            compras['Armas'] += nuevas
            subtotal = 0
            for i in nuevas:
                dinero -= calcular_precio(i,s.ARMAS,s.OBJMAG)
            if 'Nada más' not in opciones: opciones.append('Nada más')
        elif op == 1: # Comprar armaduras y escudos
            nuevas = comprar(dinero,s.ARMDS,'armds')
            compras['Armds'] += nuevas
            subtotal = 0
            for i in nuevas:
                dinero -= calcular_precio(i,s.ARMDS,s.OBJMAG)
            if 'Nada más' not in opciones: opciones.append('Nada más')
        elif op == 2: # Comprar objetos varios
            print ('Opción aún no disponible')
            pass # compras['Otros'] += comprar(dinero,Otros)
            #if 'Nada más' not in opciones: opciones.append('Nada más')
        elif op == 3: # Ver las estadísticas de un objeto, arma o armadura
            print ('Opción aún no disponible')
        elif op == 4: # Ver los objetos poseídos
            print ('Opción aún no disponible')
        elif op == 5: # Devolver objetos comprados
            print ('Opción aún no disponible')
        elif op == 6: # Nada más
            return compras,dinero