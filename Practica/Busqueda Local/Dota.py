from simpleai.search import SearchProblem
from ImprimirResultados_1 import ImprimirBusqueda




# Estado = ((Pocicion X del Heroe Aliado, Pocicion Y del Heroe Aliado), Numero de Enemigos en el tablero)
UbicacionEnemigos = (1,1),(2,2)

EstadoInicial = (0,0), UbicacionEnemigos



class DotaProblem(SearchProblem):
    
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return (len(estado[1]) == 0)


    def actions(self, estado):
        
        acciones_posibles = []
        Movimientos = (
            (-1, 0),  # arriba
            (1, 0),  # abajo
            (0, -1),  # izquierda
            (0, 1),  # derecha
        )

        UbicacionHeroe, UbicacionEnemigosVivos = estado
        X, Y = UbicacionHeroe

        #Recorro cada movimienta
        for movimiento in Movimientos:           
            
            MovimientoX, MovimientoY = movimiento
            nueva_posicion = (X + MovimientoX , Y + MovimientoY)
        
            if (0 <= nueva_posicion[0] <= 2) and (0 <= nueva_posicion[1] <= 2):
                #Si se puede realizar la accion
                if (nueva_posicion not in UbicacionEnemigosVivos):
                    #Moverse
                    acciones_posibles.append((nueva_posicion,"Mover"))
                else:
                    #Atacar
                    acciones_posibles.append((nueva_posicion,"Atacar"))

        return acciones_posibles


    def result(self, estado, accion):
        
        nueva_posicion, TipoAccion = accion

        # Convierto la tupla de gente del estado actual en una lista para poder modificarla
        Lista_estado = list(estado)

        Lista_estado[0] = nueva_posicion

        if (TipoAccion == "Atacar"):
            UbicacionEnemigosVivos = list(Lista_estado[1])
            UbicacionEnemigosVivos.remove(nueva_posicion)
            Lista_estado[1] = tuple(UbicacionEnemigosVivos)

        # Combierto la lista otra vez en tupla
        Tupla_estado = tuple(Lista_estado)

        return (Tupla_estado)



problema = DotaProblem(EstadoInicial)
metodosinformados = False
ImprimirBusqueda(problema,metodosinformados)