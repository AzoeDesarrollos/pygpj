import os
os.system(['clear','cls'][os.name == 'nt'])

def licencia (achivo_licencia):
    archivo = open(achivo_licencia)
    texto = archivo.read()
    archivo.close()
    return texto
    
print ('Bienvenido al Generador de Personajes para D&D 3.5',
       'by Zeniel Danaku y Einacio Spiegel',sep = '\n',end = '\n\n')