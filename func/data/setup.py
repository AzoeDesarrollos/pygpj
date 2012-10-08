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
    OBJMAG = []
    
    Cars = (t('Fuerza'),t('Destreza'),t('Constitución'),
    t('Inteligencia'),t('Sabiduría'),t('Carisma'))

    alinieamientos = (t('Legal Bueno'),t('Neutral Bueno'),t('Caótico Bueno'),
                      t('Legal Neutral'),t('Neutral Auténtico'),t('Caótico Neutral'),
                      t('Legal Maligno'),t('Neutral Maligno'),t('Caótico Maligno'))
    
    alinis = (t('LB'),t('NB'),t('CB'),t('LN'),t('NN'),t('CN'),t('LM'),t('NM'),t('CM'))
    
    tam = {t('Minúsculo'):(+8,-16,+16),t('Diminuto'):(+4,-12,+12),t('Menudo'):(+2,-8,+8),
           t('Pequeño'):(+1,-4,+4),t('Mediano'):(+0,+0,+0),t('Grande'):(-1,+4,-4),
           t('Enorme'):(-2,+8,-8),t('Gargantuesco'):(-4,+12,-12),t('Colosal'):(-8,+16,-16)}
    
    
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
        data.OBJMAG = c.abrir_json(root+'objmag.json')
    
        data.Cars = (t('Fuerza'),t('Destreza'),t('Constitución'),
        t('Inteligencia'),t('Sabiduría'),t('Carisma'))
    
        data.alinieamientos = (t('Legal Bueno'),t('Neutral Bueno'),t('Caótico Bueno'),
                          t('Legal Neutral'),t('Neutral Auténtico'),t('Caótico Neutral'),
                          t('Legal Maligno'),t('Neutral Maligno'),t('Caótico Maligno'))
        
        data.alinis = (t('LB'),t('NB'),t('CB'),t('LN'),t('NN'),t('CN'),t('LM'),t('NM'),t('CM'))
        
        data.tam = {t('Minúsculo'):(+8,-16,+16),t('Diminuto'):(+4,-12,+12),t('Menudo'):(+2,-8,+8),
               t('Pequeño'):(+1,-4,+4),t('Mediano'):(+0,+0,+0),t('Grande'):(-1,+4,-4),
               t('Enorme'):(-2,+8,-8),t('Gargantuesco'):(-4,+12,-12),t('Colosal'):(-8,+16,-16)}

data.cambiar_idioma(c.idioma)