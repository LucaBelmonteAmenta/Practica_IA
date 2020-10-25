from simpleai.search import SearchProblem
from itertools import combinations

PAQUETES = {} # como en el estado haremos referencia a los ids de los paquetes, en este diccionario almacenamos
# el origen y destino de los mismos.



Ciudades_Conecciones = {
    'rafaela' : (('lehmann', 8), ('esperanza', 70), ('susana', 10)),
    'santa_fe' : (('recreo', 10), ('santo_tome', 5)),
    'lehmann' : (('rafaela', 8)),
    'sunchales' : (('lehmann', 32)),
    'susana' : (('angelica', 25), ('rafaela', 10)),
    'santa_clara_de_saguier' : (('angelica', 60)),
    'angelica' : (('santo_tome', 85), ('san_vicente', 18), ('santa_clara_de_saguier', 60), ('susana', 25)),
    'san_vicente' : (('angelica', 18)),
    'esperanza' : (('recreo', 20), ('rafaela', 70)),
    'recreo' : (('esperanza', 20), ('santa_fe', 10)), 
    'santo_tome' : (('santa_fe', 5), ('angelica', 85), ('sauce_viejo', 15)), 
    'sauceviejo' : (('santo_tome', 15))
}

# Ciudades = Ciudades_Conecciones.keys()   ----------->    ['rafaela', 'santa_fe', ...]

CiudadesSedes = ('rafaela', 'santa_fe')


class Camion:

    paquetes = []
    
    def __init__(self, IdCamion, litros, ciudad):
        self.IdCamion = IdCamion
        self.litros = litros
        self.ciudad = ciudad
    

class Paquete:
    
    def __init__(self, IdPaquete, ciudadOrigen, ciudadDestino):
        self.IdPaquete = IdPaquete
        self.ciudadOrigen = ciudadOrigen
        self.ciudadDestino = ciudadDestino


class Estado:

    camiones = []
    paquetes = []

    def __init__(self, estado):
        
        tuplaCamiones, tuplaPaquetes = estado
        
        for camion in tuplaCamiones:
            nuevoCamion = Camion(camion[0],camion[1],camion[2])
            
            for paquete in camion[3]:
                nuevoPaquete = Paquete(paquete[0],paquete[1],paquete[2])
                nuevoCamion.paquetes.append(nuevoPaquete)

            self.camiones.append(nuevoCamion)
        
        for paquete in tuplaPaquetes:
            nuevoPaquete = Paquete(paquete[0],paquete[1],paquete[2])
            self.paquetes.append(nuevoPaquete)
    
    def devolverTupla(self):
        listaCamiones = [] 

        for camion in self.camiones:
            listaPaquetes = []

            for paquete in camion.paquetes:
                tuplaPaquete = paquete.IdPaquete, paquete.ciudadOrigen, paquete.ciudadDestino
                listaPaquetes.append(tuplaPaquete)

            tuplaCamion = camion.IdCamion , camion.litros , camion.ciudad, tuple(listaPaquetes)
            listaCamiones.append(tuplaCamion) 

        listaPaquetes = []

        for paquete in self.paquetes:
            tuplaPaquete = paquete.IdPaquete, paquete.ciudadOrigen, paquete.ciudadDestino
            listaPaquetes.append(tuplaPaquete)

        return (listaCamiones, listaPaquetes)

        

# Camion = (IdCamion,litros,ciudad, (Paquete, ))
# Paquete = (IdPaquete, ciudadOrigen, ciudadDestino)
# Estado = ( ( Camion, ), ( Paquete que no esta en un camion, ) )
# Accion = (IdCamion, CiudadDestino, litrosVieaje, (Idpaquete, ))



class MercadoArtificialProblem(SearchProblem):
  
    def cost(self, state1, action, state2):
        estado = Estado(state1) 

        # Recorro los camiones del estado, buscando el que está en la acción #
        for camion in estado.camiones:      
            if (camion.IdCamion == action[0]):
                
                # Una vez encontrado el camión, busco de igual forma la #
                # distancia entre la ciudad en la que estaba el camión  #
                # y la ciudad de destino de la acción #
                for ciudad in Ciudades_Conecciones[camion.ciudad]:                  
                    if (ciudad[0] == action[1]):
                        distancia = ciudad[1]
                        break

                break
        # Retorno el combustible gastado para dicha distancia a recorrer #
        return distancia/100


    def is_goal(self, state):
        pass


    def actions(self, state):     
        estado = Estado(state) 
        acciones = []

        # Recorro cada camión, y por cada camión, recorro también las ciudades a las que podría ir en este viaje #
        for camion in estado.camiones:
            for ciudad in Ciudades_Conecciones[camion.ciudad]:

                # Cargo la acción del viaje en el caso de que no halla cargado ningún paquete de donde estuvo #
                listaPaquetesCamion = list(camion.paquetes)
                accion = camion.IdCamion, ciudad[0], tuple(listaPaquetesCamion)
                acciones.append(accion)
                
                # Recorro cada paquete que no se encuentre en un camion y guardo #
                # los que podría recoger de la ciudad en la que me encontraba #
                paquetesTransportables = []
                for paquete in estado.paquetes:
                    paquetesTransportables = []
                    if (paquete.ciudadOrigen == camion.ciudad):
                        paquetesTransportables.append(paquete)
                
                if (len(paquetesTransportables) > 0):
                    # Genero una accion por cada combinacion posible de paquete recogido #
                    # EJ: Habiendo 3 paquetes, podria cargar en el camion cualquiera de  #
                    #     los 3 o cualquier combinacion de 2, o los tres a la vez.       #
                    for X in range(1,len(paquetesTransportables)):       
                        for combinaciones in combinations(paquetesTransportables,X): 
                            listaPaquetesCamion = list(camion.paquetes)    
                            listaPaquetesCamion.extend(combinaciones)
                            accion = camion.IdCamion, ciudad[0], tuple(listaPaquetesCamion)
                            acciones.append(accion)

        return acciones

                
                
        


    def result(self, state, action):       
        pass


    def heuristic(self,state):
        pass



def planear_camiones(metodo, camiones, paquetes):
    # armar estado inicial en base a camiones y paquetes
    
    # Estado = ( (Camion, ), (Paquete que no está en un camion, ) )
    ESTADO_INICIAL = ()
    ESTADO_INICIAL = list(ESTADO_INICIAL)
    detalle_camiones = [] # tendrá los datos que vienen en "camiones", y una tupla vacía inicialmente, que indica los 
    #paquetes que tiene ese camion cargados
    for camion in camiones:
        detalle_camiones.append((camion, ())) # () indica que el camion no tiene aun paquetes cargados
    ESTADO_INICIAL[0] = tuple(detalle_camiones) # convierto la lista a tupla y la almaceno en la primer tupla
    #del estado inicial

    paquetes_que_no_estan_en_un_camion = [] # inicialmente tendrá todos los id de todos los paquetes
    for paquete in paquetes:
        id_paquete, origen, destino = paquete
        paquetes_que_no_estan_en_un_camion.append(id_paquete)
        # en una variable global que puede ser un diccionario PAQUETES, guardamos el origen y destino de 
        # cada paquete para cuando sea necesario consultarlo
        PAQUETES[id_paquete] = [origen, destino]

    ESTADO_INICIAL[1] = tuple(paquetes_que_no_estan_en_un_camion) # guardar en la segunda tupla del estado

    problema = MercadoArtificialProblem(tuple(ESTADO_INICIAL))#estado inicial armado en base a los camiones y paquetes...)
    result = metodo(problema)
    itinerario = []
    #...armar el itinerario en base a la solución encontrada en result, leyendo result.path(),
    for action, state in result.path():
        itinerario.append(action) # si tenemos en cuenta la misma estructura para actions, el profe dijo que 
        # podemos definir como queramos las acciones, de ultima después se cambia dependiendo lo que se haga en actions

    return itinerario

