from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda


# estado = [(posicionX-robot1,posicionY-robot1),(posicionX-robot2, posicionY-robot2)]
EstadoInicial = (0,1),(0,1)
salidas = (3,2),(0,4)
HabitacionesInaccesibles = (0,2),(1,3),(2,1)

class RobotsDefensivosSecretosProblem(SearchProblem):
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return set(EstadoInicial) == set(salidas)


    def actions(self, estado):       
        accionesPosibles = []

        movimientos = (
            (-1, 0),  # arriba
            (1, 0),  # abajo
            (0, -1),  # izquierda
            (0, 1),  # derecha
        )

        for robot, coordenadasRobot in enumerate(estado):
            for movimiento in movimientos:
                accion = [(0,0),0]
                accion[0] = (coordenadasRobot[0] + movimiento[0], coordenadasRobot[1] + movimiento[1])
                accion[1] = robot

                accesoNoAutorizado = accion[0] in HabitacionesInaccesibles
                dentroDelLimite = (0 <= accion[0][0] <= 3) and (0 <= accion[0][1] <= 4)
                enSalida = coordenadasRobot in salidas

                if ((not accesoNoAutorizado) and dentroDelLimite):
                    accionesPosibles.append(accion)

        return accionesPosibles


    def result(self, estado, accion):       
        
        nuevasCoordemnadas, robot = accion
        listaNuevoEstado = list(estado)
        listaNuevoEstado[robot] = nuevasCoordemnadas
        print(estado, accion, listaNuevoEstado)
        return tuple(listaNuevoEstado)



problema = RobotsDefensivosSecretosProblem(EstadoInicial)
metodosInformados = False
ImprimirBusqueda(problema,metodosInformados)






