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
    guadar_json(archivo,nuevo)

try:
    CONFIG = abrir_json('config.json')
except IOError:
    file = open('config.json','w')
    CONFIG = {'idioma':'es'}
    json.dump(CONFIG,file)
    file.close()

idioma = CONFIG['idioma']

try:
    textos = abrir_json('data/'+idioma+'/'+idioma+'.json')
except IOError:
    textos = {}