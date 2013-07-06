# coding=UTF-8
import func.core.config as c
from func.core.lang import t

class data:
    RAZAS = []
    CLASES = []
    IDIOMAS = []
    ESCUELAS = []
    CONJUROS = []
    HABS = []
    DOTES = []
    ARMAS = []
    ARMDS = []
    APTS = []
    DOMINIOS = []
    OBJMAG = []
    CAMPNG = []
    
    Cars = {}
    alins = {}
    tam = {}
    
    
    def cambiar_idioma (idioma):
        root = 'func/data/'+idioma+'/'
        data.RAZAS = c.abrir_json(root+'razas.json')
        data.CLASES = c.abrir_json(root+'clases.json')
        data.IDIOMAS = c.abrir_json(root+'idiomas.json')
        data.ESCUELAS = c.abrir_json(root+'escuelas.json')
        data.CONJUROS = c.abrir_json(root+'conjuros.json')
        data.HABS = c.abrir_json(root+'habs.json')
        data.DOTES = c.abrir_json(root+'dotes.json')
        data.ARMAS = c.abrir_json(root+'armas.json')
        data.ARMDS = c.abrir_json(root+'armds.json')
        data.APTS = c.abrir_json(root+'apts.json')
        data.DOMINIOS = c.abrir_json (root+'dominios.json')
        data.OBJMAG = c.abrir_json(root+'objmag.json')
        data.CAMPNG = c.abrir_json('func/data/campaign.json')
    
        data.Cars = {0:{'Abr':t('FUE'),'Nom':t('Fuerza')},
                     1:{'Abr':t('DES'),'Nom':t('Destreza')},
                     2:{'Abr':t('CON'),'Nom':t('Constitución')},
                     3:{'Abr':t('INT'),'Nom':t('Inteligencia')},
                     4:{'Abr':t('SAB'),'Nom':t('Sabiduría')},
                     5:{'Abr':t('CAR'),'Nom':t('Carisma')}}

    
        data.alins = {0:{'Abr':t('LB'),'Nom':t('Legal Bueno')},
                      1:{'Abr':t('NB'),'Nom':t('Neutral Bueno')},
                      2:{'Abr':t('CB'),'Nom':t('Caótico Bueno')},
                      3:{'Abr':t('LN'),'Nom':t('Legal Neutral')},
                      4:{'Abr':t('NN'),'Nom':t('Neutral Auténtico')},
                      5:{'Abr':t('CN'),'Nom':t('Caótico Neutral')},
                      6:{'Abr':t('LM'),'Nom':t('Legal Maligno')},
                      7:{'Abr':t('NM'),'Nom':t('Neutral Maligno')},
                      8:{'Abr':t('CM'),'Nom':t('Caótico Maligno')}}
        
        data.tam = {0:{'Nom':t('Minúsculo'),   'Mod':+8,'Pre':-16,'Esc':+16},
                    1:{'Nom':t('Diminuto'),    'Mod':+4,'Pre':-12,'Esc':+12},
                    2:{'Nom':t('Menudo'),      'Mod':+2,'Pre':-8, 'Esc':+8},
                    3:{'Nom':t('Pequeño'),     'Mod':+1,'Pre':-4, 'Esc':+4},
                    4:{'Nom':t('Mediano'),     'Mod':+0,'Pre':+0, 'Esc':+0},
                    5:{'Nom':t('Grande'),      'Mod':-1,'Pre':+4, 'Esc':-4},
                    6:{'Nom':t('Enorme'),      'Mod':-2,'Pre':+8, 'Esc':-8},
                    7:{'Nom':t('Gargantuesco'),'Mod':-4,'Pre':+12,'Esc':-12},
                    8:{'Nom':t('Colosal'),     'Mod':-8,'Pre':+16,'Esc':-16}}

data.cambiar_idioma(c.idioma)