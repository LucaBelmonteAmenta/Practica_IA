from simpleai.search import SearchProblem
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
from simpleai.search.traditional import (
    breadth_first, 
    depth_first, 
    limited_depth_first, 
    iterative_limited_depth_first, 
    uniform_cost, 
    greedy, 
    astar
)




def ImprimirBusqueda(problema,metodosInformados):
    
    metodosBusquedaSinInformacion = (breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost)
    metodosBusquedaConInformacion = (greedy, astar)

    if metodosInformados:
        metodos = metodosBusquedaConInformacion
    else:
        metodos = metodosBusquedaSinInformacion
    
    for metodo_busqueda in metodos:
        print()
        print('=' * 80)

        print("corriendo:", metodo_busqueda)
        visor = BaseViewer()
        result = metodo_busqueda(problema, graph_search=True, viewer=visor)
        
        if (result is None):
            print("No se pudo llegar al resultado")
        else:
            print('estadísticas:')
            print('cantidad de acciones hasta la meta:', len(result.path()))
            print(visor.stats)
            
            #print('estado final:')
            #print(result.state)
            #print('-' * 80)

            for action, state in result.path():
                print('accion:', action)
                print('estado resultante:', state)


