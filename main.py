import func.core.config as c
import func.core.chargen
import func.core.intro as intro
from func.core.lang import t
from func.gen.viz import subselector
from func.core.prsnj import Pj
from func.gen.export import imprimir_clases
import os

def cargar_archivo(prompt, carpeta):
    from func.data.setup import data as s
    ars, nom = [], []
    for ar in os.listdir(carpeta):
        if os.path.isfile(carpeta+'/'+ar):
            personaje = c.abrir_json(carpeta+'/'+ar)
            nom.append(personaje['nombre']+' ('+imprimir_clases(personaje['cla'],s.CLASES)+')')
            ars.append(ar)
              
    sel = subselector(prompt,nom,True)
    data = c.abrir_json(carpeta+'/'+ars[sel])
    return data

def menu ():
    while True:
        opciones = [t('Crear un nuevo personaje'),
                    t('Avanzar un personaje existente'),
                    t('Editar preferencias'),
                    t('Salir'),
                    '\n'+t('Ver licencia')]
         
        os.system(['clear','cls'][os.name == 'nt'])
        intro.imprimir_titulo()
        intro.introduccion()
        print(t('Elije una opción'))
        op = subselector(t('Opción'),opciones)
        if op == 0: # Crear un nuevo Pj
            Pj.nuevo_pj()
            func.core.chargen.go()
        elif op == 1: # Avanzar un Pj existente
            Pj.cargar_pj(cargar_archivo('Personaje','Guardar'))
            func.core.chargen.go()            
        elif op == 2: # preferencias
            c.preferencias(c.abrir_json('config.json'))
        elif op == 3: # exit
            break
        elif op == 4:
            intro.licencia('LICENSE.txt')
        
        input(t('\n[Presione Enter para continuar]\n'))


if __name__ == '__main__':
    os.system(['clear','cls'][os.name == 'nt'])
    menu()

