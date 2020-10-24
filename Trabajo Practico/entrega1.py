from simpleai.search import SearchProblem

PAQUETES = {} # como en el estado haremos referencia a los ids de los paquetes, en este diccionario almacenamos
# el origen y destino de los mismos.

Ciudades = ('rafaela', 'santa_fe' )
ConeccionesCiudades = { 'esperanza' : (('recreo',20), ('rafaela',70))}
CiudadesSedes = ('rafaela', 'santa_fe')

# Estado = ( ( (IdCamion,litros,ciudad), ), ( (IdPaquete, ciudadOrigen, ciudadDestino), ) )
# Accion = ((IdCamion, CiudadDestino, litrosVieaje, (Idpaquete, )), )

class MercadoArtificialProblem(SearchProblem):
  
    def cost(self, state1, action, state2):
        pass


    def is_goal(self, state):
        pass


    def actions(self, state):       
        pass


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

