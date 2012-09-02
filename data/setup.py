# coding=UTF-8
import core.config as c
from core.lang import t

root = 'data/'+c.idioma+'/'
RAZAS = c.abrir_json(root+'razas.json')
CLASES = c.abrir_json(root+'clases.json')
IDIOMAS = c.abrir_json(root+'idiomas.json')
ESCUELAS = c.abrir_json(root+'escuelas.json')
CONJUROS = c.abrir_json(root+'conjuros.json')
HABS = c.abrir_json(root+'habs.json')
DOTES = c.abrir_json(root+'dotes.json')
ARMAS = c.abrir_json(root+'armas.json')
ARMDS = c.abrir_json(root+'armds.json')
APTS = c.abrir_json(root+'apts.json')

Cars = (t('Fuerza'),t('Destreza'),t('Constitución'),
    t('Inteligencia'),t('Sabiduría'),t('Carisma'))

alinieamientos = (t('Legal Bueno'),t('Neutral Bueno'),t('Caótico Bueno'),
              t('Legal Neutral'),t('Neutral Auténtico'),t('Caótico Neutral'),
              t('Legal Maligno'),t('Neutral Maligno'),t('Caótico Maligno'))

alinis = (t('LB'),t('NB'),t('CB'),
      t('LN'),t('NN'),t('CN'),
      t('LM'),t('NM'),t('CM'))

tam = {t('Minúsculo'):(+8,-16,+16),t('Diminuto'):(+4,-12,+12),t('Menudo'):(+2,-8,+8),
   t('Pequeño'):(+1,-4,+4),t('Mediano'):(+0,+0,+0),t('Grande'):(-1,+4,-4),
   t('Enorme'):(-2,+8,-8),t('Gargantuesco'):(-4,+12,-12),t('Colosal'):(-8,+16,-16)}