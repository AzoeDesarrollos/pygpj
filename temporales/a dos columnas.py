import csv
csv.register_dialect('myCSV',delimiter=';')

def leerCSV (archivo):
    arch = csv.reader(open(archivo),dialect='myCSV')
    temp = []
    for t in arch:
        temp.append(t)
    if len(temp) == 1:
        temp = temp[0]
    return temp

habs = leerCSV('D:/Python/GPJ/data/habs.csv')

del habs[44]

c1 = []
c2 = []
for i in habs:
    if habs.index(i) < len(habs)/2:
        c1.append(i)
    else:
        c2.append(i)

for i in range(int(len(habs)/2)):
    if len(c1[i]+': ') > 23:
        print (c1[i]+': ',c2[i]+': ',sep='\t')
    elif len(c1[i]+': ') > 15:
        print (c1[i]+': ',c2[i]+': ',sep='\t\t')
    else:
        print (c1[i]+': ',c2[i]+': ',sep='\t\t\t')

while True:
        pass
