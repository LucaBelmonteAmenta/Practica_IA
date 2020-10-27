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
# Ciudades = Ciudades_Conexiones.keys()   ----------->    ['rafaela', 'santa_fe', ...]

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


# Camion = (IdCamion, ciudad, litros, (Paquete, ))
# Paquete = (IdPaquete1, IdPaquete2, ...)
# Estado = ( ( Camion, ), ( Paquete que no esta en un camion, ) )
# Accion = (IdCamion, CiudadDestino, (Idpaquete, ))


def devolverCamionEspesifico(state, IdCamionEspesifico):
    camiones, paquetes_fuera_de_camiones = state
    for camion in camiones:
        IdCamion, ciudad, litros, paquetes_del_camion = camion
        if (IdCamionEspesifico == IdCamion):
            return camion

class MercadoArtificialProblem(SearchProblem):
  
    def cost(self, state1, action, state2):
        IdCamion, CiudadDestino, Paquetes = action
        camion = devolverCamionEspesifico(state1, IdCamion)
        IdCamion, ciudad_camion, litros, paquetes_del_camion = camion
        # Busco de la distancia entre la ciudad en la que      #
        # estaba el camión y la ciudad de destino de la acción #
        for ciudad in Ciudades_Conexiones[ciudad_camion]:                  
            if (ciudad[0] == action[1]):
                distancia = ciudad[1]
                break
        # Retorno el combustible gastado para dicha distancia a recorrer #
       
        costo_viaje = distancia/100
        
        return costo_viaje


    def is_goal(self, state):
        # es goal si todos los camiones repartieron todos los paquetes y se encuentran en una ciudad sede
        camiones, paquetes_fuera_de_camiones = state
        isgoal = True
        # pregunto si hay paquetes que quedaron pendientes
        if len(paquetes_fuera_de_camiones) != 0:
            isgoal = False
        else:
            # entonces recorro cada camión preguntando si no está en una sede y si quedaron paquetes por entregar
            for camion in camiones:
                IdCamion, ciudad, litros, paquetes_del_camion = camion
                if (ciudad not in CiudadesSedes) or (len(paquetes_del_camion) != 0):
                    isgoal = False
        
        return isgoal


    def actions(self, state):     
        camiones, paquetes_fuera_de_camiones = state
        acciones = []
        
        # Recorro cada camión, y por cada camión, recorro también las ciudades a las que podría ir en este viaje #
        for camion in camiones:           
            IdCamion, ciudad_camion, litros, paquetes_del_camion = camion

            for ciudad in Ciudades_Conexiones[ciudad_camion]:
                
                # Genero la acción del viaje en el caso de que no halla recogido ningún paquete de donde estuvo #
                listaPaquetesCamion = list(paquetes_del_camion)
                accion = IdCamion, ciudad[0], paquetes_del_camion
                
                litrosDelViaje = self.cost(state, accion, ("vacio"))
                # No cargare ninguna accion si el vehiculo no es capaz de afrontar #
                # el gasto de combustible del viaje que implica dicha accion       #
                if (litros >= litrosDelViaje):

                    # Cargo la acción del viaje en el caso de que no halla recogido ningún paquete de donde estuvo #
                    acciones.append(accion)
                
                    # Recorro cada paquete que no se encuentre en un camion y guardo #
                    # los que podría recoger de la ciudad en la que me encontraba #
                    paquetesTransportables = []
                   
                    for paquete in paquetes_fuera_de_camiones:
                        origen_paquete, destino_paquete = PAQUETES[paquete]

                        #paquetesTransportables = []
                        if (origen_paquete == ciudad_camion):
                            paquetesTransportables.append(paquete)

                   
                    if (len(paquetesTransportables) > 0):
                        
                        # Genero una accion por cada combinacion posible de paquete recogido #
                        # EJ: Habiendo 3 paquetes, podria cargar en el camion cualquiera de  #
                        #     los 3 o cualquier combinacion de 2, o los tres a la vez.       #
                        #for p in paquetesTransportables:

                        for X in range(1, (len(paquetesTransportables) + 1) ):       
                            for combinaciones in combinations(paquetesTransportables,X): 
                                listaPaquetesCamion = list(paquetes_del_camion)
                                listaPaquetesCamion.extend(combinaciones)
                                accion = IdCamion, ciudad[0], tuple(listaPaquetesCamion)
                                acciones.append(accion)      
        
        return acciones     


    def result(self, state, action):
        """
        a partir del estado y de la acción (camion, destino y paquetes que lleva) voy a:
        - cambiar la ciudad del camion del estado, por la de destino de la accion
        - a partir de los paquetes que tiene el camion en la acción, actualizo los que tiene el camion en el estado
        - mover a ciudad de la acción y restar combustible
        - si queda en estado resultante en una sede, cargo combustible

        Actualizar ciudad del camion y paquetes que lleva. Descontar combustible. Si donde llega es una
        sede, cargar combustible
        """
        
        camion, destino, paquetes_transportados = action    
        camiones, paquetes_que_no_estan_en_un_camion = state  
        # por cada camion (id, litrosdisponibles, ciudad, (paquetes) )
        paquetes_que_no_estan_en_un_camion = list(paquetes_que_no_estan_en_un_camion)
        camiones = list(camiones)
        nueva_lista_camiones = []
        for c in camiones:
            
            c = list(c)
           
            if c[0] == camion:
                
                # ahora analizar los paquetes
                if paquetes_transportados: # si hay paquetes en la acción
                    
                    # ver si los paquetes ya están en el camión (en el estado)
                    paquetes_camion = list(c[3])
                    for p in paquetes_transportados:
                        if p not in c[3]:
                            # si el paquete no está en el camion, cargarlo 
                            # sacarlo de la lista de paquetes que no estan en un camion.
                            paquetes_camion.append(p)
                            paquetes_que_no_estan_en_un_camion.remove(p)

                    
                    nuevos_paquetes_camion = list(paquetes_camion)
                    for p in paquetes_camion:
                        # ver si llegó al destino, sacar del estado
                        if PAQUETES[p][1] == destino:
                            nuevos_paquetes_camion.remove(p)

                    c[3] = tuple(nuevos_paquetes_camion)                         
                
                # ver el combustible que se gastará para llegar al destino, descontarlo
                litros_viaje = self.cost(state, action, ("vacio"))
                c[2] -= litros_viaje # c[1] son los litros disponibles del camión

                # si el destino es una sede, cargar combustible a capacidad máxima
                if destino in CiudadesSedes:
                    c[2] = CAMIONES[c[0]][1]
                
                # actualizar la ciudad en la que se encuentra el camion de la accion    
                c[1] = destino
            nueva_lista_camiones.append(tuple(c))
            

        camiones = tuple(nueva_lista_camiones)
        paquetes_que_no_estan_en_un_camion = tuple(paquetes_que_no_estan_en_un_camion)
        estado_resultante = camiones, paquetes_que_no_estan_en_un_camion
       
        return estado_resultante


    def heuristic(self,state):
        # La heurística es el cálculo de cuánto se estima de costo hasta llegar a la meta,
        # al calcular el costo con los litros que se gastan en cada viaje, entonces deberíamos
        # calcular lo que falta en litros también.
        # Tenemos en cuenta la distancia desde la ciudad actual de cada camion hasta alguna ciudad sede.

        camiones, paquetes_fuera_de_camiones = state

        distancia_total = 0
        for camion in camiones:
            IdCamion, ciudad_camion, litros, paquetes_del_camion = camion
            distancia_total+=distancia_a_sedes[ciudad_camion]

        return distancia_total/100

def planear_camiones(metodo, camiones, paquetes):
    # armar estado inicial en base a camiones y paquetes
    ESTADO_INICIAL = []
    detalle_camiones = [] # tendrá los datos que vienen en "camiones", y una tupla vacía inicialmente, que indica los 
    #paquetes que tiene ese camion cargados
    for camion in camiones:
        CAMIONES[camion[0]] = [camion[1], camion[2]] # guardar en diccionario para usarlo cuando se necesite
        listaCamion = list(camion)
        listaCamion.append(())
        detalle_camiones.append(tuple(listaCamion)) # () indica que el camion no tiene aun paquetes cargados
    ESTADO_INICIAL.append(tuple(detalle_camiones)) # convierto la lista a tupla y la almaceno en la primer tupla
    #del estado inicial

    paquetes_que_no_estan_en_un_camion = [] # inicialmente tendrá todos los id de todos los paquetes
    for paquete in paquetes:
        id_paquete, origen, destino = paquete
        paquetes_que_no_estan_en_un_camion.append(id_paquete)
        # en una variable global que puede ser un diccionario PAQUETES, guardamos el origen y destino de 
        # cada paquete para cuando sea necesario consultarlo
        PAQUETES[id_paquete] = [origen, destino]

    ESTADO_INICIAL.append(tuple(paquetes_que_no_estan_en_un_camion)) # guardar en la segunda tupla del estado
    ESTADO_INICIAL = tuple(ESTADO_INICIAL)
   
    METODOS = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'iterative_limited_depth_first': iterative_limited_depth_first,
        'uniform_cost': uniform_cost,
        'astar': astar,
    }
    
    problema = MercadoArtificialProblem(ESTADO_INICIAL) #estado inicial armado en base a los camiones y paquetes...)
    result = METODOS[metodo](problema, graph_search=True)
    itinerario = []
    state1 = ESTADO_INICIAL
    #...armar el itinerario en base a la solución encontrada en result, leyendo result.path(),
    for action, state in result.path():
        if action == None:
            pass
        else:
            state2 = state
            # en state1 tengo dónde estaba el camión ANTES
            camion, destino, paquetes = action
            combustible_gastado = problema.cost(state1, action, state2)
            viaje = camion, destino, combustible_gastado, paquetes
            itinerario.append(viaje)
            state1 = state2
   
    return itinerario


if __name__ == '__main__':   

    camiones = [('c_normal', 'rafaela', 1.5),]
    paquetes = [('p_normal', 'rafaela', 'lehmann'), ('p_pasando_normal', 'rafaela', 'sunchales')]
    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        "breadth_first",camiones,paquetes
    )

    print("ITINERARIO: ",itinerario)