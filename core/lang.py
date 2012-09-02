#lang.py
import os
import core.config as config

def t (string):
  if string in config.textos:
    string = config.textos[string]
  return string

def sel_idioma ():
    langs = []
    for i in os.listdir('data'):
        if os.path.exists('data/'+i+'/nombre.txt'):
            ar = open('data/'+i+'/nombre.txt','r')
            langs.append(ar.readline())
            ar.close()
    
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
    
    for i in os.listdir('data'):
        if os.path.exists('data/'+i+'/nombre.txt'):
            ar = open('data/'+i+'/nombre.txt','r')
            ex = ar.readline()
            ar.close()
            if ex == lang:
                LANG = i
    
    try:
        config.textos = config.abrir_json('data/'+LANG+'/'+LANG+'.json')
    except IOError:
        config.textos = {}
    
    return LANG