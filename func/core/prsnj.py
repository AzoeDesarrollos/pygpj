# coding=UTF-8

class Pj():
    '''Clase base para todos los Objetos-Personaje.'''
    nombre = ''
    CARS = [0,0,0,0,0,0]
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
    stats = [0,0,0,0]
    ataques = []
    nivel = 0
    alini = 0
    apps = []
    aprin = {'Ataques':[],'Cualidades':[]}
    compW = []
    compA = []
    idiomas = []
    raciales = []
    NL = {}
    conjuros = []
    PG = 0
    iniciativa = 0
    raza = {'Nombre':''}
    velocidad = ''
    subtipo = ''
    tam = {'Nombre':'','mod_gen':0,'mod_pre':0,'mod_esc':0}
    equipo = {'Armas':[],'Armds':[],'Otros':[]}
    armas = []
    armd = []
    esc = []
    CA = 0
    dinero = 0
        
    def nuevo_pj():
        from func.data.setup import data as d
        Pj.nombre = ''
        Pj.CARS = [0,0,0,0,0,0]
        Pj.CARS_mods = []

        t_habs = range(len(d.HABS))
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
        Pj.ataques = []
        Pj.nivel = 0
        Pj.alini = 0
        Pj.apps = []
        Pj.aprin = {'Ataques':[],'Cualidades':[]}
        Pj.compW = []
        Pj.compA = []
        Pj.idiomas = []
        Pj.raciales = []
        Pj.NL = {}
        Pj.conjuros = []
        Pj.PG = 0
        Pj.iniciativa = 0
        Pj.raza = {'Nombre':''}
        Pj.velocidad = ''
        Pj.subtipo = ''
        Pj.tam = {'Nombre':'','mod_gen':0,'mod_pre':0,'mod_esc':0}
        Pj.armas = []
        Pj.armd = {}
        Pj.esc = {}
        Pj.CA = 0
        Pj.dinero = 0
        Pj.equipo = {'Armas':[],'Armds':[],'Otros':[]}
        
    def cargar_pj (data):
        from func.data.setup import data as d
        from func.gen.iniciales import procesar_clase, Competencias
        from func.gen.cars import CarMod
        from func.gen.dotes import aplicar_dote
        from func.gen.estats import calcular_ATKs,calcular_CA
        from func.gen.export import aplicar_mods
        
        Pj.nombre = data['nombre']
        Pj.raza = data['raza']
        Pj.cla = data['cla']
        Pj.nivel = len(Pj.cla)
        Pj.stats = [0,0,0,0]
        for clase in Pj.cla:
            Clase = d.CLASES[clase]
            Pj.stats =(procesar_clase(Clase,Pj.cla.count(clase),Pj.stats))
            Pj.clases.append(Clase['Nombre'])
        Pj.alini = data['alini']
        Pj.tam = data['tam']
        Pj.PG = data['PG']
        Pj.iniciativa = data['iniciativa']
        Pj.CARS = data['CARS']
        for i in range(len(Pj.CARS)):
            Pj.CARS_mods.append(CarMod(Pj.CARS[i]))
        Pj.rng = data['rng']
        Pj.dts = [i*0 for i in range(len(d.HABS))]
        Pj.sng = [i*0 for i in range(len(d.HABS))]
        if 'Hab_rcl' in Pj.raza:
            Pj.raciales = Pj.raza['Hab_rcl']
        Pj.dotes = data['dotes']
        aplicar_mods(d.DOTES, d.HABS, Pj.raciales, Pj.dotes, Pj.rng)
        Pj.apps = data['apps']
        for clase in Pj.cla:
            Pj.compW = Competencias (d.CLASES[clase]['Comp_Arma'],Pj.compW)
            Pj.compA = Competencias (d.CLASES[clase]['Comp_Armd'],Pj.compA)
        for dote in Pj.dotes:
            if ':' in dote:
                aplicar_dote (dote,d.DOTES,d.ARMAS,d.ARMDS)
        Pj.idiomas = data['idiomas']
        Pj.ataques = calcular_ATKs (Pj.stats[0],Pj.CARS_mods[0],Pj.CARS_mods[1],
                                      Pj.tam,Pj.armas,Pj.dotes,d.ARMAS)
        Pj.CA = calcular_CA (Pj.tam,Pj.CARS_mods[1],Pj.armd,Pj.esc)
        Pj.dinero = data['dinero']
    
    def guardar_pj ():
        guardar = {'nombre':Pj.nombre,
                   'raza':Pj.raza,
                   'cla':Pj.cla,
                   'alini':Pj.alini,
                   'tam':Pj.tam,
                   'PG':Pj.PG,
                   'iniciativa':Pj.iniciativa,
                   'CARS':Pj.CARS,
                   'rng':Pj.rng,
                   'dotes':Pj.dotes,
                   'apps':Pj.apps,
                   'idiomas':Pj.idiomas,
                   'armas':Pj.armas,
                   'dinero':Pj.dinero}
        
        return guardar
    
