from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda
from itertools import repeat

def GenerarEstadoInicial(NumeroJarras):
    estado = list((0,) * (NumeroJarras - 1))
    estado.append(NumeroJarras) 
    return tuple(estado)

def GenerarEstadoAceptacion(NumeroJarras):
    estado = (1,) * NumeroJarras
    return estado

# Estado = (cantidad de litros del jarro 1, cantidad de litros del jarro 2, cantidad de litros del jarro 3, cantidad de litros del jarro 4)

NumeroJarras = input("Ingrese el numero de jarras: ")
EstadoInicial = GenerarEstadoInicial(int(NumeroJarras))
print("Estado inicial: ",EstadoInicial)
EstadoAceptacion = GenerarEstadoAceptacion(int(NumeroJarras))
print("Estado aceptacion: ",EstadoAceptacion)


class LlenandoJarrosProblem(SearchProblem):
  
    def cost(self, estado1, accion, estado2):
        return accion[0] + 1


    def is_goal(self, estado):
        return estado == EstadoAceptacion


    def actions(self, estado):
        
        acciones_posibles = []
        # recorro todas las acciones posibles a realizar 
        for jarroOrigen, ContenidoJarroOrigen in enumerate(estado):
            if (ContenidoJarroOrigen > 0):
                for jarroDestino, ContenidoJarroDestino in enumerate(estado):
                    if (jarroOrigen != jarroDestino) and (ContenidoJarroDestino != (jarroDestino + 1)):
                        accion = (jarroOrigen, jarroDestino)
                        acciones_posibles.append(accion)

        return acciones_posibles


    def result(self, estado, accion):


        jarroOrigen, jarroDestino = accion


        # Convierto la tupla de gente del estado actual en una lista para poder modificarla
        Lista_estado = list(estado)

        AguaFaltante_JarroDestino = (jarroDestino + 1) - Lista_estado[jarroDestino] 

        if (Lista_estado[jarroOrigen] >= AguaFaltante_JarroDestino):
            Lista_estado[jarroOrigen] -= AguaFaltante_JarroDestino
            Lista_estado[jarroDestino] += AguaFaltante_JarroDestino
        else:            
            Lista_estado[jarroDestino] = Lista_estado[jarroOrigen]
            Lista_estado[jarroOrigen] = 0
       
        # Combierto la lista otra vez en tupla
        Tupla_estado = tuple(Lista_estado)

        return (Tupla_estado)


    def heuristic(self, estado):   
        return list(estado).count(0)


problema = LlenandoJarrosProblem(EstadoInicial)
metodosinformados = True
ImprimirBusqueda(problema,metodosinformados)

