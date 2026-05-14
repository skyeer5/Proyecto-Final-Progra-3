from estructuras.lista_enlazada import Nodo

class Cola:

    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0

    def encolar(self, valor):
        nuevo = Nodo(valor)
        if self.frente is None:
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            nuevo.anterior = self.final
            self.final = nuevo
        self.tamanio += 1

    def desencolar(self):
        if self.frente is None:
            return None
        valor = self.frente.valor
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        else:
            self.frente.anterior = None
        self.tamanio -= 1
        return valor

    def vacia(self):
        return self.frente is None

    def __len__(self):
        return self.tamanio
