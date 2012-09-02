from core.lang import *
import core.config as c
from core.prsnj import Pj
import core.chargen
from gen.viz import subselector
import os

def cargar_archivo(prompt, carpeta):
    ars, arex = [], []
    for ar in os.listdir(carpeta):
        if os.path.isfile(carpeta+'/'+ar):
            ars.append(ar.split('.')[0])
            arex.append((ar.split('.')[1]))
    
    sel = subselector(prompt,ars,True)
    data = c.abrir_json(carpeta+'/'+ars[sel]+'.'+arex[sel])
    return data

def menu ():
    opciones = ['Crear un nuevo personaje',
                'Avanzar un personaje existente',
                'Editar preferencias',
                'Salir']

    while True:
        op = subselector(t('Opción'),opciones)
        if op == 0:
            Pj.nuevo_pj()
            core.chargen.go()
        elif op == 1:
            Pj.nuevo_pj()
            Pj.cargar_pj(cargar_archivo('Personaje','guardar/reciente'))
            core.chargen.go()
        elif op == 2:
            c.idioma = sel_idioma()
            c.guardar_preferencias ({'idioma':c.idioma})
        elif op == 3:
            break


if __name__ == '__main__':
    menu()

