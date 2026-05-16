from estructuras.lista_enlazada import ListaEnlazada

_LINEAS_GANADORAS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   
    (0, 4, 8), (2, 4, 6),              
)


class Tablero:

    VACIO = " "

    def __init__(self, desde_cadena=None):
        self.celdas = ListaEnlazada()
        if desde_cadena is None:
            for _ in range(9):
                self.celdas.agregar(Tablero.VACIO)
        else:
            if len(desde_cadena) != 9:
                raise ValueError("La cadena de tablero debe tener 9 caracteres")
            for c in desde_cadena:
                self.celdas.agregar(c)

    def obtener(self, pos):
        return self.celdas.obtener(pos)

    def colocar(self, pos, simbolo):
        if self.celdas.obtener(pos) == Tablero.VACIO:
            self.celdas.establecer(pos, simbolo)
            return True
        return False

    def disponible(self, pos):
        return self.celdas.obtener(pos) == Tablero.VACIO

    def lleno(self):
        for v in self.celdas:
            if v == Tablero.VACIO:
                return False
        return True

    def ganador(self):
        for tripleta in _LINEAS_GANADORAS:
            a, b, c = tripleta
            va = self.celdas.obtener(a)
            vb = self.celdas.obtener(b)
            vc = self.celdas.obtener(c)
            if va == vb == vc and va != Tablero.VACIO:
                return va, tripleta
        return None, None

    def turno(self):
        x_count = 0
        o_count = 0
        for c in self.celdas:
            if c == "X":
                x_count += 1
            elif c == "O":
                o_count += 1
        return "X" if x_count == o_count else "O"

    def movimientos_disponibles(self):
        movs = ListaEnlazada()
        i = 0
        for v in self.celdas:
            if v == Tablero.VACIO:
                movs.agregar(i)
            i += 1
        return movs

    def como_cadena(self):
        partes = ListaEnlazada()
        for c in self.celdas:
            partes.agregar(c)
        s = ""
        for c in partes:
            s += c
        return s

    def clonar(self):
        return Tablero(desde_cadena=self.como_cadena())

    def visualizacion_texto(self):
        c = ListaEnlazada()
        for v in self.celdas:
            c.agregar(v)
        return (
            f" {c.obtener(0)} | {c.obtener(1)} | {c.obtener(2)} \n"
            f"---+---+---\n"
            f" {c.obtener(3)} | {c.obtener(4)} | {c.obtener(5)} \n"
            f"---+---+---\n"
            f" {c.obtener(6)} | {c.obtener(7)} | {c.obtener(8)} \n"
        )

    def __repr__(self):
        return f"Tablero('{self.como_cadena()}')"
