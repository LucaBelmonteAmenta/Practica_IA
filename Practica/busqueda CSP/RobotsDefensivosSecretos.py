from ImprimirResultados_2 import imprimirResultados
from itertools import permutations

#--------------------------------------------VARIABLES--------------------------------------------#

Variables = ["Robot1", "Robot2", "Robot3", "Robot4", "Robot5","Robot6"]

#--------------------------------------------DOMINIOS--------------------------------------------#

HabitacionesInaccesibles = (0,2),(1,3),(2,1)
salidas = (3,2),(0,4)

DominioBase = []
for x in range(4):
    for y in range(5):
        if ((x,y) not in HabitacionesInaccesibles) and ((x,y) not in salidas):
            DominioBase.append((x,y))
DominioBase = tuple(DominioBase)

Dominios = {variable:[habitacion for habitacion in DominioBase] for variable in Variables }

Dominios["Robot1"] = [(3,2)]
Dominios["Robot2"] = [(0,4)]

#--------------------------------------------RESTRICCIONES--------------------------------------------#

Restricciones = []

def habitacionNoCompartida(variables, valores):
    return valores[0] != valores[1]

def habitacionesNoAdyacentes(variables, valores):

    Movimientos = (
        (-1, 0),  # arriba
        (1, 0),  # abajo
        (0, -1),  # izquierda
        (0, 1),  # derecha
    )

    condicion = True

    for movimiento in Movimientos:
        habitacionAdyacente = list(valores[0])
        habitacionAdyacente[0] += movimiento[0]
        habitacionAdyacente[1] += movimiento[1]
        if (tuple(habitacionAdyacente) == valores[1]):
            condicion = False
            break
    
    return condicion


for variables in permutations(Variables, 2):
    Restricciones.append((variables, habitacionNoCompartida))
    Restricciones.append((variables, habitacionesNoAdyacentes))


#--------------------------------------------RESOLUCION--------------------------------------------#

imprimirResultados(Variables, Dominios, Restricciones)