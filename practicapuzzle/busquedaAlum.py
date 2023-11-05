from __future__ import annotations
from NPuzle_Alum import *


@dataclass
class Nodo:
    estado: tEstado
    operador: str
    costeCamino: int
    profundidad: int
    valHeuristica: int  # Por el momento se le puede asignar el valor 0.
    padre: Nodo

    def __str__(self) -> str:
        return f'{"- " * 10}\n{self.estado.tablero}, Operador: {operadores[self.operador]}, Heu:{self.valHeuristica}\n{"- " * 10}'

    def hash(self) -> str:
        return self.estado.crearHash()


def nodoInicial() -> Nodo:
    return Nodo(estadoInicial(), "0", 0, 0, 0, None)


def dispCamino(nodo):
    lista = []
    aux = nodo
    while aux.padre != None:
        lista.append((aux.estado.tablero, aux.operador))
        aux = aux.padre
    for i in lista[::-1]:
        print("Movimiento hacia: ", operadores[i[1]], "\n", i[0])
        print()


def dispSolucion(nodo):
    dispCamino(nodo)
    print("Profundidad: ", nodo.profundidad)
    print("Coste: ", nodo.costeCamino)


def expandir(nodo) -> list:
    nodos = []
    for operador in operadores.keys:
        if esValido(operador, nodo.estado):
            nuevo = aplicaOperador(operador, nodo.estado)
            nodo.append(nuevo)
    return nodos


def busquedaAnchura() -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    while objetivo == False and len(abiertos):
        abiertos.append(raiz)
        abiertos.pop(0)
        objetivo = testObjetivo()
        if objetivo == False:
            sucesores.extend(raiz)
            abiertos.extend(sucesores)
            
    # Completar el resto del código

    if objetivo:
        dispSolucion()  # Completar
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo
