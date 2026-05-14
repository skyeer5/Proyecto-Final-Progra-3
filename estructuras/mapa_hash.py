from estructuras.lista_enlazada import ListaEnlazada


class _EntradaHash:
    __slots__ = ("clave", "valor")

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor


class MapaHash:

    def __init__(self, capacidad=8192):
        self.capacidad = capacidad
        self.cubetas = ListaEnlazada()
        for _ in range(capacidad):
            self.cubetas.agregar(ListaEnlazada())
        self.tamanio = 0

    def _hash(self, clave):
        h = 0
        for c in str(clave):
            h = (h * 31 + ord(c)) & 0x7FFFFFFF
        return h % self.capacidad

    def insertar(self, clave, valor):
        indice = self._hash(clave)
        cubeta = self.cubetas.obtener(indice)
        for entrada in cubeta:
            if entrada.clave == clave:
                entrada.valor = valor
                return
        cubeta.agregar(_EntradaHash(clave, valor))
        self.tamanio += 1

    def obtener(self, clave):
        indice = self._hash(clave)
        cubeta = self.cubetas.obtener(indice)
        for entrada in cubeta:
            if entrada.clave == clave:
                return entrada.valor
        return None

    def contiene(self, clave):
        indice = self._hash(clave)
        cubeta = self.cubetas.obtener(indice)
        for entrada in cubeta:
            if entrada.clave == clave:
                return True
        return False

    def valores(self):
        for cubeta in self.cubetas:
            for entrada in cubeta:
                yield entrada.valor

    def __len__(self):
        return self.tamanio
