import json

def abrir_json (archivo):
    ex = open(archivo)
    data = json.load(ex)
    ex.close()
    return data

RAZAS = abrir_json('data/razas.json')
CLASES = abrir_json('data/clases.json')
IDIOMAS = abrir_json('data/idiomas.json')
ESCUELAS = abrir_json('data/escuelas.json')
HABS = abrir_json('data/habs.json')
DOTES = abrir_json('data/dotes.json')
ARMAS = abrir_json('data/armas.json')
ARMDS = abrir_json('data/armds.json')
APTS = abrir_json('data/apts.json')

alinieamientos = ('Legal bueno','Neutral bueno','Caótico bueno',
                  'Legal neutral','Neutral auténtico','Caótico neutral',
                  'Legal maligno','Neutral maligno','Caótico maligno')
alinis = ('LB','NB','CB','LN','NN','CN','LM','NM','CM')

tam = {'Minúsculo':(+8,-16,+16),'Diminuto':(+4,-12,+12),'Menudo':(+2,-8,+8),
    'Pequeño':(+1,-4,+4),'Mediano':(+0,+0,+0),'Grande':(-1,+4,-4),
        'Enorme':(-2,+8,-8),'Gargantuesco':(-4,+12,-12),'Colosal':(-8,+16,-16)}