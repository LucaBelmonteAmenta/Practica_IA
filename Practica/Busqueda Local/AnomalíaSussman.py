from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda
from itertools import permutations


EstadoInicial = ("B",),("A","C"),()
EstadoAceptacion =(),(),("C","B","A")



class AnomaliaSussmanProblem(SearchProblem):
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return estado == EstadoAceptacion


    def actions(self, estado):        
        accionesPosibles = []
        columnas = [0,1,2]

        for movimiento in permutations(columnas, 2):
            columnaOrigen, columnaDestino = movimiento
            if (len(estado[columnaOrigen]) > 0):
                accionesPosibles.append(movimiento)
        
        return accionesPosibles


    def result(self, estado, accion):
        columnaOrigen, columnaDestino = accion
        
        bloque = estado[columnaOrigen][-1]
        listaNuevoEstado = list(estado)

        origen = list(listaNuevoEstado[columnaOrigen]) 
        origen.pop(-1)
        listaNuevoEstado[columnaOrigen] = tuple(origen)

        destino = list(listaNuevoEstado[columnaDestino]) 
        destino.append(bloque)
        listaNuevoEstado[columnaDestino] = tuple(destino)

        return tuple(listaNuevoEstado)
    




problema = AnomaliaSussmanProblem(EstadoInicial)
metodosinformados = False
ImprimirBusqueda(problema,metodosinformados)
