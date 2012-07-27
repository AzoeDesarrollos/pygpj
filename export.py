# coding=UTF-8
'''Modulo de Exportación'''
import prsnj as p
import setup as s

# Aplicar modificadores
# Raciales
for r in p.raciales:
    p.rcl[r[0]]+=r[1]

# Por Dotes
for d in p.dotes:
    if 'Hab_dt' in s.DOTES[d]:
        for i in s.DOTES[d]['Hab_dt']:
            p.dts[i]+=2

# Por Objetos
## aún no implementado

# Por sinergias
for r in range(len(p.rng)):
    if p.rng[r] >= 5:
        if 'Sinergias' in setup.HABS[r]:
            for i in s.HABS[r]['Sinergias']:
                sng[i]+=2

# Ordenar las habilidades que se van a imprimir
temp = []
t = -1
imprimir = ''

# Rangos de habilidad
for r in p.rng:
    t+=1
    if p.rng[t]>0:
        if setup.HABS[t]['Nombre'] not in temp:
            temp.append(setup.HABS[t]['Nombre'])

# Bonificadores raciales
t = -1
for r in p.rcl:
    t+=1
    if p.rcl[t]>0:
        if setup.HABS[t]['Nombre'] not in temp:
            temp.append(setup.HABS[t]['Nombre'])

# Bonificadores de sinergia
t = -1
for r in p.sng:
    t+=1
    if p.sng[t]>0:
        if setup.HABS[t]['Nombre'] not in temp:
            temp.append(setup.HABS[t]['Nombre'])

# Bonificadores por dotes
t = -1
for r in p.dts:
    t+=1
    if p.dts[t]>0:
        if setup.HABS[t]['Nombre'] not in temp:
            temp.append(setup.HABS[t]['Nombre'])

temp.sort()

## Eliminar las habilidades 'solo entrenadas' sin rangos
#for h in temp:
#    if rng[habs.index(h)] == 0:
#        if habs.index(h) in hab_n_E:
#            del temp[temp.index(h)]

for h in temp:
    imprimir = imprimir+h+' +'+str(HabMod(hab_mods,habs.index(h),FUE_mod,DES_mod,CON_mod,INT_mod,SAB_mod,CAR_mod))+', '
imprimir = imprimir.rstrip(', ')+'.'

#Output
if input('Deseas Guardar este personaje?\n').lower().startswith('s'):
    nombre = input('\nNombre: ').capitalize()
    Pj = open('Personajes/'+nombre+'.txt','w')
    Pj.write('Nombre: '+nombre+'\n')
    Pj.write('Tipo y Tamaño: Humanoide '+p.tam_nom+' ('+p.subtipo+')\n')
    #Pj.write('DG: '+PG[1]+' ('+str(PG[0])+' pg)\n')
    Pj.write('Iniciativa: +'+str(Iniciativa)+'\nVelocidad: '+velocidad+'\n\n')
    Pj.write("Ataque base: +"+str(ATKbase)+"\nPresa: +"+str(Presa)+"\n\nE/A: 5'/5'.\n\n\n")
    Pj.write('TS: Fortaleza +'+str(Fort)+', Reflejos +'+str(Ref)+', Voluntad +'+str(Vol)+'\n')
    Pj.write('Características: Fuerza '+str(fFUE)+', Destreza '+str(fDES)+', Constitución '+str(fCON)+
             ', Inteligencia '+str(fINT)+', Sabuduría ' + str(fSAB)+', Carisma '+str(fCAR)+
             '.\nHabilidades y Dotes: '+imprimir+' '+PrepPrint(dotes[1]))
    sleep(3)
    print('\nPersonaje Guardado')
    Pj.close()
print ('Gracias')
sleep (2)