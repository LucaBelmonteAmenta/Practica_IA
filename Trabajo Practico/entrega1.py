from simpleai.search import SearchProblem

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
    pass