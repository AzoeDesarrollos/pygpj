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

cla = [] ## [5, 5, 7]
clases = [] ## ['Gue', 'Gue', 'Mag']
lasclases = [] ## ['Guerrero', 'Guerrero', 'Mago']
dotes = []
dt_cl = False
dt_rcl = False
stats = [0,0,0,0]
nivel = 0
alini = 0
apps,aprin = [],[] ## apps mantiene indices, aprin mantiene texto
compW,compA = [],[]
idiomas = []
raciales = []
NL = {}
PG = 0
print_PG = ''
iniciativa = 0
raza = {'Nombre':''}
velocidad = ''
subtipo = ''
tam_nom = ''
tam_mod = ''
tam_pre = ''
tam_esc = ''