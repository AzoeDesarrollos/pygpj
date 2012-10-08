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
        opciones = [t('Cambiar idioma'),t('Cambiar las advertencias'),t('Salir')]
        os.system(['clear','cls'][os.name == 'nt'])
        imprimir_titulo()
        print (t('Menú: Preferencias'),t('Elije una opción'),sep = '\n\n', end='\n\n')
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
            break
    
    guardar_preferencias (prefs)

def aplicar_idioma(idioma):
    global textos
    try:
        textos = abrir_json('func/data/'+idioma+'/'+idioma+'.json')
    except IOError:
        textos = {}
    
try:
    CONFIG = abrir_json('config.json')
except IOError:
    CONFIG = {'idioma':'es',
              'advt':True}
    guardar_preferencias(CONFIG)

idioma = CONFIG['idioma']
advt = CONFIG['advt']
aplicar_idioma(idioma)

