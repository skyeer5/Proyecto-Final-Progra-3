class Nodo:

    __slots__ = ("valor", "siguiente", "anterior")

    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None
        self.anterior = None


class ListaEnlazada:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0


    def agregar(self, valor):
        nuevo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.tamanio += 1

    def insertar(self, indice, valor):
        if indice < 0 or indice > self.tamanio:
            raise IndexError("Índice fuera de rango")
        if indice == self.tamanio:
            self.agregar(valor)
            return
        if indice == 0:
            nuevo = Nodo(valor)
            nuevo.siguiente = self.cabeza
            if self.cabeza is not None:
                self.cabeza.anterior = nuevo
            self.cabeza = nuevo
            if self.cola is None:
                self.cola = nuevo
            self.tamanio += 1
            return
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        nuevo = Nodo(valor)
        nuevo.anterior = actual.anterior
        nuevo.siguiente = actual
        actual.anterior.siguiente = nuevo
        actual.anterior = nuevo
        self.tamanio += 1


    def obtener(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        if indice < self.tamanio // 2:
            actual = self.cabeza
            for _ in range(indice):
                actual = actual.siguiente
        else:
            actual = self.cola
            for _ in range(self.tamanio - 1 - indice):
                actual = actual.anterior
        return actual.valor

    def establecer(self, indice, valor):
        if indice < 0 or indice >= self.tamanio:
            return False
        if indice < self.tamanio // 2:
            actual = self.cabeza
            for _ in range(indice):
                actual = actual.siguiente
        else:
            actual = self.cola
            for _ in range(self.tamanio - 1 - indice):
                actual = actual.anterior
        actual.valor = valor
        return True


    def eliminar_en(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        if actual.anterior is not None:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.cabeza = actual.siguiente
        if actual.siguiente is not None:
            actual.siguiente.anterior = actual.anterior
        else:
            self.cola = actual.anterior
        self.tamanio -= 1
        return actual.valor

    def limpiar(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0

    def vacia(self):
        return self.tamanio == 0

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self):
        return self.tamanio

    def __contains__(self, valor):
        for v in self:
            if v == valor:
                return True
        return False

    def __repr__(self):
        partes = []
        for v in self:
            partes.append(repr(v))
        return "ListaEnlazada([" + ", ".join(partes) + "])"
