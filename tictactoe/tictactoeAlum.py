from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import numpy as np
from itertools import combinations

visual = {1: "❌", -1: "⭕", 0.0: " "}


@dataclass
class Nodo:
    tablero: np.array
    vacias: int
    N: int

    def __init__(self, tablero):
        self.tablero = tablero
        self.N = self.tablero.shape[0]
        self.vacias = len(np.where(tablero == 0)[0])

    def __str__(self):
        string = f"{' ----+----+----'}\n|"
        for i in range(self.tablero.shape[0]):
            for j in range(self.tablero.shape[1]):
                if self.tablero[i, j] == 0:
                    string += "    |"
                else:
                    string += f" {visual[self.tablero[i, j]]} |"
            if i == 2 and j == 2:
                string += f"\n ----+----+----\n"
            else:
                string += f"\n ----+----+----\n|"
        return f"{string}"


@dataclass
class Jugada:
    x: int
    y: int

    def __str__(self):
        return f"\nFila: ({self.x}, Col: {self.y})"


######
# Se crean todas las posibles jugadas para el for de rango (for jugada in jugadas)
jugadas = []
for i in range(0, 3):
    for j in range(0, 3):
        jugadas.append(Jugada(i, j))
######

""" Funciones complementarias
    * crearNodo
    * nodoInicial
    * opuesto
"""


def crearNodo(tablero):
    return Nodo(tablero)


def nodoInicial():
    tablero_inicial = np.zeros((3, 3))
    return Nodo(tablero_inicial)


def opuesto(jugador):
    return jugador * -1


""" Funciones Búsqueda MiniMax
    * aplicaJugada
    * esValida
    * terminal
    * utilidad
"""


def aplicaJugada(actual: Nodo, jugada: Jugada, jugador: int) -> Nodo:
    nuevo = deepcopy(actual)
    nuevo.vacias -= 1
    nuevo.tablero[jugada.x, jugada.y] = jugador
    return nuevo


def esValida(actual: Nodo, jugada: Jugada) -> bool:
    return 0 <= jugada.x < actual.N and 0 <= jugada.y < actual.N and actual.tablero[jugada.x, jugada.y] == 0


def terminal(actual: Nodo) -> bool:
    esterminal = False
    comprobar = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    comprueba = np.reshape(actual.tablero, actual.N * actual.N)
    for pos in comprobar:
        if comprueba[pos[0]] == comprueba[pos[1]] and comprueba[pos[1]] == comprueba[pos[2]] and comprueba[pos[0]] != 0:
            esterminal = True
            
    return esterminal or actual.vacias == 0


def utilidad(nodo: Nodo) -> int:
    ganador = 0
    comprobar = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    comprueba = np.reshape(nodo.tablero, nodo.N * nodo.N)
    for pos in comprobar:
        if comprueba[pos[0]] != 0 and comprueba[pos[0]] == comprueba[pos[1]] and comprueba[pos[1]] == comprueba[pos[2]]:
            ganador = comprueba[pos[2]] * 100
    return ganador


# def heuristica(nodo: Nodo):
#     opciones = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
#     cont1 = 0
#     cont2 = 0
#     comprobar = np.reshape(nodo.tablero, nodo.N * nodo.N)
#     for pos in opciones:
#         if comprobar[pos[0]] == comprobar[pos[1]] == comprobar[pos[2]] == 1 :
#             cont1 += 1
#         elif comprobar[pos[0]] == comprobar[pos[1]] == comprobar[pos[2]] == -1:
#             cont2 += 1
#     return cont2 - cont1

def heuristica(nodo: Nodo):
    opciones = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    cont1 = 0
    cont2 = 0
    comprobar = np.reshape(nodo.tablero, nodo.N * nodo.N)
    for pos in opciones:
        if comprobar[pos[0]] == 1 :
            if comprobar[pos[1]] == 1 or comprobar[pos[1]] == 0 and comprobar[pos[2]] == 0 or comprobar[pos[2]] == 1 :
                cont1 += 1
        if comprobar[pos[1]] == 1 :
            if comprobar[pos[0]] == 1 or comprobar[pos[0]] == 0 and comprobar[pos[2]] == 0 or comprobar[pos[2]] == 1 :
                cont1 += 1
        if comprobar[pos[2]] == 1 :
            if comprobar[pos[1]] == 1 or comprobar[pos[1]] == 0 and comprobar[pos[0]] == 0 or comprobar[pos[0]] == 1 :
                cont1 += 1
    for pos in opciones:
        if comprobar[pos[0]] == -1 :
            if comprobar[pos[1]] == -1 or comprobar[pos[1]] == 0 and comprobar[pos[2]] == 0 or comprobar[pos[2]] == -1 :
                cont2 += 1
        if comprobar[pos[1]] == -1 :
            if comprobar[pos[0]] == -1 or comprobar[pos[0]] == 0 and comprobar[pos[2]] == 0 or comprobar[pos[2]] == -1 :
                cont2 += 1
        if comprobar[pos[2]] == -1 :
            if comprobar[pos[1]] == -1 or comprobar[pos[1]] == 0 and comprobar[pos[0]] == 0 or comprobar[pos[0]] == -1 :
                cont2 += 1
    return cont1 - cont2
