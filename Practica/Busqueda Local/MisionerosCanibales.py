from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer


# Estado = ( (numero de misioneros a la izquierda, numero de canibales a la izquierda) (numero de misioneros a la derecha, numero de canibales a la derecha) (posicion del bote siendo 1 a la izquierda y 0 a la derecha del rio) )


EstadoInicial = ((3,3),(0,0),(0))
EstadoAceptacion = ((0,0),(3,3),(1))

 
class MisionerosCanibalesProblem(SearchProblem):
  
    def cost(self, estado1, accion, estado2):
        return 1


    def is_goal(self, estado):
        return estado == EstadoAceptacion


    def actions(self, estado):
        
        gente_izquierda, gente_derecha, posicion_bote = estado
        gente_posicion_original = estado[posicion_bote]
        misioneros_posicion_original, canibales_posicion_original = gente_posicion_original
        acciones_posibles = []

        # recorro todas las acciones posibles a realizar 
        for misioneros_mover in (0, 1, 2):
            for canibales_mover in (0, 1, 2):
                # verifico que no se intente transportar mas gente de la que el bote resiste (no mas de 2)
                if ((misioneros_mover + canibales_mover) in (1,2)) and (misioneros_mover <= misioneros_posicion_original) and (canibales_mover <= canibales_posicion_original):
                    
                    actions = (misioneros_mover, canibales_mover)
                    # pruevo "realizar" el movimiento para ver como queda el contexto
                    estado_resultante = self.result(estado, actions)
                    # Compruebo si en dicho estado resultante los misioneros son deborados o no
                    misioneros_asalvo = True
                    for estado_costa in (estado_resultante[0], estado_resultante[1]):
                        misioneros_resultantes, canibales_resultantes = estado_costa
                        if (misioneros_resultantes > 0) and (misioneros_resultantes < canibales_resultantes):
                            misioneros_asalvo = False
                    
                    if misioneros_asalvo:
                        acciones_posibles.append(actions)

        return acciones_posibles


    def result(self, estado, accion):
        
        gente_izquierda, gente_derecha, posicion_bote = estado
        misioneros_mover, canibales_mover = accion

        # Combierto la tupla de gente del estado actual en una lista para poder modificarla
        Lista_gente_costa_origen = list(estado[posicion_bote])
        if posicion_bote == 0:
            proxima_posicion_bote = 1
        else:
            proxima_posicion_bote = 0
        Lista_gente_costa_destino = list(estado[proxima_posicion_bote])

        Lista_gente_costa_origen[0] -= misioneros_mover
        Lista_gente_costa_destino[0] += misioneros_mover

        Lista_gente_costa_origen[1] -= canibales_mover
        Lista_gente_costa_destino[1] += canibales_mover

        # Combierto la lista otra vez en tupla
        Tupla_gente_costa_origen = tuple(Lista_gente_costa_origen)
        Tupla_gente_costa_destino = tuple(Lista_gente_costa_destino)

        if proxima_posicion_bote == 0:
            return (Tupla_gente_costa_destino, Tupla_gente_costa_origen, proxima_posicion_bote)
        else:
            return (Tupla_gente_costa_origen, Tupla_gente_costa_destino, proxima_posicion_bote)


metodos = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for metodo_busqueda in metodos:
    print()
    print('=' * 80)

    print("corriendo:", metodo_busqueda)
    visor = BaseViewer()
    problema = MisionerosCanibalesProblem(EstadoInicial)
    result = metodo_busqueda(problema, graph_search=True, viewer=visor)

    print('estado final:')
    print(result.state)

    print('-' * 80)

#    for action, state in result.path():
#        print('accion:', action)
#        print('estado resultante:', state)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)

