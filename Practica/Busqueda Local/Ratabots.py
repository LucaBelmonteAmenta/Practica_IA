from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda

# estado = ((coordenadas del ratabot x,y),((coordenadas comida 1),(coordenadas comida 2),(coordenadas comida 3)))

coordenadasComidas = (1,2),(4,0),(3,4)
salida = (3,5)

EstadoInicial = (3,5), coordenadasComidas
EstadoAceptacion = (salida,(()))

# pares de coordenadas de las paredes internas al laberinto
paredes = [
    (0,3),
    (0,5),
    (1,1),
    (1,3),
    (2,2),
    (2,4),
    (3,0),
    (4,1),
    (4,3),
    (4,5),
    (5,3)
]

class RatabotsProblem(SearchProblem):

    def distanciaEntre(self, coordenadas1, coordenadas2):
        x1, y1 = coordenadas1
        x2, y2 = coordenadas2
        return (max(x1,x2) - min(x1,x2)) + (max(y1,y2) - min(y1,y2))
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return estado == EstadoAceptacion


    def actions(self, estado):
        
        coordenadasRatabot, coordenadasComidas = estado
        coordenadaX,coordenadaY  = coordenadasRatabot
    
        acciones_posibles = []

        movimientos = (
            (1,0),
            (-1,0),
            (0,1),
            (0,-1)
        )

        for movimiento in movimientos:
            
            nuevasCoordenadasRatabot = list(coordenadasRatabot)
            nuevasCoordenadasRatabot[0] += movimiento[0]
            nuevasCoordenadasRatabot[1] += movimiento[1]
            
            dentroDelLaberinto = ( (0 <= nuevasCoordenadasRatabot[0] <= 5) and (0 <= nuevasCoordenadasRatabot[1] <= 5))

            SuperposicionParedes =  tuple(nuevasCoordenadasRatabot) in paredes
            
            if((not SuperposicionParedes) and dentroDelLaberinto):
                acciones_posibles.append(tuple(nuevasCoordenadasRatabot))

        return acciones_posibles


    def result(self, estado, accion):
        
        coordenadasRatabot, coordenadasComidas = estado
        
        ListaComidas = []
        for coordenadaComida in coordenadasComidas:
            if (accion != coordenadaComida):
                ListaComidas.append(coordenadaComida)

        nuevoEstado = accion, tuple(ListaComidas)

        return (nuevoEstado)

    def heuristic(self,estado):
        
        coordenadasRatabot, coordenadasComidas = estado

        heuristica = 0

        for coordenadaComida in coordenadasComidas: 
            heuristica += self.distanciaEntre(coordenadaComida,coordenadasRatabot) + self.distanciaEntre(coordenadaComida,salida)

        return heuristica


problema = RatabotsProblem(EstadoInicial)
metodosinformados = True
ImprimirBusqueda(problema, metodosinformados)