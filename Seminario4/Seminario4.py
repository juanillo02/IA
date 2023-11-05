from __future__ import annotations #todo en python es un objeto, annotations:pistas
from dataclasses import dataclass #estructura en c
from copy import deepcopy  #parametros a funciones se pasan por referencia, entonces hacemos una copia explicita

operadores = {"1": "IZQUIERDA",
              "2": "DERECHA"}

@dataclass
class tEstado:
    #atributo
    tablro: list #el tablero es una lista donde esta el dinero
    ladrones: int
    banca: int
    N: int
    #Resto de funciones de laclase
    def __init__(self, tablero): #constructor con puntero self:a si mismo, puntero al objeto del objeto 
        self.tablero = tablero #el tablero que ha decidido el usuario(banquero)
        self.ladrones = 0 #valor inicial
        self.banca = 0
        self.N = len(tablero) #sacamos N= longitud del tablero

    def __str__(self) -> str:
        return f"{self.tablero}\nLadrones: {self.ladrones}\nBanca: {self.banca}"
    
def testObjetivo(estado) -> bool:
    return estado.N < 2 and estado.ladrones > estado.banca

def esValido(oper, estado) -> bool:
    return estado.N >= 2

def aplicaOperador(oper, estado) -> tEstado: #despues de la flecha pone el tipo que devulete, devuelve un estado
    nuevo = deepcopy(estado) #nuevo estado=copia del anterior
    match operadores[oper]: #match=switch
        case "IZQUIERDA":
            nuevo.ladrones += estado.tablero[0]
            nuevo.banca += estado.tablero[-1] #estado.tablero[estado.N -1]
            nuevo.tablero.pop(estado.N - 1) #quitamos lo que habia a la derecha 
            nuevo.tablero.pop(0) #quitamos lo que habia el principio
    
        case "DERECHA":
            nuevo.ladrones += estado.tablero[-1]
            nuevo.banca += estado.tablero[-2] #estado.tablero[estado.N - 2]
            nuevo.tablero.pop(estado.N - 1)
            nuevo.tablero.pop(estado.N - 2)

    nuevo.N -= 2
    return nuevo

def estadoInicial() -> tEstado:
    inicial = [4, 3, 2, 5, 7, 1, 8, 6]
    return tEstado(inicial) #le paso la estructura tEstado creada con la lista inicial completa


