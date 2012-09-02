# coding=UTF-8
import os
from random import randint
from time import sleep
from gen.viz import PrepPrint
from core.lang import t

def UnaCar ():
    '''Un simple generador para una caracterítica.'''
    
    car = [randint(1,6),randint(1,6),randint(1,6),randint(1,6)]
    car.sort(reverse=True)
    del car[-1]
    Car = sum(car)
    return Car

def generar_tiradas():
    ''''Genera las 7 tiradas y descarta la más baja.'''
    
    A,B,C = UnaCar(),UnaCar(),UnaCar()
    D,E,F = UnaCar(),UnaCar(),UnaCar()
    G = UnaCar()
    TirList = [A,B,C,D,E,F,G]
    TirList.sort(reverse=True)
    del TirList[-1]
    return TirList

def elegir_tiradas (tirs):
    print(t('Sus tiradas son')+': '+PrepPrint(tirs))
    sleep (2)
    if input (t('¿Desea tirar de nuevo? ')).lower().startswith('s'):
        os.system(['clear','cls'][os.name == 'nt'])
        return False
    else:
        return True

def repartir_puntuaciones(lista,Car):
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