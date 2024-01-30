# aqui realizo funciones extra para el modelo users
import random
from itertools import permutations


def code_numrandom(size=6):
    # Genera una lista de dígitos del 0 al 9
    digitos = list(range(10))
    # Selecciona 6 dígitos únicos aleatorios
    numeros_generados = random.sample(digitos, size)
    # Convierte la lista de dígitos en una cadena
    numeros_generados = ''.join(map(str, numeros_generados))
    return numeros_generados
