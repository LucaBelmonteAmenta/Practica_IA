from ImprimirResultados_2 import imprimirResultados
from itertools import permutations

#--------------------------------------------VARIABLES--------------------------------------------#

Variables = []
nivelesPiramide = 4

for fila in range(1, nivelesPiramide + 1):
    for columna in range(1, fila + 1):
        Variables.append((fila, columna))

print("Variables: ", Variables)

#--------------------------------------------DOMINIOS--------------------------------------------#

DominioBase = []
for valores in range(1,51):
    DominioBase.append(valores)

Dominios = {variable:[valores for valores in DominioBase] for variable in Variables }

Dominios[(1,1)] = [48]
Dominios[(4,1)] = [5]
Dominios[(4,2)] = [8]
Dominios[(4,4)] = [3]

#--------------------------------------------RESTRICCIONES--------------------------------------------#

Restricciones = []

def noRepetidos(variables, valores):
    return valores[0] != valores[1]

for variables_2 in permutations(Variables, 2):
    Restricciones.append((variables_2, noRepetidos))



def resultadoSuma(variables, valores):
    valor1, valor2, valor3 = valores
    return valor1 == valor2 + valor3

for variable in Variables:
    if(variable[0] < nivelesPiramide):
        
        filaInferior = variable[0] + 1

        columnaInferior1 = variable[1]
        columnaInferior2 = variable[1] + 1

        bloqueInferior1 = (filaInferior, columnaInferior1)
        bloqueInferior2 = (filaInferior, columnaInferior2)

        Restricciones.append(((variable, bloqueInferior1, bloqueInferior2), resultadoSuma))
        Restricciones.append(((variable, bloqueInferior2, bloqueInferior1), resultadoSuma))
        print(variable, bloqueInferior1, bloqueInferior2)


#--------------------------------------------RESOLUCION--------------------------------------------#

imprimirResultados(Variables, Dominios, Restricciones)