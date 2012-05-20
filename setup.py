# coding=UTF-8
import csv
import procs as p
csv.register_dialect('myCSV',delimiter=';')

RAZAS = p.ProcRazas(p.leerCSV('data/razas.csv'))
DOTES = p.leerCSV('data/dotes.csv')
HABS = p.leerCSV('data/habs.csv')
CLASES = p.leerCSV('data/clases.csv')
hab_cls = p.ProcHabCls(CLASES)
dt_cls = p.ProcDTcls (CLASES)
APPS = p.ProcApps(p.leerCSV('data/apps.csv'))
APs_mc = p.leerCSV('data/app_mc.csv')
ARMAS = p.leerCSV('data/armas.csv')
ARMDS = p.leerCSV('data/armd.csv')

Cars = ['Fuerza','Destreza','Constitución','Inteligencia','Sabiduría','Carisma']
CARS = [0,0,0,0,0,0]

rng = [i*0 for i in range(len(HABS[0]))] # Rangos de habilidad
dts = [i*0 for i in range(len(HABS[0]))] # Bonificadores por dotes
rcl = [i*0 for i in range(len(HABS[0]))] # Bonificadores raciales
sng = [i*0 for i in range(len(HABS[0]))] # Bonificadores de sinergía
obj = [i*0 for i in range(len(HABS[0]))] # Bonificadores por objetos

hab_s_E = [0,6,7,17,20,21,25,26,28,29,30,31,32,33,34,35,40,42,44]

tamaño = {'Minúsculo':(+8,-16,+16),'Diminuto':(+4,-12,+12),'Menudo':(+2,-8,+8),'Pequeño':(+1,-4,+4),'Mediano':(+0,+0,+0),'Grande':(-1,+4,-4),'Enorme':(-2,+8,-8),'Gargantuesco':(-4,+12,-12),'Colosal':(-8,+16,-16)}

cla = [] ## ['Gue', '', 'Mag']
lasclases = [] ## ['Guerrero', 'Guerrero', 'Mago']
dotes = []
stats = [0,0,0,0]
nivel = 0
# alinis = ('LB','NB','CB','LN','NN','CN','LM','NM','CM')
alini = ''
nuevas,apps,aprin = [],[],[]
compW,compA = [],[]