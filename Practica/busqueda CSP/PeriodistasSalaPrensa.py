from ImprimirResultados_2 import imprimirResultados
from itertools import combinations

#--------------------------------------------VARIABLES--------------------------------------------#

Variables = ["CNN1", "CNN2", "Fox", "BBC", "TheOnion","MSNBC1","MSNBC2","MSNBC3", "RT", "Infobae1", "Infobae2"]

#--------------------------------------------DOMINIOS--------------------------------------------#

DominioBase = []
for x in range(3):
    for y in range(4):
        DominioBase.append((x,y))
DominioBase = tuple(DominioBase)

Dominios = {variable:[asientos for asientos in DominioBase] for variable in Variables }

for variable in Variables[:4]:
    Dominios[variable] = [asiento for asiento in DominioBase if asiento[0] == 0]

Dominios["TheOnion"] = [asiento for asiento in DominioBase if asiento[0] == 2]

#--------------------------------------------RESTRICCIONES--------------------------------------------#

Restricciones = []


def contiguos(variables, valores):
    columnas = [valor[1] for valor in valores]
    minimo = min(columnas)
    maximo = max(columnas)
    columnasContiguas = [y for y in range(minimo, maximo + 1)]
    return set(columnas) == set(columnasContiguas)

Restricciones.append((("CNN1", "CNN2"),contiguos))

for variables in combinations(("MSNBC1","MSNBC2","MSNBC3"), 3):
    Restricciones.append((variables,contiguos))



def noContiguos(variables, valores):
    columnas = [valor[1] for valor in valores]
    condicion = (columnas[0] != (columnas[1] + 1)) and (columnas[1] != (columnas[0] + 1))
    return condicion

Restricciones.append((("BBC", "Fox"), noContiguos))
Restricciones.append((("Infobae1","Infobae2"),noContiguos))




def noSentarseCerca(variables, valores):

    Movimientos = (
        (-1, 0),  # arriba
        (1, 0),  # abajo
        (0, -1),  # izquierda
        (0, 1),  # derecha
    )

    condicion = True

    for movimiento in Movimientos:
        asientoAdyacente = list(valores[0])
        asientoAdyacente[0] += movimiento[0]
        asientoAdyacente[1] += movimiento[1]
        if (tuple(asientoAdyacente) == valores[1]):
            condicion = False
            break
    
    return condicion

Restricciones.append((("RT", "CNN1"), noSentarseCerca))
Restricciones.append((("RT", "CNN2"), noSentarseCerca))



def noRepetido(variables, valores):
    return valores[0] != valores[1]

for variables in combinations(Variables, 2):
    Restricciones.append((variables, noRepetido))


#--------------------------------------------RESOLUCION--------------------------------------------#

imprimirResultados(Variables, Dominios, Restricciones)




