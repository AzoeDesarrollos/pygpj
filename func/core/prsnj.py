# coding=UTF-8
from func.data.setup import data as d

class Pj():
    '''Clase base para todos los Objetos-Personaje.'''
    nombre = ''
    CARS = {}
    habs = {}
    cla = []
    clases = []
    dotes = []
    e_dts = {}
    stats = {}
    ataques = []
    nivel = 0
    alini = 0
    apts = {}
    aprin = {}
    comps = {}
    idiomas = []
    NL = {}
    conjuros = []
    raza = {}
    velocidad = ''
    subtipo = ''
    tam = {}
    equipo = {}
    armas = []
    armd = []
    esc = []
    CA = 0
    dinero = 0
        
    def nuevo_pj():
        Pj.nombre = ''
        Pj.CARS = {'FUE':{'Punt':0,'Mod':0},'DES':{'Punt':0,'Mod':0},
                   'CON':{'Punt':0,'Mod':0},'INT':{'Punt':0,'Mod':0},
                   'SAB':{'Punt':0,'Mod':0},'CAR':{'Punt':0,'Mod':0}}
        
        for h in range(len(d.HABS)):
            Pj.habs[str(h)] = {'rng':0,'dts':0,'rcl':0,'sng':0,'obj':0}

        Pj.cla = [] ## ['Gue', 'Gue', 'Mag']
        Pj.clases = [] ## ['Guerrero', 'Guerrero', 'Mago']
        Pj.dotes = []
        Pj.e_dts = {'dt_cls': False, 'dt_rcl':False,'dt_nv':False}
        Pj.stats = {'AtqB':0,'TSFort':0,'TSRef':0,'TSVol':0,'Init':0,'PG':0,
                    'CA':{'Normal':0,'Toque':0,'Desprevenido':0}} # esta nueva forma
                                                                  # lo cambia todo.
        Pj.ataques = []
        Pj.nivel = 0
        Pj.alini = 0
        Pj.apts = {}
        Pj.aprin = {'Ataques':[],'Cualidades':[]}
        Pj.comps = {'Armas':[],'Armds':[]}
        Pj.idiomas = []
        Pj.NL = {}
        Pj.conjuros = []
        Pj.raza = {}
        Pj.velocidad = ''
        Pj.subtipo = ''
        Pj.tam = {'Ind':0,'Nombre':'','Mod':0,'Pre':0,'Esc':0}
        Pj.armas = []
        Pj.armd = {}
        Pj.esc = {}
        Pj.dinero = 0
        Pj.equipo = {'mb':'','mm':'','dm':'','armd':''}
        Pj.inventario = {'Armas':[],'Armd':[],'Esc':[]}
        
    def cargar_pj (data):
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
            Pj.aplicar_clase (clase)
        Pj.alini = data['alini']
        Pj.tam = data['tam']

        Pj.iniciativa = data['iniciativa']
        Pj.CARS = data['CARS']
        #for i in range(len(Pj.CARS)):
        #    Pj.CARS_mods.append(CarMod(Pj.CARS[i]))
        Pj.rng = data['rng']
        Pj.dts = [i*0 for i in range(len(d.HABS))]
        Pj.sng = [i*0 for i in range(len(d.HABS))]
        if 'Hab_rcl' in Pj.raza:
            Pj.raciales = Pj.raza['Hab_rcl']
        Pj.dotes = data['dotes']
        aplicar_mods(d.DOTES, d.HABS, Pj.raciales, Pj.dotes, Pj.rng)
        Pj.apts = data['apts']
        for clase in Pj.cla:
            Pj.compW = Competencias (d.CLASES[clase]['Comp_Arma'],Pj.compW)
            Pj.compA = Competencias (d.CLASES[clase]['Comp_Armd'],Pj.compA)
        for dote in Pj.dotes:
            Pj.aplicar_dote(dote,d.DOTES,d.ARMAS,d.ARMDS)
        Pj.idiomas = data['idiomas']
        Pj.equipo = data['equipo']
        Pj.ataques = calcular_ATKs (Pj.stats[0],Pj.CARS['FUE']['Mod'],Pj.CARS['DES']['Mod'],
                                      Pj.tam,Pj.armas,Pj.dotes,d.ARMAS)
        Pj.CA = calcular_CA (Pj.tam,Pj.CARS['INT']['DES'],Pj.armd,Pj.esc)
        Pj.dinero = data['dinero']
    
    def guardar_pj ():
        guardar = {'nombre':Pj.nombre,
                   'raza':Pj.raza,
                   'cla':Pj.cla,
                   'alini':Pj.alini,
                   'tam':Pj.tam,
                   'PG':Pj.stats['PG'],
                   'iniciativa':Pj.stats['Init'],
                   'CARS':Pj.CARS,
                   'habs':sorted([Pj.habs[hab]['rng'] for hab in Pj.habs]),
                   'dotes':Pj.dotes,
                   'apts':Pj.apts,
                   'idiomas':Pj.idiomas,
                   'armas':Pj.armas,
                   'dinero':Pj.dinero,
                   'equipo':Pj.equipo}
        
        return guardar
    
    def asignar_carcteristicas (campaing,tirs=None):
        from func.core.config import puntgen
        from func.gen.cars import repartir_puntuaciones,compra_puntos
    
        tipo = puntgen[0]
        sub = puntgen[1:]
    
        if tipo == 'A':
            CARS = repartir_puntuaciones(campaing[tipo][sub], d.Cars, tirs)
        elif tipo == 'B':
            CARS = compra_puntos(campaing[tipo][sub],d.Cars)
        elif tipo == 'C':
            CARS = repartir_puntuaciones(1,d.Cars,tirs)
        
        for Car in CARS:
            Pj.CARS[Car]['Punt'] = CARS[Car]
    
    def aplicar_raza (raza):
        from func.gen.cars import CarMod
                
        Pj.raza = d.RAZAS[raza]
        Pj.subtipo = d.RAZAS[raza]['Subtipo']
        Pj.velocidad = d.RAZAS[raza]['Velocidad']
        
        Pj.tam['Ind'] = [i for i in d.tam if d.RAZAS[raza]['Tamaño'] == d.tam[i]['Nom']][0]
        Pj.tam['Nombre'] = d.RAZAS[raza]['Tamaño']
        Pj.tam['Mod'] = d.tam[Pj.tam['Ind']]['Mod']
        Pj.tam['Pre'] = d.tam[Pj.tam['Ind']]['Pre']
        Pj.tam['Esc'] = d.tam[Pj.tam['Ind']]['Esc']
        
        if 'Hab_rcl' in d.RAZAS[raza]:
            for hab in d.RAZAS[raza]['Hab_rcl']:
                Pj.habs[hab]['rcl'] = d.RAZAS[raza]['Hab_rcl'][hab]
        
        if 'Dt_rcl' in d.RAZAS[raza]:
            Pj.e_dts['dt_rcl'] = d.RAZAS[raza]['Dt_rcl']
        
        if 'Ajustes' in  d.RAZAS[raza]:
            for Car in d.RAZAS[raza]['Ajustes']:
                Pj.CARS[Car]['Punt'] += d.RAZAS[raza]['Ajustes'][Car]
            
        for Car in Pj.CARS:
            Pj.CARS[Car]['Mod'] = CarMod(Pj.CARS[Car]['Punt'])
    
    def aplicar_clase (clase):
        from func.gen.apts import calcular_NL
        from func.gen.estats import calcular_PG
        from func.gen.iniciales import Competencias,procesar_clase
        
        Pj.comps['Armas'] = Competencias (d.CLASES[clase]['Comp_Arma'],Pj.comps['Armas'])
        Pj.comps['Armds'] = Competencias (d.CLASES[clase]['Comp_Armd'],Pj.comps['Armds'])
        Pj.cla.append(clase)
        Pj.clases.append(d.CLASES[clase]['Nombre'])
        Pj.NL = calcular_NL(clase,Pj.cla,d.CLASES)
        for i in range(len(Pj.cla)):
            if Pj.cla[i] == '':
                Pj.cla[i] = Pj.cla[i-1]
                
        nuevostats = procesar_clase(d.CLASES[clase],Pj.cla.count(clase),Pj.stats)
        Pj.stats['AtqB'] = nuevostats[0]
        Pj.stats['TSFort'] = nuevostats[1]+Pj.CARS['CON']['Mod'] # TS Fortaleza
        Pj.stats['TSRef'] = nuevostats[2]+Pj.CARS['DES']['Mod'] # TS Reflejos
        Pj.stats['TSVol'] = nuevostats[3]+Pj.CARS['SAB']['Mod'] # TS Voluntad
    
    def actualizar_habilidades(hab_rng):
        for hab in range(len(hab_rng)):
            Pj.habs[str(hab)]['rng'] =+ hab_rng[hab]
    
    def calcular_sinergias (HABS):
        for hab in Pj.habs:
            if Pj.habs[hab]['rng'] >= 5:
                if 'Sinergias' in HABS[hab]:
                    for i in HABS[hab]['Sinergias']:
                        Pj.habs[str(i)]['sng'] += 2
    
    def aumentar_caracteristicas (Car):
        from func.gen.cars import CarMod
        Pj.CARS[Car]['Punt']+=1
        Pj.CARS[Car]['Mod'] = CarMod(Pj.CARS[Car]['Punt'])
    
    def agregar_dote (dote,lista):
        Pj.dotes.append(dote)
        Pj.aplicar_dote (dote, d.DOTES,d.ARMAS,d.ARMDS)
        Pj.e_dts[lista] = False
    
    def aplicar_dote (nueva_dote,DOTES,ARMAS,ARMDS):
        if ':' in nueva_dote:
            dt = nueva_dote.split(':')[0]
            sb = int(nueva_dote.split(':')[1])
            if 'Competencia' in DOTES[dt]:
                if 'Marcial' or 'Exótica' in DOTES[dt]['Competencia']:
                    if sb not in Pj.comps['Armas']:
                        Pj.comps['Armas'].append(sb)
                elif 'Sencillas' in DOTES[dt]['Competencia']:
                    for i in range(len(ARMAS)):
                        if ARMAS[i]['Competencia'] == dt:
                            if i not in Pj.comps['Armas']:
                                Pj.comps['Armas'].append(i)
                Pj.comps['Armas'].sort()
            elif 'Critico' in DOTES[dt]:
                pass
            elif 'Hab_dt' in DOTES[dt]:
                Pj.habs[str(sb)]['dts'] += 3
        elif nueva_dote.isnumeric():
            dt = nueva_dote
            if 'Stat' in DOTES[dt]:
                st = DOTES[dt]['Stat'].split(':')[0]
                sb = int(DOTES[dt]['Stat'].split(':')[1])
                Pj.stats [st] += sb
            elif 'Hab_dt' in DOTES[dt]:
                for i in DOTES[dt]['Hab_dt']:
                    Pj.habs[str(i)]['dts']+=2
            elif 'Competencia' in DOTES[dt]: #competencia con armadura y escudo
                for i in range(len(ARMDS)):
                    if ARMDS[i]['Competencia'] == dt:
                        if i not in Pj.compA:
                            Pj.compA.append(i)
                Pj.compA.sort()
    
    def agregar_ap (apt,args,cmd):
        '''Ordena la asignación de aptitudes especiales'''
        if cmd == 'a': ##OK
            Pj.apts[apt] = args
        elif cmd == 'c': ##OK
            if apt not in Pj.apts:
                Pj.apts[apt] = args
            else:
                Pj.apts[apt]['cant'] +=1
        elif 'r' in cmd: ##OK
            r = cmd.strip('r')
            del Pj.apts[r]
            Pj.apts[apt] = args
        elif cmd == 'd': ##OK
            Pj.dotes.append(apt)
        elif cmd == 't': ##OK
            Pj.e_dts['dt_cls'] = True # toggle p.e_dts['dt_cls']
        elif cmd == 's':
            Pj.apts[apt] = args #append
            # faltan los poderes concedidos.
            # y los conjuros de dominio...
    
    def actualizar_inventario (compras):
        Pj.inventario = compras
        
    def equipar_pj ():
        from func.gen.objetos import equiparse
        Pj.equipo = equiparse(Pj.inventario,Pj.equipo)
    
    def calcular_estadisticas_de_combate(clase):
        import func.gen.estats as T
        Pj.stats['PG'] = T.calcular_PG(Pj.stats['PG'],Pj.CARS['CON']['Punt'],
                                       d.CLASES[clase]['DG'],Pj.nivel,Pj.dotes,d.DOTES) # puntos de golpe
        
        Pj.ataques = T.calcular_ATKs (Pj.stats['AtqB'],Pj.CARS['FUE']['Mod'],Pj.CARS['DES']['Mod'],
                                     Pj.tam,Pj.equipo,Pj.dotes,d.ARMAS,d.DOTES) # modificadores de ataque
        
        CA = T.calcular_CA (Pj.tam,Pj.CARS['DES']['Mod'],Pj.equipo,d.ARMDS) # CA
        Pj.stats['CA']['Normal'] = CA[0]
        Pj.stats['CA']['Toque'] = CA[1]
        Pj.stats['CA']['Desprevenido'] = CA[2]
        Pj.stats['Init'] = T.calcular_inic (Pj.CARS['DES']['Mod'],Pj.dotes,d.DOTES) # iniciativa
