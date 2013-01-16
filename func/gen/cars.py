import os
from random import randint,shuffle,choice
from func.core.viz import subselector,paginar_dos_columnas
from func.core.lang import t,probar_input
from func.core.intro import imprimir_titulo
from func.data.setup import data as d
from func.core.prsnj import Pj as p

def UnaTir (dados,descarte=0):
    '''Un simple generador para una tirada.'''
    
    car = []
    for i in range(dados):
        car.append(randint(1,6))

    car.sort(reverse=True)
    
    for i in range(descarte):
        del car[-1]

    shuffle(car)
            
    return car

def retirar (tir):
    tir[-1] = randint(1,6)
    tir.sort(reverse=True)
    return tir

def generar_tiradas(metodo):
    ''''Genera las 6 tiradas segun el método elegido'''
    Tirs = []
    total = 0
    if metodo in (0,1):
        while total <= 0:
            for i in range(6):
                Tirs.append(sum(UnaTir(3)))
                total += CarMod(Tirs[i])
            if total >0:
                break
            else:
                total = 0
                Tirs = []
                
            
    elif metodo in (2,3):
        for i in range(6):
            Tirs.append(sum(UnaTir(4,1)))

    elif metodo == 4:
        tirs = []
        tirsp = []
        for i in range(6):
            t = UnaTir(4)
            tirs.append(t)
            tirsp.append(','.join([str(i) for i in t]))
            
        lineas = []
        for i in range(len(tirs)):
            lineas.append('el '+str(tirs[i][-1])+' de la '+str(i+1)+'º tirada ('+tirsp[i]+': '+str(sum(tirs[i][0:-1]))+')')

        print ('¿que valor desea retirar?')
        op = subselector('Opción',lineas,True)
        tirs[op] = retirar(tirs[op])

        for t in range(len(tirs)):
            del tirs[t][-1]
            Tirs.append(sum(tirs[t]))

    elif metodo == 5:
        for i in range(6):
            Tirs.append(sum(UnaTir(5,2)))

    Tirs.sort(reverse=True)
    return Tirs

def imprimir_puntos (puntos,modo):
    if modo == 'A':
        print ('Sus tiradas son: '+', '.join(str(i) for i in puntos)+'.')
    elif modo == 'C':
        print ('Sus puntuaciones son: '+', '.join(str(i) for i in puntos)+'.')
    
    return puntos

def repartir_a_voluntad(lista,Car):
    '''Ordena la distribución de valores de característica.'''
    
    CarVal = 0
    while CarVal == 0:
        entrada = input(Car+': ')
        if not entrada.isdigit():
            print(t('Por favor ingrese sólo números')+'\n')
        elif int(entrada) not in lista:
            print(t('No hay tiradas con ese valor')+'\n')
        else:
            CarVal = int(entrada)
            del lista[lista.index(int(entrada))]
    return CarVal

def repartir_puntuaciones(metodo,Cars,tirs):
    CARS = {}
    noms = {}
    for i in Cars:
        CARS[Cars[i]['Abr']] = 0
        noms[Cars[i]['Abr']] = Cars[i]['Nom']
        
    if metodo in (1,2,5): # repartir a voluntad
        print ('\nReparte tus puntuaciones de característica')
        #for Car in CARS:
        for i in Cars:
            Car = Cars[i]['Abr']
            CARS[Car] = repartir_a_voluntad(tirs,noms[Car])
    elif metodo in (0,3,4): # salen como salen
        for Car in CARS:
            t = choice(tirs)
            CARS[Car] = t
            del tirs[tirs.index(t)]
        print('Sus características quedan así:\n'+'\n'.
              join([Cars[i]['Nom']+': '+str(CARS[Cars[i]['Abr']]) for i in Cars]))
        
        if metodo == 3: # personajes orgánicos; vuelve a tirar una caracteristica, intercambia 2
            if input('\n¿Desea volver a tirar por una característica? ').lower().startswith('s'):
                Car = sel_car('\nElije qué caraceristica deseas volver a tirar\n\nCaracterísitica: ',Cars)
                CARS[Car] = sum(UnaTir(4,1))
            print('\nPuedes intercambiar las puntuaciones de dos características.')
            # toda esta seccion es bastante burda, y debe tener muchos bugs...
            if input('¿Quieres hacerlo? ').lower().startswith('s'):
                print ('\nElije cuales')
                prim = sel_car('Primera: ',Cars)
                sec = sel_car('Segunda: ',Cars)
                
                a = CARS[prim]
                b = CARS[sec]

                CARS[prim] = b
                CARS[sec] = a
            
    return CARS

def sel_car (prompt,Cars):
    '''Se asegura de que la selección de característica sea válida'''
    
    while True:
        car = input(prompt)
        for C in Cars:
            if car.title() == Cars[C]['Nom']:
                return Cars[C]['Abr']
        print ('Característica inválida')

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

def elegir_aumento_de_caracteristica (nivel,Cars):
    
    nom = [Cars[i]['Nom'] for i in range(len(Cars))]
    
    while True:
        imprimir_titulo()
        print ('\nEn el '+str(nivel)+'º nivel, tienes un aumento de características')
        print (t('Selecciona la característica que quieres aumentar'))
        car = subselector('Característica',nom)
        if car.isnumeric():
            Car = Cars[car]['Abr']
        else:
            car = probar_input(Car,nom)
            if car == '':
                print (t('La característica es inválida o inexistente'))
            else:
                car = nom.index(car)
                Car = Cars[car]['Abr']
   
    p.aumentar_caracteristicas(Car)
    print ('El personaje tiene ahora '+d.Cars[car]['Nom']+
           ' '+str(p.CARS[Car]['Punt'])+' (+'+str(p.CARS[Car]['M'])+')')

def compra_puntos (puntos,Cars):
    costes = {9:1,10:2,11:3,12:4,13:5,14:6,15:8,16:10,17:13,18:16}
    _puntos = puntos # copia de seguridad
    cars = ['']*6
    lista = []
    
    CARS = {}
    for i in Cars:
        CARS[Cars[i]['Abr']] = 0
        
    def header(h, previo = True):
        imprimir_titulo()
        print(t('Compra tus puntuaciones de característica'))
        print('\n'+texto(puntos,'Tienes','Tienes',' para gastar'))
        paginar_dos_columnas(5,lista)
        if previo == True:
            print('\n'+'\n'.join(cars[:h+1]),end = '')
    
    def texto (puntos, plural, singular, sufijo=''):
        if puntos > 1:
            texto = t(plural)+' '+str(puntos)+' '+t('puntos')+t(sufijo)
        elif puntos == 0:
            texto = t(plural)+' '+str(puntos)+' '+t('puntos')+t(sufijo)
        else:
            texto = t(singular)+' '+str(puntos)+' '+t('punto')+t(sufijo)
        
        return texto
    
    for i in range(9,19):
        lista.append(str(i)+': '+str(costes[i])+' '+t('puntos'))
    while True:
        for i in Cars:
            nom = Cars[i]['Nom']
            abr = Cars[i]['Abr']
            while puntos > 0:
                h = i
                header(h)
                entrada = input(nom+': ')
                
                if not entrada.isdigit():
                    print(t('Por favor ingrese sólo números')+'\n')
                    input(t('\n[Presione Enter para continuar]\n'))
                else:
                    entrada = int(entrada)
                    
                if entrada not in costes:
                    if entrada < 8:
                        print(t('El mínimo de característica es 8'))
                        input(t('\n[Presione Enter para continuar]\n'))
                    elif entrada > 18:
                        print(t('No se puede tener una puntuación de característica mayor a 18 antes de los')+
                              '\n'+t('ajustes raciales')+'\n')
                        input(t('\n[Presione Enter para continuar]\n'))
                    else:
                        CARS[abr] = entrada
                        cars[i] = nom+': '+str(CARS[abr])
                        break
                
                elif puntos - costes[entrada] < 0:
                    print ('\n'+t('No alcanzan los puntos para comprar esa puntuación')+' ('+texto(puntos,'quedan','queda')+')')
                    input(t('\n[Presione Enter para continuar]\n'))
                
                else:
                    puntos -= costes[entrada]
                    CARS[abr] = entrada
                    cars[i] = nom+': '+str(CARS[abr])
                    break
        
        header(h, previo = False)
        print()
        for i in Cars:
            print (Cars[i]['Nom']+': '+str(CARS[Cars[i]['Abr']]))
        
        if input ('\n'+t('¿Está seguro? ')).lower().startswith('s'):
            if puntos != 0:
                print(t('Debe gastar todos los puntos disponibles')+' ('+texto(puntos,'quedan','queda')+')')
                puntos = _puntos # restablecer copia
                cars = ['']*6
                for i in CARS: CARS[i] = 0
                    
                input(t('\n[Presione Enter para continuar]\n'))
            else:
                break
    
    return CARS

