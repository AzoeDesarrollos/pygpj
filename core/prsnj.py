# coding=UTF-8

class Pj():
    CARS = []
    CARS_mods = []

    rng = [] # Rangos de habilidad
    dts = [] # Bonificadores por dotes
    rcl = [] # Bonificadores raciales
    sng = [] # Bonificadores de sinergía
    obj = [] # Bonificadores por objetos

    cla = [] ## ['Gue', 'Gue', 'Mag']
    clases = [] ## ['Guerrero', 'Guerrero', 'Mago']
    dotes = []
    e_dts = {'dt_cls': False, 'dt_rcl':False,'dt_nv':False}
    stats = []
    nivel, alini = 0, 0
    apps,aprin = [],[] ## apps mantiene indices, aprin mantiene texto
    compW,compA = [],[]
    idiomas = []
    raciales = []
    NL = {}
    conjuros = []
    PG = 0
    iniciativa = 0
    raza = {}
    velocidad = ''
    subtipo = ''
    tam = {}
    
    def nuevo_pj():
        from data.setup import HABS, CLASES, ARMAS, ARMDS, DOTES
        Pj.CARS = [0,0,0,0,0,0]
        Pj.CARS_mods = []

        t_habs = range(len(HABS))
        Pj.rng = [0 for i in t_habs] # Rangos de habilidad
        Pj.dts = [0 for i in t_habs] # Bonificadores por dotes
        Pj.rcl = [0 for i in t_habs] # Bonificadores raciales
        Pj.sng = [0 for i in t_habs] # Bonificadores de sinergía
        Pj.obj = [0 for i in t_habs] # Bonificadores por objetos

        Pj.cla = [] ## ['Gue', 'Gue', 'Mag']
        Pj.clases = [] ## ['Guerrero', 'Guerrero', 'Mago']
        Pj.dotes = []
        Pj.e_dts = {'dt_cls': False, 'dt_rcl':False,'dt_nv':False}
        Pj.stats = [0,0,0,0]
        Pj.nivel = 0
        Pj.alini = 0
        Pj.apps,Pj.aprin = [],[] ## apps mantiene indices, aprin mantiene texto
        Pj.compW,Pj.compA = [],[]
        Pj.idiomas = []
        Pj.raciales = []
        Pj.NL = {}
        Pj.conjuros = []
        Pj.PG = 0
        Pj.iniciativa = 0
        Pj.raza = {'Nombre':''}
        Pj.velocidad = ''
        Pj.subtipo = ''
        tam = {'Nombre':'','mod_gen':0,'mod_pre':0,'mod_esc':0}
    
    def cargar_pj (data):
        from data.setup import HABS, CLASES, ARMAS, ARMDS, DOTES
        from core.config import abrir_json, guardar_json
        from gen.iniciales import procesar_clase, Competencias
        from gen.cars import CarMod
        from gen.dotes import aplicar_dote
        
        Pj.raza = data['raza']
        Pj.cla = data['cla']
        Pj.nivel = len(Pj.cla)
        Pj.stats = [0,0,0,0]
        for clase in Pj.cla:
            Clase = CLASES[clase]
            Pj.stats =(procesar_clase(Clase,Pj.cla.count(clase),Pj.stats))
            Pj.clases.append(Clase['Nombre'])
        Pj.alini = data['alini']
        Pj.tam = data['tam']
        Pj.PG = data['pg']
        Pj.iniciativa = data['iniciativa']
        Pj.CARS = data['CARS']
        for i in range(len(Pj.CARS)):
            Pj.CARS_mods.append(CarMod(Pj.CARS[i]))
        Pj.rng = data['rng']
        Pj.sng = [i*0 for i in range(len(HABS))]
        for r in range(len(Pj.rng)):
            if Pj.rng[r] >= 5:
                if 'Sinergias' in HABS[r]:
                    for i in HABS[r]['Sinergias']:
                        Pj.sng[i]+=2
        Pj.dotes = data['dotes']
        Pj.apps = data['apps']
        for clase in Pj.cla:
            Pj.compW = Competencias (CLASES[clase]['Comp_Arma'],Pj.compW)
            Pj.compA = Competencias (CLASES[clase]['Comp_Armd'],Pj.compA)
        for dote in Pj.dotes:
            if ':' in dote:
                aplicar_dote (dote,DOTES,ARMAS,ARMDS)
        Pj.idiomas = data['idiomas']
    
    def guardar_pj ():
        guardar = {'raza':Pj.raza,
                   'cla':Pj.cla,
                   'alini':Pj.alini,
                   'tam':Pj.tam,
                   'pg':Pj.PG,
                   'iniciativa':Pj.iniciativa,
                   'CARS':Pj.CARS,
                   'rng':Pj.rng,
                   'dotes':Pj.dotes,
                   'apps':Pj.apps,
                   'idiomas':Pj.idiomas}
        
        return guardar

Pj.nuevo_pj()
