from itertools import combinations

from simpleai.search import (
    SearchProblem, 
    breadth_first, 
    depth_first, 
    uniform_cost,
    astar,
    iterative_limited_depth_first
)

PAQUETES = {} # como en el estado haremos referencia a los ids de los paquetes, en este diccionario almacenamos
# el origen y destino de los mismos.

CAMIONES = {} # tendrá lo que se pasa como parámetro en planear_camiones, camion, origen, capacidadlitros

Ciudades_Conexiones = {
    'rafaela' : (('lehmann', 8), ('esperanza', 70), ('susana', 10)),
    'santa_fe' : (('recreo', 10), ('santo_tome', 5)),
    'lehmann' : (('rafaela', 8),('sunchales', 32),),
    'sunchales' : (('lehmann', 32),),
    'susana' : (('angelica', 25), ('rafaela', 10)),
    'sc_de_saguier' : (('angelica', 60),),
    'angelica' : (('santo_tome', 85), ('san_vicente', 18), ('sc_de_saguier', 60), ('susana', 25)),
    'san_vicente' : (('angelica', 18),),
    'esperanza' : (('recreo', 20), ('rafaela', 70)),
    'recreo' : (('esperanza', 20), ('santa_fe', 10)), 
    'santo_tome' : (('santa_fe', 5), ('angelica', 85), ('sauce_viejo', 15)), 
    'sauce_viejo' : (('santo_tome', 15),)
}

CiudadesSedes = ('rafaela', 'santa_fe')

# diccionario que especifica a que distancia se encuentra cada ciudad de la sede más cercana
distancia_a_sedes = {
    'rafaela' : 0,
    'santa_fe' : 0,
    'lehmann' : 8,
    'sunchales' : 40,
    'susana' : 10,
    'sc_de_saguier' : 95,
    'angelica' : 35,
    'san_vicente' : 53,
    'esperanza' : 30,
    'recreo' : 10, 
    'santo_tome' : 5, 
    'sauce_viejo' : 20,
}


# Camion = (IdCamion, ciudad, litrosActuales)
# Paquetes = ((IdPaquete,ubicacionActual), (IdPaquete,ubicacionActual), ...)
# Estado = ( ( Camion, ), ( Paquetes que no llegaron a su destino, ) )
# Accion = (IdCamion, CiudadDestino, (Idpaquete, ))

# a partir del id de un camión, devuelve la tupla de un camión
def devolverCamionEspecifico(state, IdCamionEspecifico):
    camiones, paquetes = state
    for camion in camiones:
        IdCamion, ciudad, litros = camion
        if (IdCamionEspecifico == IdCamion):
            return camion

class MercadoArtificialProblem(SearchProblem):
  
    def cost(self, state1, action, state2):
        IdCamion, CiudadDestino, Paquetes = action
        camion = devolverCamionEspecifico(state1, IdCamion)
        IdCamion, ciudad_camion, litros = camion
        # Busco de la distancia entre la ciudad en la que     
        # estaba el camión y la ciudad de destino de la acción 
        for ciudad in Ciudades_Conexiones[ciudad_camion]:                  
            if (ciudad[0] == action[1]):
                distancia = ciudad[1]
                break
        # Retorno el combustible gastado para dicha distancia a recorrer 
       
        costo_viaje = distancia/100
        
        return costo_viaje


    def is_goal(self, state):
        # es goal si todos los camiones repartieron todos los paquetes y se encuentran en una ciudad sede
        camiones, paquetes = state
        isgoal = True
        # pregunto si hay paquetes que quedaron pendientes
        if (len(paquetes) != 0):
            isgoal = False
        else:
            # entonces recorro cada camión preguntando si no está en una sede 
            for camion in camiones:
                IdCamion, ciudad, litros = camion
                if (ciudad not in CiudadesSedes):
                    isgoal = False
        
        return isgoal


    def actions(self, state):     
        camiones, paquetes = state
        acciones = []
        # serán tuplas con idcamión, destino, paquetes que transporta
        # Recorro cada camión, y por cada camión, recorro también las ciudades a las que podría ir en este viaje 
        for camion in camiones:           
            IdCamion, ciudad_camion, litros = camion

            for ciudad in Ciudades_Conexiones[ciudad_camion]:
                
                # Genero la acción del viaje en el caso de que no haya recogido ningún paquete de donde estuvo 
                paquetesTransportables = []
                accion = IdCamion, ciudad[0], tuple(paquetesTransportables)
                
                litrosDelViaje = self.cost(state, accion, ("vacio"))
                # No cargare ninguna accion si el vehiculo no es capaz de afrontar 
                # el gasto de combustible del viaje que implica dicha accion       
                if (litros >= litrosDelViaje):

                    # Cargo la acción del viaje 
                    acciones.append(accion)
                   
                    # recorrer los paquetes pendientes
                    for paquete in paquetes:
                        idPaquete, ubicacionActual = paquete
                        # ver si está en la ciudad en la que se encuentra el camión, si es así, agregar a paquetesTransportables
                        if (ubicacionActual == ciudad_camion):
                            paquetesTransportables.append(paquete[0])
                    
                    # si hay paquetes en esa ciudad
                    if (len(paquetesTransportables) > 0):               
                        # Genero una accion por cada combinacion posible de paquete recogido 
                        # EJ: Habiendo 3 paquetes, podria cargar en el camion cualquiera de  
                        #     los 3 o cualquier combinacion de 2, o los tres a la vez.       
                        for X in range(1, (len(paquetesTransportables) + 1) ):       
                            for combinaciones in combinations(paquetesTransportables,X): 
                                lista_a_transportar = tuple(combinaciones)
                                accion = IdCamion, ciudad[0], lista_a_transportar
                                acciones.append(accion)      
        
        return acciones     


    def result(self, state, action):
        """
        a partir del estado y de la acción (camion, destino y paquetes que lleva) voy a:
        - cambiar la ciudad del camion del estado, por la de destino de la accion
        - sacar un paquete del estado si ya llegó a su destino real
        - mover a ciudad de la acción y restar combustible
        - si queda en estado resultante en una sede, cargo combustible
        """     
        camion, destino, paquetes_transportados = action    
        camiones, paquetes = state  
         # Creamos una una lista de paquetes que solo tenga los paquetes que no estan en el destino
        listaPaquetes = []
        
        for paquete in paquetes:
            # Modifico la ubicacion de los paquetes que se van a transaportar
            
            if (paquete[0] in paquetes_transportados):
                nuevopaquete = (paquete[0],destino)
                # si el destino del paquete es diferente al destino real, lo agrego a la lista de paquetes pendientes
                if (nuevopaquete[1] != PAQUETES[paquete[0]][1]):
                    listaPaquetes.append(nuevopaquete)
            else:
                # si el paquete no está en destino real ni en paquetes_transportados, también lo agrego a paquetes pendientes
                if (paquete[1] != PAQUETES[paquete[0]][1]):
                    listaPaquetes.append(paquete)
      
        listaCamiones = list(camiones)
        camion_accion = devolverCamionEspecifico(state, camion)
        listaCamiones.remove(camion_accion)
        camion_accion = list(camion_accion)
        # ver el combustible que se gastará para llegar al destino, descontarlo
        litros_viaje = self.cost(state, action, ("vacio"))
        
        # si el destino es una sede, cargar combustible a capacidad máxima
        if destino in CiudadesSedes:
            camion_accion[2] = CAMIONES[camion_accion[0]][1]
        else:
            camion_accion[2] -= litros_viaje # c[1] son los litros disponibles del camión

        # actualizar la ciudad en la que se encuentra el camion de la accion    
        camion_accion[1] = destino
        listaCamiones.append(tuple(camion_accion))

        estado_resultante = tuple(listaCamiones), tuple(listaPaquetes)
        return estado_resultante


    def heuristic(self,state):       
        camiones, paquetes = state
        distancia_total = 0
        # combustible que le demanda a cada camión del estado para llegar a la sede más cercana
        for camion in camiones:
            IdCamion, ciudad_camion, litros = camion
            distancia_total+=distancia_a_sedes[ciudad_camion]

        # destinos distintos de los paquetes * combustible viaje mas corto
        destinos_paquetes = []
        for paquete in paquetes:
            destinos_paquetes.append(PAQUETES[paquete[0]][1])

        return (distancia_total/100) + (len(set(destinos_paquetes))* 0.05)


def planear_camiones(metodo, camiones, paquetes):
    # armar estado inicial en base a camiones y paquetes
    ESTADO_INICIAL = []
    detalle_camiones = [] # tendrá los datos que vienen en "camiones" (idcamion, origen, combustible máximo)
    for camion in camiones:
        CAMIONES[camion[0]] = [camion[1], camion[2]] # guardar en diccionario 
        listaCamion = list(camion)
        detalle_camiones.append(tuple(listaCamion)) 
    ESTADO_INICIAL.append(tuple(detalle_camiones)) # convierto la lista a tupla y la almaceno en la primer tupla
    #del estado inicial
    
    paquetes_estado = [] # inicialmente tendrá todos los ids de todos los paquetes y la ciudad de origen (id, ubicacion actual)
    for paquete in paquetes:
        id_paquete, origen, destino = paquete # nos llegan estos datos en la tupla paquete
        paquetes_estado.append((id_paquete, origen)) 
        PAQUETES[id_paquete] = [origen, destino] # diccionario con origen y destino de paquetes
    
    ESTADO_INICIAL.append(tuple(paquetes_estado)) # guardar en la segunda tupla del estado
    ESTADO_INICIAL = tuple(ESTADO_INICIAL)

    METODOS = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'iterative_limited_depth_first': iterative_limited_depth_first,
        'uniform_cost': uniform_cost,
        'astar': astar,
    }
    problema = MercadoArtificialProblem(ESTADO_INICIAL) 
    result = METODOS[metodo](problema, graph_search=True)
    itinerario = []
    state1 = ESTADO_INICIAL
    #...armar el itinerario en base a la solución encontrada en result, leyendo result.path(),

    # Accion = (IdCamion, CiudadDestino, (Idpaquete, ))
    for action, state in result.path():
        if action == None:
            pass
        else:
            # state es el estado que se obtiene a partir de la accion
            state2 = state
            # en state1 tengo dónde estaba el camión ANTES de la acción
            camion, destino, paquetes = action
            combustible_gastado = problema.cost(state1, action, state2)
            # armamos cada viaje a partir de la acción y el combustible gastado
            viaje = camion, destino, combustible_gastado, paquetes
            itinerario.append(viaje)
            state1 = state2
   
    return itinerario


if __name__ == '__main__':   
 
    camiones = [('c_normal', 'rafaela', 1.5),]
    paquetes = [('p_normal', 'rafaela', 'lehmann'), ('p_normal2', 'rafaela', 'lehmann'), ('p_pasando_normal', 'rafaela', 'sunchales'), ('p_invertido', 'lehmann', 'rafaela'), ('p_molesto', 'sunchales', 'susana'), ('p_opuesto', 'rafaela', 'susana')]
    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        "astar",camiones,paquetes
    )

    print("ITINERARIO: ",itinerario)