# coding=UTF-8
import setup as s

Cars = ['Fuerza','Destreza','Constitución','Inteligencia','Sabiduría','Carisma']
CARS = [0,0,0,0,0,0]
CARS_mods = []

rng = [i*0 for i in range(len(s.HABS))] # Rangos de habilidad
dts = [i*0 for i in range(len(s.HABS))] # Bonificadores por dotes
rcl = [i*0 for i in range(len(s.HABS))] # Bonificadores raciales
sng = [i*0 for i in range(len(s.HABS))] # Bonificadores de sinergía
obj = [i*0 for i in range(len(s.HABS))] # Bonificadores por objetos

tam = {'Minúsculo':(+8,-16,+16),'Diminuto':(+4,-12,+12),'Menudo':(+2,-8,+8),'Pequeño':(+1,-4,+4),'Mediano':(+0,+0,+0),'Grande':(-1,+4,-4),'Enorme':(-2,+8,-8),'Gargantuesco':(-4,+12,-12),'Colosal':(-8,+16,-16)}

cla = [] ## [5, 5, 7]
clases = [] ## ['Gue', 'Gue', 'Mag']
lasclases = [] ## ['Guerrero', 'Guerrero', 'Mago']
dotes = []
dt_cl = False
stats = [0,0,0,0]
nivel = 0
# alinis = ('LB','NB','CB','LN','NN','CN','LM','NM','CM')
alini = ''
apps,aprin = [],[] ## apps mantiene indices, aprin mantiene texto
compW,compA = [],[]
idiomas = []
raciales = []
NL = {}

subtipo = ''
tam_nom = ''
tam_mod = ''
tam_pre = ''
tam_esc = ''