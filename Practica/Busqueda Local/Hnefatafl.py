from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda


# Estado = (Pocicion X del rey, Pocicion Y del rey)

ubicacionesEnemigos = (
    (0,0),
    (0,1),
    (0,4),
    (1,4),
    (2,0),
    (3,1),
    (3,6),
    (4,0),
    (6,3),
    (6,5),
)

EstadoInicial = (3,3)


class HnefataflProblem(SearchProblem):
    
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return (estado[0] in (0,6)) or (estado[1] in (0,6))


    def actions(self, estado):
        
        acciones_posibles = []

        Movimientos = (
            (-1, 0),  # arriba
            (1, 0),  # abajo
            (0, -1),  # izquierda
            (0, 1),  # derecha
        )

        for movimiento in Movimientos:  

            nuevoEstado = list(estado)
            nuevoEstado[0] += movimiento[0]
            nuevoEstado[1] += movimiento[1]
            
            sobreElEnemigo = nuevoEstado in ubicacionesEnemigos

            adjacenteAlEnemigo = False

            dentroDelTablero = ( (0 <= nuevoEstado[0] <= 6) and (0 <= nuevoEstado[1] <= 6))

            for movimientoVirtual in Movimientos: 

                EstadoVirtual = list(nuevoEstado)
                EstadoVirtual[0] += movimientoVirtual[0]
                EstadoVirtual[1] += movimientoVirtual[1]
                EstadoVirtual = tuple(EstadoVirtual)

                if (EstadoVirtual in ubicacionesEnemigos):
                    adjacenteAlEnemigo = True

            if (not sobreElEnemigo) and (not adjacenteAlEnemigo) and dentroDelTablero:
                acciones_posibles.append(tuple(nuevoEstado)) 

        return acciones_posibles


    def result(self, estado, accion):
        return (accion)



problema = HnefataflProblem(EstadoInicial)
metodosinformados = False
ImprimirBusqueda(problema,metodosinformados)