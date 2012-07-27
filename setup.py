import json

def abrir_json (archivo):
    ex = open(archivo)
    data = json.load(ex)
    ex.close()
    return data

RAZAS = abrir_json('data/razas.json')
CLASES = abrir_json('data/clases.json')
IDIOMAS = abrir_json('data/idiomas.json')
HABS = abrir_json('data/habs.json')
DOTES = abrir_json('data/dotes.json')
ARMAS = abrir_json('data/armas.json')
ARMDS = abrir_json('data/armds.json')
APTS = abrir_json('data/apts.json')