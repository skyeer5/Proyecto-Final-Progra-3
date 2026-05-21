import random

from estructuras.lista_enlazada import ListaEnlazada
from estructuras.tablero import Tablero
from juego.logica import Partida


class ResultadoSimulacion:
    def __init__(self):
        self.partidas = ListaEnlazada()
        self.victorias_sistema = 0
        self.derrotas_sistema = 0
        self.empates = 0
        self.iteraciones_realizadas = 0
        self.cambios_pesos_totales = 0
        self.peso_promedio_inicial = 0.0
        self.peso_promedio_final = 0.0


class Aprendizaje:
    INCREMENTO_VICTORIA = 0.50
    DECREMENTO_DERROTA = 0.30
    AJUSTE_EMPATE = 0.05
    PESO_MINIMO = 0.05

    def __init__(self, arbol_estados):
        self.arbol = arbol_estados
        self.iteraciones_acumuladas = 0
        self.iteraciones_para_primera_victoria = None
        self.victorias_sistema = 0
        self.derrotas_sistema = 0
        self.empates = 0

    # ---------- Selección de movimiento ----------

    def elegir_movimiento(self, estado_str, explorar=False):
        nodo = self.arbol.obtener_estado(estado_str)
        if nodo is None or nodo.es_terminal:
            return None
        if explorar:
            return nodo.seleccionar_ponderado()
        return nodo.mejor_movimiento()

    def elegir_movimiento_aleatorio(self, estado_str):
        """Selección uniformemente aleatoria entre movimientos válidos."""
        nodo = self.arbol.obtener_estado(estado_str)
        if nodo is None or nodo.es_terminal:
            return None
        if nodo.movimientos.tamanio == 0:
            return None
        idx = random.randint(0, nodo.movimientos.tamanio - 1)
        return nodo.movimientos.obtener(idx)

    # ---------- Ajuste de pesos ----------

    def ajustar_pesos(self, trayectoria, resultado, simbolo_sistema):
        """Aplica refuerzo a los movimientos del sistema."""
        self.iteraciones_acumuladas += 1
        if resultado == simbolo_sistema:
            self.victorias_sistema += 1
            if self.iteraciones_para_primera_victoria is None:
                self.iteraciones_para_primera_victoria = self.iteraciones_acumuladas
        elif resultado == "EMPATE":
            self.empates += 1
        else:
            self.derrotas_sistema += 1

        cambios = 0
        for paso in trayectoria:
            if paso.simbolo != simbolo_sistema:
                continue
            paso.movimiento.veces_elegido += 1
            if resultado == simbolo_sistema:
                paso.movimiento.peso += self.INCREMENTO_VICTORIA
            elif resultado == "EMPATE":
                paso.movimiento.peso += self.AJUSTE_EMPATE
            else:
                paso.movimiento.peso -= self.DECREMENTO_DERROTA
                if paso.movimiento.peso < self.PESO_MINIMO:
                    paso.movimiento.peso = self.PESO_MINIMO
            paso.peso_despues = paso.movimiento.peso
            cambios += 1
        return cambios

    # ---------- Entrenamiento automático ----------

    def entrenamiento_automatico(self, n_partidas, generador_id, callback_partida=None):
        reporte = ResultadoSimulacion()

        # peso promedio antes
        suma_antes = 0.0
        n_aristas = 0
        for nodo in self.arbol.estados.valores():
            for m in nodo.movimientos:
                suma_antes += m.peso
                n_aristas += 1
        reporte.peso_promedio_inicial = (suma_antes / n_aristas) if n_aristas else 0.0

        for _ in range(n_partidas):
            id_p = generador_id()
            partida = Partida(
                id_partida=id_p,
                simbolo_jugador="X",
                simbolo_sistema="O",
                modo="AUTOMATICO",
            )
            while not partida.terminada:
                estado = partida.tablero.como_cadena()
                if partida.turno_actual == partida.simbolo_sistema:
                    mov = self.elegir_movimiento(estado, explorar=True)
                else:
                    mov = self.elegir_movimiento_aleatorio(estado)
                if mov is None:
                    break
                partida.aplicar_movimiento(mov, partida.turno_actual)

            cambios = self.ajustar_pesos(
                partida.trayectoria,
                partida.resultado,
                partida.simbolo_sistema,
            )
            reporte.cambios_pesos_totales += cambios
            reporte.iteraciones_realizadas += 1

            if partida.resultado == partida.simbolo_sistema:
                reporte.victorias_sistema += 1
            elif partida.resultado == "EMPATE":
                reporte.empates += 1
            else:
                reporte.derrotas_sistema += 1

            reporte.partidas.agregar((id_p, partida.resultado, partida))

            if callback_partida is not None:
                callback_partida(partida)

        # peso promedio después
        suma_desp = 0.0
        n_aristas = 0
        for nodo in self.arbol.estados.valores():
            for m in nodo.movimientos:
                suma_desp += m.peso
                n_aristas += 1
        reporte.peso_promedio_final = (suma_desp / n_aristas) if n_aristas else 0.0

        return reporte

    # ---------- Reinicio ----------

    def reiniciar(self):
        self.arbol.reiniciar_pesos()
        self.iteraciones_acumuladas = 0
        self.iteraciones_para_primera_victoria = None
        self.victorias_sistema = 0
        self.derrotas_sistema = 0
        self.empates = 0
