import os
from func.core.lang import t

def licencia (achivo_licencia):
    archivo = open(achivo_licencia)
    texto = archivo.read()
    archivo.close()
    imprimir_titulo()
    print (texto)

def introduccion ():
    print (t('Bienvenido a PyGPJ, un generador de personajes para D&D 3.5'),
       '\n'+'by Zeniel Danaku & Einacio Spiegel'.rjust(79),sep = '\n',end = '\n\n')

def imprimir_titulo ():
    os.system(['clear','cls'][os.name == 'nt'])
    print ('====== PyGPJ ======'.center(79)+'\n')