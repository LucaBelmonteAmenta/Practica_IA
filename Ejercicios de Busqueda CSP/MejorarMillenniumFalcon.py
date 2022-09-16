from ImprimirResultados_2 import imprimirResultados
from itertools import combinations

#--------------------------------------------VARIABLES--------------------------------------------#

PosicionesFuselaje = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
Variables = PosicionesFuselaje

Interconecciones = {
    'P1': ['P2', 'P3'],
    'P2': ['P1', 'P3'],
    'P3': ['P2', 'P1'],
    'P4': [],
    'P5': ['P6'],
    'P6': ['P5'],
    'P7': ['P8'],
    'P8': ['P7'],
}

#--------------------------------------------DOMINIOS--------------------------------------------#

Mejoras = [ "Motor de salto a velocidad de la luz",
            "Sistema de ocultamiento",
            "Sistema de apuntamiento de armas",
            "Lanzador de torpedos de protones",
            "Bahía médica mejorada",
            "Sistema de evasión",
            "Bahía de carga mejorada",
            "Sistema de comunicaciones",
            "Escudo Mejorado"]


Dominios = {variable:["Sistema de comunicaciones", "Escudo Mejorado"] for variable in Variables }

Dominios["P7"].append("Motor de salto a velocidad de la luz") 
Dominios["P8"].append("Motor de salto a velocidad de la luz") 

Dominios["P1"].append("Sistema de ocultamiento") 
Dominios["P2"].append("Sistema de ocultamiento") 
Dominios["P3"].append("Sistema de ocultamiento") 
Dominios["P5"].append("Sistema de ocultamiento") 

Dominios["P1"].append("Sistema de apuntamiento de armas") 
Dominios["P2"].append("Sistema de apuntamiento de armas") 
Dominios["P3"].append("Sistema de apuntamiento de armas") 
# Dominios["P4"].append("Sistema de apuntamiento de armas") 

Dominios["P1"].append("Lanzador de torpedos de protones") 
Dominios["P2"].append("Lanzador de torpedos de protones") 

Dominios["P5"].append("Bahía médica mejorada") 
Dominios["P6"].append("Bahía médica mejorada") 
Dominios["P7"].append("Bahía médica mejorada") 
Dominios["P8"].append("Bahía médica mejorada") 

Dominios["P7"].append("Sistema de evasión") 
Dominios["P8"].append("Sistema de evasión") 

#--------------------------------------------RESTRICCIONES--------------------------------------------#

Restricciones = []

#ITEM 6
def NoRepetido(variables, valores):
    return len(set(valores)) == len(valores)
    
#ITEM 3
def OcultamientoMotor(variables, valores):
    mejorasIncompatibles = ("Sistema de ocultamiento","Motor de salto a velocidad de la luz")
    return set(valores) != set(mejorasIncompatibles)

#ITEM 10
def EscudosComunicaciones(variables, valores):
    mejorasInconectables = ("Sistema de comunicaciones", "Escudo Mejorado")
    return (set(valores) != set(mejorasInconectables)) or (variables[0] not in Interconecciones[variables[1]])


for posicion1,posicion2 in combinations(Variables,2):
    Restricciones.append(((posicion1,posicion2),NoRepetido))
    Restricciones.append(((posicion1,posicion2),OcultamientoMotor))
    Restricciones.append(((posicion1,posicion2),EscudosComunicaciones))



#--------------------------------------------RESOLUCION--------------------------------------------#

imprimirResultados(Variables, Dominios, Restricciones)