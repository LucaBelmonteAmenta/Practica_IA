from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda


# Estado = ((Pocicion X del Caballero, Pocicion Y del Caballero), (coordenadas por las que fue pasando el Caballero))


EstadoInicial = (0,0),((0,0),)


class TourDelCaballeroProblem(SearchProblem):
    
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return len(set(estado[1])) == 64


    def actions(self, estado):
        
        posicionActualCaballero, posicionesPorLasQuePaso = estado   
        acciones_posibles = []

        Movimientos = (
            (2,1),
            (2,-1),
            (-2,1),
            (-2,-1),
            (1,2),
            (1,-2),
            (-1,2),
            (-1,-2),
        )
        
        for movimiento in Movimientos:  

            nuevaPosicion = list(posicionActualCaballero)
            nuevaPosicion[0] += movimiento[0]
            nuevaPosicion[1] += movimiento[1]
            
            posicionRepetida = nuevaPosicion in posicionesPorLasQuePaso
            dentroDelTablero = ( (0 <= nuevaPosicion[0] <= 7) and (0 <= nuevaPosicion[1] <= 7))

            if (not posicionRepetida) and (dentroDelTablero):
                acciones_posibles.append(tuple(nuevaPosicion)) 

        return acciones_posibles


    def result(self, estado, accion):

        listaNuevoEstado = list(estado)
        listaNuevoEstado[0] = accion
        posicionesPorLasQuePaso = list(listaNuevoEstado[1])
        posicionesPorLasQuePaso.append(accion)
        listaNuevoEstado[1] = tuple(posicionesPorLasQuePaso)
        return (tuple(listaNuevoEstado))



problema = TourDelCaballeroProblem(EstadoInicial)
metodosinformados = False
ImprimirBusqueda(problema,metodosinformados)