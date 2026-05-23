from estructuras.lista_enlazada import ListaEnlazada


class RegistroPartida:
    __slots__ = ("id_partida", "resumen", "tablero_final", "ganador",
                 "fecha", "movimientos_realizados", "modo")

    def __init__(self, id_partida, resumen, tablero_final, ganador,
                 fecha, movimientos_realizados, modo):
        self.id_partida = id_partida
        self.resumen = resumen
        self.tablero_final = tablero_final     
        self.ganador = ganador                 
        self.fecha = fecha                     
        self.movimientos_realizados = movimientos_realizados
        self.modo = modo                      

    def __repr__(self):
        return (f"RegistroPartida(id={self.id_partida}, "
                f"ganador={self.ganador}, modo={self.modo})")


class NodoBTree:

    __slots__ = ("hoja", "claves", "hijos")

    def __init__(self, hoja=True):
        self.hoja = hoja
        self.claves = ListaEnlazada()   
        self.hijos = ListaEnlazada()   

    def num_claves(self):
        return self.claves.tamanio

    def num_hijos(self):
        return self.hijos.tamanio


class ArbolB:

    def __init__(self, grado=3):
        if grado < 2:
            raise ValueError("El grado mínimo del árbol B debe ser >= 2")
        self.grado = grado
        self.raiz = NodoBTree(hoja=True)
        self.total_registros = 0
        self.total_nodos = 1

    # ---------- Búsqueda ----------

    def buscar(self, id_partida, nodo=None):
        if nodo is None:
            nodo = self.raiz
        i = 0
        while i < nodo.num_claves() and id_partida > nodo.claves.obtener(i).id_partida:
            i += 1
        if i < nodo.num_claves() and nodo.claves.obtener(i).id_partida == id_partida:
            return nodo.claves.obtener(i)
        if nodo.hoja:
            return None
        return self.buscar(id_partida, nodo.hijos.obtener(i))

    # ---------- Inserción (CLRS) ----------

    def insertar(self, registro):
        raiz = self.raiz
        if raiz.num_claves() == 2 * self.grado - 1:
            nueva_raiz = NodoBTree(hoja=False)
            nueva_raiz.hijos.agregar(raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self.total_nodos += 1
            self._insertar_no_lleno(nueva_raiz, registro)
        else:
            self._insertar_no_lleno(raiz, registro)
        self.total_registros += 1

    def _insertar_no_lleno(self, nodo, registro):
        if nodo.hoja:
            i = nodo.num_claves() - 1
            indice_insertar = nodo.num_claves()
            j = 0
            while j < nodo.num_claves():
                if registro.id_partida < nodo.claves.obtener(j).id_partida:
                    indice_insertar = j
                    break
                j += 1
            nodo.claves.insertar(indice_insertar, registro)
        else:
            i = nodo.num_claves() - 1
            while i >= 0 and registro.id_partida < nodo.claves.obtener(i).id_partida:
                i -= 1
            i += 1
            hijo = nodo.hijos.obtener(i)
            if hijo.num_claves() == 2 * self.grado - 1:
                self._dividir_hijo(nodo, i)
                if registro.id_partida > nodo.claves.obtener(i).id_partida:
                    i += 1
            self._insertar_no_lleno(nodo.hijos.obtener(i), registro)

    def _dividir_hijo(self, padre, indice):
        t = self.grado
        hijo_lleno = padre.hijos.obtener(indice)
        nuevo = NodoBTree(hoja=hijo_lleno.hoja)
        self.total_nodos += 1

        mediana = hijo_lleno.claves.obtener(t - 1)

        for j in range(t, 2 * t - 1):
            nuevo.claves.agregar(hijo_lleno.claves.obtener(j))

        if not hijo_lleno.hoja:
            for j in range(t, 2 * t):
                nuevo.hijos.agregar(hijo_lleno.hijos.obtener(j))

        nuevas_claves = ListaEnlazada()
        for j in range(t - 1):
            nuevas_claves.agregar(hijo_lleno.claves.obtener(j))
        hijo_lleno.claves = nuevas_claves

        if not hijo_lleno.hoja:
            nuevos_hijos = ListaEnlazada()
            for j in range(t):
                nuevos_hijos.agregar(hijo_lleno.hijos.obtener(j))
            hijo_lleno.hijos = nuevos_hijos

        # Insertar mediana en padre y conectar nuevo hijo
        padre.claves.insertar(indice, mediana)
        padre.hijos.insertar(indice + 1, nuevo)

    # ---------- Recorridos ----------

    def recorrido_in_orden(self):
        acumulador = ListaEnlazada()
        self._inorden(self.raiz, acumulador)
        return acumulador

    def _inorden(self, nodo, acumulador):
        if nodo is None:
            return
        i = 0
        n_claves = nodo.num_claves()
        while i < n_claves:
            if not nodo.hoja:
                self._inorden(nodo.hijos.obtener(i), acumulador)
            acumulador.agregar(nodo.claves.obtener(i))
            i += 1
        if not nodo.hoja:
            self._inorden(nodo.hijos.obtener(n_claves), acumulador)

    def vaciar(self):
        self.raiz = NodoBTree(hoja=True)
        self.total_registros = 0
        self.total_nodos = 1

    def cantidad(self):
        return self.total_registros

    def estructura_visualizable(self):
        niveles = ListaEnlazada()
        if self.raiz is None or self.raiz.num_claves() == 0:
            return niveles
        nivel_actual = ListaEnlazada()
        nivel_actual.agregar(self.raiz)
        while nivel_actual.tamanio > 0:
            niveles.agregar(nivel_actual)
            siguiente = ListaEnlazada()
            for nodo in nivel_actual:
                if not nodo.hoja:
                    for hijo in nodo.hijos:
                        siguiente.agregar(hijo)
            nivel_actual = siguiente
        return niveles
