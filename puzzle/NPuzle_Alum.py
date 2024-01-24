import numpy as np
from dataclasses import dataclass
from copy import deepcopy

operadores = {"8": "ARRIBA", "2": "ABAJO", "4": "IZQUIERDA", "6": "DERECHA"}


@dataclass
class tEstado:
    tablero: np.ndarray
    fila: int
    col: int

    def __init__(self, tablero: np.ndarray):
        self.tablero = tablero
        self.N = self.tablero.shape[0]
        self.fila, self.col = np.where(self.tablero == 0)

    def __repr__(self) -> str:
        return f"{self.tablero}\n Fila: {self.fila}\n Col: {self.col}\n"

    def crearHash(self) -> str:
        return f"{self.tablero.tobytes()}{self.fila}{self.col}"


def estadoInicial() -> tEstado:
    puzle_inicial = np.array([[0, 2, 3], [1, 4, 5], [8, 7, 6]])
    return tEstado(puzle_inicial)


def estadoObjetivo() -> tEstado:
    puzle_final = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    return tEstado(puzle_final)


def coste(op, estado):
    return 1


def dispOperador(operador):
    print("~" * 10)
    print("Movimiento hacia ", operadores[operador])


def iguales(actual, objetivo) -> bool:
    return np.array_equal(actual.tablero, objetivo.tablero)


def testObjetivo(actual) -> bool:
    objetivo = estadoObjetivo()
    return iguales(actual, objetivo)


def esValido(op: str, estado) -> bool:
    valido = False
    match operadores[op]:
        case "ARRIBA":
            valido = estado.fila > 0
        case "ABAJO":
            valido = estado.fila < estado.N - 1
        case "IZQUIERDA":
            valido = estado.col > 0
        case "DERECHA":
            valido = estado.col < estado.N - 1
    return valido


def aplicaOperador(op: str, estado) -> bool:
    nuevo = deepcopy(estado)
    ficha = 0
    match operadores[op]:
        case "ARRIBA":
            ficha = nuevo.tablero[nuevo.fila - 1, nuevo.col]
        case "ABAJO":
            ficha = nuevo.tablero[nuevo.fila + 1, nuevo.col]        
        case "IZQUIERDA":
            ficha = nuevo.tablero[nuevo.fila, nuevo.col - 1]
        case "DERECHA":
            ficha = nuevo.tablero[nuevo.fila, nuevo.col + 1]
    nuevo.fila, nuevo.col = np.where(nuevo.tablero == ficha)
    nuevo.tablero[nuevo.fila, nuevo.col] = 0
    nuevo.tablero[estado.fila, estado.col] = ficha
    return nuevo
