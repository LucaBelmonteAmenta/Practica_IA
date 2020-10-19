from simpleai.search import (   
    CspProblem, 
    convert_to_binary,
    backtrack,    
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


def imprimirResultados(Variables, Dominios, Restricciones):

    problema = CspProblem(Variables, Dominios, Restricciones)

    resultado = backtrack(  problema,
                            variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                            value_heuristic=LEAST_CONSTRAINING_VALUE,
                            inference=True  )
    print('resultado con backtracking: ')
    print(resultado)
    print("-"*50)

    resultado = min_conflicts(problema, iterations_limit=500)
    print('resultado con minimos conflictos: ')
    print(resultado)
    print("-"*50)

    nuevasVariables, nuevosDominios, nuevasRestricciones = convert_to_binary(Variables, Dominios, Restricciones)
    problema = CspProblem(nuevasVariables, nuevosDominios, nuevasRestricciones)
    resultado = backtrack(  problema,
                            variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                            value_heuristic=LEAST_CONSTRAINING_VALUE,
                            inference=True)
    print('resultado con Binarizacion y resolviendo de nuevo con backtracking: ')
    print(resultado)
    print("-"*50)