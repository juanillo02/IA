from Seminario4 import *

actual = estadoInicial()
print(actual)

while not testObjetivo(actual) and actual.N >= 2:
    oper = input(f"Seleccione un moviento {operadores}")
    if esValido(oper, actual):
        actual = aplicaOperador(oper, actual)
    print(actual)

if testObjetivo(actual):
    print("Objetivo logrado")

