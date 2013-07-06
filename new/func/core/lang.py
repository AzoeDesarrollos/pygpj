#lang.py
import os
import func.core.config as config

def t (string):
  if string in config.textos:
    string = config.textos[string]
  return string

def sel_idioma ():
    carpeta = 'func/data/'
    langs = []
    for i in os.listdir(carpeta):
        if os.path.exists(carpeta+i+'/nombre.txt'):
            ar = config.abrir_json(carpeta+i+'/nombre.txt')
            langs.append(ar)
    
    for i in range(len(langs)):
        print (str(i)+': '+langs[i])
    lang = ''
    while lang == '':
        lang = input('\n>>> ')
        if lang.isnumeric():
                if int(lang) not in range(len(langs)):
                        lang = ''
                else:
                        lang = langs[int(lang)]
        elif lang not in langs:
                lang = ''
    
    for i in os.listdir(carpeta):
        if os.path.exists(carpeta+i+'/nombre.txt'):
            ex = config.abrir_json(carpeta+i+'/nombre.txt')
            if ex == lang:
                LANG = i
    
    config.aplicar_idioma(LANG)
    return LANG
  
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def probar_input (item,palabras):
    '''Compruba que el input sea válido, utilizando la distancia Levenshtein
    
    Esta función fue extraída de un documento en PHP, todos los comentarios
    se refeieren a aquel dcumento'''
    
    while True:
      # la distancia mas corta no ha sido encontrada, aún
      dist = -1
      
      # loopea por las palabras hasta encontrar la mas cercana
      for palabra in palabras:
          # calcula la distnacia entre la palabra buscada,
          # y la palabra actual
          lev = levenshtein(item, palabra)
      
          # comprobación de coincidencia exacta
          if lev == 0:
              # este es el item más cercano (coincidencia exacta)
              cercana = palabra
              dist = 0
      
              # salir del bucle, hemos encontrado una coincidencia exacta
              break
      
          # si esta distancia es menor que la siguiente distancia más corta
          # encontrada, O si una palabra más corta siguiente aún no
          # se ha encontrad
          if lev <= dist or dist < 0:
              # establecer la coincidencia más cercana y,
              # la distancia más corta
              cercana  = palabra
              dist = lev

      if dist == 0:
          return cercana
      elif dist <= -1 or dist > 3:
          return ''
      else:
          if input(t('¿Quizo decir')+': '+cercana+'? ').lower().startswith(t('s')):
            return cercana
          else:
            return ''