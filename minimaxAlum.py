from tictactoeAlum import *
from copy import deepcopy
import numpy as np

limite = 4

def PSEUDOminimax(nodo):
    mejorJugada = -1
    puntos = -2
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(nodo, jugada, 1)
            util = utilidad(intento)
            if util > puntos:
                puntos = util
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, 1)
    return nodo


def jugadaAdversario(nodo):
    valida = False
    jugada = None
    while not valida:
        fila = int(input("Fila: "))
        col = int(input("Col: "))
        jugada = Jugada(fila, col)
        valida = esValida(nodo, jugada)
        if not valida:
            print("\n Intenta otra posicion del tablero \n")
    nodo = aplicaJugada(nodo, jugada, -1)
    return nodo


def minimax(nodo: Nodo, jugador: int):
    max = -1000
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(deepcopy(nodo), jugada, jugador)
            max_actual = valorMin(intento)
            if max_actual > max:
                max = max_actual
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, jugador)
    return nodo


def valorMax(nodo: Nodo):
    if terminal(nodo):
        valor_max = utilidad(nodo)
    else:
        valor_max = np.inf
        for jugada in jugadas:
            if esValida(nodo, jugada):
                valor_max = max(valor_max, valorMin(aplicaJugada(nodo, jugada, 1)))
    return valor_max


def valorMin(nodo: Nodo):
    if terminal(nodo):
        valor_min = utilidad(nodo)
    else:
        valor_min = np.inf
        for jugada in jugadas:
            if esValida(nodo, jugada):
                valor_min = min(valor_min, valorMax(aplicaJugada(nodo, jugada, -1)))
    return valor_min

def poda_ab(nodo: Nodo, jugador):
    prof = 0
    beta = np.inf
    alfa = -np.inf
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(deepcopy(nodo), jugada, jugador)
            v = valorMin_ab(intento, prof+1, alfa, beta)
            if  v > alfa:
                alfa = v
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, jugador)
    return nodo

def valorMin_ab(nodo: Nodo, prof: int, alfa: int, beta: int):
    if terminal(nodo):
        vmin = utilidad(nodo)
    elif prof == limite:
        vmin = heuristica(nodo)
    else:
        i = 0
        while i < len(jugadas) and alfa < beta:
            jugada = jugadas[i]
            if esValida(nodo, jugada):
                intento = aplicaJugada(deepcopy(nodo), jugada, -1)
                beta = min(beta, valorMax_ab(intento, prof+1, alfa, beta))
            i += 1
        vmin = beta
    return vmin

def valorMax_ab(nodo: Nodo, prof: int, alfa: int, beta: int):
    if terminal(nodo):
        vmax = utilidad(nodo)
    elif prof == limite:
        vmax = heuristica(nodo)
    else:
        i = 0
        while i < len(jugadas) and alfa < beta:
            jugada = jugadas[i]
            if esValida(nodo, jugada):
                intento = aplicaJugada(deepcopy(nodo), jugada, 1)
                alfa = max(alfa, valorMin_ab(intento, prof+1, alfa, beta))
            i += 1
        vmax = alfa
    return vmax