from __future__ import annotations
from NPuzle_Alum import *


@dataclass
class Nodo:
    estado: tEstado
    operador: str
    costeCamino: int
    profundidad: int
    valHeuristica: int
    padre: Nodo
    modo: str = "voraz"

    def __str__(self) -> str:
        return f'{"- " * 10}\n{self.estado.tablero}, Operador: {operadores[self.operador]}, Heu:{self.valHeuristica}\n{"- " * 10}'

    def hash(self) -> str:
        return self.estado.crearHash()
    
    def __lt__(self, nodo) -> bool:
        if self.modo == "voraz":
            return self.valHeuristica < nodo.valHeuristica
        else:
            return self.valHeuristica + self.costeCamino < nodo.valHeuristica + nodo.costeCamino

def nodoInicial() -> Nodo:
    return Nodo(estadoInicial(), "0", 0, 0, 0, None)


def CosteHeu(estado) -> int :
    obj = estadoObjetivo()
    piezasmal = 0
    for i in range(0, estado.N):
        for j in range(0, estado.N):
            if estado.tablero[i, j] != 0:
                piezasmal += estado.tablero[i,j] != obj.tablero[i, j]
                # piezasmal = max(estado.tablero != objetivo.tablero).sum() - 1, 0) es mejor la otra
    return piezasmal

def Manhattan(estado) -> int :
    obj = estadoObjetivo()
    coste = 0
    for ficha in range(1, 8):
        f, c = np.where(estado.tablero == ficha)
        f_obj, c_obj = np.where(obj.tablero == ficha)
        coste += abs(f_obj - f) + abs(c_obj -  c)
    return coste

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

def expandirH(nodo, tipo) -> list:
    nodos = []
    for op in operadores:
        if(esValido(op, nodo.estado)):
            nuevo = aplicaOperador(op, nodo.estado)
            if tipo == "M":
                nodos.append(
                    Nodo(
                    nuevo,
                    op,
                    nodo.costeCamino + coste(op, nuevo),
                    nodo.profundidad + 1,
                    Manhattan(nodo.estado),
                    nodo
                    )
                )
            else:
                nodos.append(
                    Nodo(
                    nuevo,
                    op,
                    nodo.costeCamino + coste(op, nuevo),
                    nodo.profundidad + 1,
                    CosteHeu(nodo.estado),
                    nodo
                    )
                )
            
    return nodos

def expandir(nodo) -> list:
    nodos = []
    for op in operadores:
        if esValido(op, nodo.estado):
            nuevo = aplicaOperador(op, nodo.estado)
            nodos.append(
                Nodo(
                    nuevo,
                    op,
                    nodo.costeCamino + coste(op, nuevo),
                    nodo.profundidad + 1, 
                    0, 
                    nodo,
                )
            )
    return nodos


def BusquedaAnchura() -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {} # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    
    while not objetivo and len(abiertos) > 0:
        actual = abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and  actual.hash() not in cerrados.keys():
            sucesores = expandir(actual)
            abiertos = abiertos + sucesores
        cerrados [actual.hash()] = 0    # Hasta heuristica le puedo poner el valor que yo quiera
    if objetivo:
        dispSolucion(actual)
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

def BusquedaHeuristica(modobusq, tipo) -> bool:
    objetivo = False
    raiz = nodoInicial()
    raiz.modo = modobusq
    f_eval = 0
    abiertos = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    
    while not objetivo and len(abiertos) != 0:
        actual = abiertos[0]
        if modobusq == "Voraz":
            f_eval = actual.valHeuristica
        else:
            f_eval = actual.valHeuristica + actual.costeCamino
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if (not objetivo and actual.hash() not in cerrados) or (actual.hash() in cerrados.keys() and f_eval < cerrados [actual.hash()]): #esto último solo funciona en A*
            sucesores = expandirH(actual, tipo)
            abiertos += sucesores
            abiertos.sort() #sort modifica y no devuelve nada, sorted modifica y devuelve
        cerrados[actual.hash()] = f_eval

    if objetivo:
        dispSolucion(actual)  
    else:
        print("No se ha encontrado solución")

    return objetivo

def BusquedaProfundidad() -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    while not objetivo and len(abiertos)>0:
        actual = abiertos[0]
        abiertos.pop(0)      
        objetivo = testObjetivo(actual.estado)
        if not objetivo and  actual.hash() not in cerrados.keys():
            sucesores = expandir(actual)
            abiertos = sucesores + abiertos
        cerrados[actual.hash()] = None     #Hash se hace para que los valores sean inmutables
    if objetivo:
        dispSolucion(actual)
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

#cerrados: nodos ya visitados(ya están en el diccionario y no expandiria)->usamos _ in _ keys()
def anchuracontrolestados() -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    while not objetivo and len(abiertos)>0:
        actual = abiertos[0] #nodo actual
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and  actual.hash() not in cerrados.keys():   #el nodo en el que estamos no está en el diccionario de nodos cerrados
            sucesores = expandir(actual)
            abiertos = abiertos + sucesores
        cerrados[actual.hash()] = None            #todos los hashes tienen el mismo numero, es para guardar el nodo actual en cerrados ya que esta visto
    if objetivo:
        dispSolucion(actual)  # Completar
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

# Añadir limites
def profundidadcontrolestados() -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    while not objetivo and len(abiertos)>0:
        actual = abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and actual.hash() not in cerrados.keys():   #el nodo en el que estamos no está en el diccionario de nodos cerrados
            sucesores = expandir(actual)
            abiertos = sucesores + abiertos
        cerrados[actual.hash()] = None #todos los hashes tienen el mismo numero, es para guardar el nodo actual en cerrados ya que esta visto. usamos como clave que no podamos modificar(el hash)
    if objetivo:
        dispSolucion(actual)  # Completar
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo

#busqueda en profundidad limitada, se pone un limite de profundidad. cuando la lista de abiertos quede vacia, termina( como si fuese una búsqueda por niveles)
def busquedaprofundidadlim(limite) -> bool:
    objetivo = False
    raiz = nodoInicial()
    abiertos = []
    sucesores = []
    cerrados = {}  # Cerrados es un diccionario para que funcione como una tabla hash
    abiertos.append(raiz)
    while not objetivo and len(abiertos) > 0 : #la profundidad del nodo no sea igual al limite puesto
        actual = abiertos[0]
        abiertos.pop(0)
        objetivo = testObjetivo(actual.estado)
        if not objetivo and actual.hash() not in cerrados.keys() and actual.profundidad <=limite:   #el nodo en el que estamos no está en el diccionario de nodos cerrados
            sucesores = expandir(actual)
            abiertos = sucesores + abiertos
            cerrados[actual.hash()] = None #todos los hashes tienen el mismo numero, es para guardar el nodo actual en cerrados ya que esta visto
    
    if objetivo:
        dispSolucion(actual)  # Completar
    elif not objetivo:
        print("No se ha encontrado solución")

    return objetivo