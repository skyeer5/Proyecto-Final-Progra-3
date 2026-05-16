import random

from estructuras.lista_enlazada import ListaEnlazada
from estructuras.cola import Cola
from estructuras.mapa_hash import MapaHash
from estructuras.tablero import Tablero


class MovimientoPonderado:

    __slots__ = ("posicion", "hijo", "peso", "veces_elegido")

    def __init__(self, posicion, hijo, peso=1.0):
        self.posicion = posicion
        self.hijo = hijo 
        self.peso = peso
        self.veces_elegido = 0


class NodoEstado:

    __slots__ = ("tablero", "movimientos", "es_terminal", "resultado_terminal", "profundidad")

    def __init__(self, cadena_tablero, profundidad=0):
        self.tablero = cadena_tablero          
        self.movimientos = ListaEnlazada()    
        self.es_terminal = False
        self.resultado_terminal = None         
        self.profundidad = profundidad

    def agregar_movimiento(self, posicion, hijo, peso=1.0):
        self.movimientos.agregar(MovimientoPonderado(posicion, hijo, peso))

    def encontrar_movimiento(self, posicion):
        for m in self.movimientos:
            if m.posicion == posicion:
                return m
        return None

    def mejor_movimiento(self):
        if self.movimientos.tamanio == 0:
            return None
        mejor_peso = float("-inf")
        empates = ListaEnlazada()
        for m in self.movimientos:
            if m.peso > mejor_peso:
                mejor_peso = m.peso
                empates.limpiar()
                empates.agregar(m)
            elif m.peso == mejor_peso:
                empates.agregar(m)
        idx = random.randint(0, empates.tamanio - 1)
        return empates.obtener(idx)

    def seleccionar_ponderado(self):
        if self.movimientos.tamanio == 0:
            return None
        suma_total = 0.0
        for m in self.movimientos:
            suma_total += max(m.peso, 0.001)
        r = random.uniform(0.0, suma_total)
        acumulado = 0.0
        for m in self.movimientos:
            acumulado += max(m.peso, 0.001)
            if r <= acumulado:
                return m
        return self.mejor_movimiento()


class ArbolEstados:

    def __init__(self):
        self.estados = MapaHash(capacidad=8192)
        self.raiz = None
        self.total_nodos = 0
        self.total_estados_terminales = 0
        self._construir()

    def _construir(self):
        tablero_inicial = " " * 9
        self.raiz = NodoEstado(tablero_inicial, profundidad=0)
        self.estados.insertar(tablero_inicial, self.raiz)
        self.total_nodos = 1

        cola = Cola()
        cola.encolar(self.raiz)

        while not cola.vacia():
            nodo = cola.desencolar()

            tablero_obj = Tablero(desde_cadena=nodo.tablero)
            gan, _ = tablero_obj.ganador()
            if gan is not None:
                nodo.es_terminal = True
                nodo.resultado_terminal = gan
                self.total_estados_terminales += 1
                continue
            if tablero_obj.lleno():
                nodo.es_terminal = True
                nodo.resultado_terminal = "EMPATE"
                self.total_estados_terminales += 1
                continue

            turno = tablero_obj.turno()
            for i in range(9):
                if nodo.tablero[i] == " ":
                    nuevo_str = nodo.tablero[:i] + turno + nodo.tablero[i + 1:]
                    hijo = self.estados.obtener(nuevo_str)
                    if hijo is None:
                        hijo = NodoEstado(nuevo_str, profundidad=nodo.profundidad + 1)
                        self.estados.insertar(nuevo_str, hijo)
                        self.total_nodos += 1
                        cola.encolar(hijo)
                    nodo.agregar_movimiento(i, hijo, peso=1.0)

    def obtener_estado(self, cadena):
        return self.estados.obtener(cadena)

    def reiniciar_pesos(self):
        for nodo in self.estados.valores():
            for m in nodo.movimientos:
                m.peso = 1.0
                m.veces_elegido = 0
