#config.py
import json
import os

def abrir_json (archivo):
    ex = open(archivo)
    data = json.load(ex)
    ex.close()
    return data

def guardar_json (archivo, datos):
    ex = open(archivo,'w')
    json.dump(datos,ex)
    ex.close()

def guardar_preferencias (nuevo):
    archivo = 'config.json'
    guardar_json(archivo,nuevo)

def preferencias (prefs):
    from func.gen.viz import subselector
    from func.core.lang import t,sel_idioma
    from func.data.setup import data as d
    from func.core.intro import imprimir_titulo
    
    while True:
        opciones = [t('Cambiar idioma'),t('Cambiar las advertencias'),
                    t('Cambiar el método de generación de características'),t('Salir')]
        imprimir_titulo()
        print (t('Menú: Preferencias'),t('Elije una opción'),sep = '\n\n')
        op = subselector(t('Opción'),opciones)
        if op == 0:
            global idioma
            idioma = sel_idioma()
            prefs['idioma'] = idioma
            aplicar_idioma(idioma)
            d.cambiar_idioma(idioma)
        elif op == 1:
            global advt
            advt = not advt
            prefs['advt'] = advt
        elif op == 2:
            global puntgen
            puntgen = menu_puntuacion()
            prefs['puntgen'] = puntgen
        elif op == 3:
            break
    
    guardar_preferencias (prefs)

def menu_puntuacion():
    from func.core.intro import imprimir_titulo
    from func.gen.viz import subselector
    
    opciones = ['Tiradas aleatorias','Compra de Puntos','Puntuaciones fijas','Salir']
    while True:
        imprimir_titulo()
        print('Seleccione un método de generación de características')
        print ('\n¿Que desea hacer?')
        op = subselector('Opción',opciones)
        if op == 0:
            ops = [('Tirada estándar','A2'),('Tirada variable con repetición','A4'),
                   ('Personaje orgánico','A3'),('Personaje promedio a medida','A1'),
                   ('Personaje promedio aleatorio','A0'),('Personaje muy poderoso','A5')]
            while True:
                imprimir_titulo()
                print ('Seleccione el método aleatorio que desee')
                op2 = ops[subselector('Opción',[i[0] for i in ops])][1]
                break
        elif op == 1:
            ops = [('Campaña estándar','B0'),('Campaña poco poderosa','B1'),
                   ('Campaña desafiante','B2'),('Campaña ardua','B3'),
                   ('Campaña muy poderosa','B4')]
            while True:
                imprimir_titulo()
                print ('Seleccione el tipo de compra de puntos')
                op2 = ops[subselector('Opción',[i[0] for i in ops])][1]
                break
        elif op == 2:
            ops = [('Puntuaciones de élite','C0'),
                   ('Punutaciones corrientes','C1'),
                   ('Puntuaciones estándar','C2')]
            while True:
                imprimir_titulo()
                print ('Seleccione el tipo de puntuación que desea')
                op2 = ops[subselector('Opción',[i[0] for i in ops])][1]
                break
        elif op == 3:
            break
    return op2

def aplicar_idioma(idioma):
    global textos
    try:
        textos = abrir_json('func/data/'+idioma+'/'+idioma+'.json')
    except IOError:
        textos = {}

def recargar_datos():
    global puntgen
    puntgen = CONFIG['puntgen']

try:
    CONFIG = abrir_json('config.json')
except IOError:
    CONFIG = {'idioma':'es',
              'advt':True,
              'puntgen':'A2'}
    guardar_preferencias(CONFIG)

idioma = CONFIG['idioma']
advt = CONFIG['advt']
puntgen = CONFIG['puntgen']
aplicar_idioma(idioma)

