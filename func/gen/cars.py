import os
from random import randint,shuffle
from func.gen.viz import subselector
from func.core.lang import t
from func.core.intro import imprimir_titulo

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
    print ('Sus tiradas son: '+', '.join(str(i) for i in Tirs)+'.')
    return Tirs

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
    CARS = []
    if metodo in (1,2,5): # repartir a voluntad
        print ('\nReparte tus puntuaciones de característica')
        for Car in Cars:
            CARS.append(repartir_a_voluntad(tirs,Car))
    elif metodo in (0,3,4): # salen como salen
        for i in tirs:
            CARS.append(i)
        print('Sus características quedan así:\n'+'\n'.join([Cars[i]+': '+str(CARS[i]) for i in range(len(Cars))]))
        if metodo == 3: # personajes orgánicos; vuelve a tirar una caracteristica, intercambia 2
            if input('\n¿Desea volver a tirar por una característica? ').lower().startswith('s'):
                CARS[Cars.index(input('Elije qué caraceristica deseas volver a tirar\nCaracterísitica: '))] = sum(UnaTir(4,1))
            print('\nPuedes intercambiar las puntuaciones de dos características.')
            # todo esta seccion es bastante burda, y debe tener muchos bugs...
            if input('¿Quieres hacerlo? ').lower().startswith('s'):
                print ('\nElije cuales')
                prim = input('Primera: ')
                sec = input ('Segunda: ')
                
                a = CARS[Cars.index(prim)]
                b = CARS[Cars.index(sec)]

                CARS[Cars.index(prim)] = b
                CARS[Cars.index(sec)] = a
            
    return CARS

def CarMod(car):
    '''Calcula el modificador de característica.'''
    
    if car % 2 == 0:
        mod = (car-10)/2
    else:
        mod = (car-11)/2
    return int(mod)

def aumenta_caract (nivel):
    CARS = (t('FUE'),t('DES'),t('CON'),t('INT'),t('SAB'),t('CAR'),t('Fuerza'),t('Destreza'),
            t('Constitución'),'Constitucion',t('Inteligencia'),t('Sabiduría'),'Sabiduria',
            t('Carisma'))

    print ('\nEn el '+str(nivel)+'º nivel, tienes un aumento de características')
    print ('Selecciona la característica que quieres aumentar')
    Car = input('Característica: ')
    while True:
        if Car.capitalize() not in CARS:
            if Car.upper() not in CARS:
                print ('La característica es inválida o inexistente')
                Car = input('Característica: ')
            else:
                break
        else:
            break
    if len(Car) > 3:
        Car = Car.capitalize()
        if Car in ('Fuerza'): Car = 0
        elif Car in ('Destreza'): Car = 1
        elif Car in ('Constitución','Constitucion'): Car = 2
        elif Car in ('Inteligencia'): Car = 3
        elif Car in ('Sabiduría','Sabiduria') : Car = 4
        elif Car in ('Carisma'): Car = 5
    else:
        Car = Car.upper()
        if Car == 'FUE': Car = 0
        elif Car == 'DES': Car = 1
        elif Car == 'CON': Car = 2
        elif Car == 'INT': Car = 3
        elif Car == 'SAB': Car = 4
        elif Car == 'CAR': Car = 5
    
    return Car
