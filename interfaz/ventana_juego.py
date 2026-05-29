import tkinter as tk
from tkinter import messagebox
import datetime
import os

from juego.logica import Partida
from estructuras.arbol_b import RegistroPartida
from visualizacion.grafico import GeneradorGrafico


COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#282c34"
COLOR_TEXTO = "#abb2bf"
COLOR_TITULO = "#ffffff"
COLOR_X = "#e06c75"
COLOR_O = "#61afef"
COLOR_LINEA = "#fff5b8"
COLOR_BOTON = "#3e4451"
COLOR_BOTON_HOVER = "#4b5363"
COLOR_ACENTO = "#98c379"


class VentanaJuego(tk.Toplevel):
    def __init__(self, master, aplicacion):
        super().__init__(master)
        self.aplicacion = aplicacion
        self.title("Totito · Partida en curso")
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        id_p = self.aplicacion.siguiente_id_partida()
        self.partida = Partida(
            id_partida=id_p,
            simbolo_jugador="X",
            simbolo_sistema="O",
            modo="MANUAL",
        )
        self._procesando = False 

        self._construir_ui()
        self._actualizar_estado_texto("Tu turno (X)")

    # ---------- Construccion del UI ----------

    def _construir_ui(self):
        contenedor = tk.Frame(self, bg=COLOR_FONDO, padx=20, pady=20)
        contenedor.pack()

        encabezado = tk.Label(
            contenedor,
            text=f"Partida #{self.partida.id_partida}",
            font=("Helvetica", 18, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        )
        encabezado.pack(pady=(0, 4))

        sub = tk.Label(
            contenedor,
            text="Tú (X) vs Sistema (O)",
            font=("Helvetica", 11),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        sub.pack(pady=(0, 12))

        marco_tablero = tk.Frame(contenedor, bg=COLOR_PANEL, padx=6, pady=6)
        marco_tablero.pack()
        self.botones = []
        for i in range(9):
            fila = i // 3
            col = i % 3
            btn = tk.Button(
                marco_tablero,
                text=" ",
                font=("Helvetica", 30, "bold"),
                width=3, height=1,
                bg=COLOR_PANEL, fg=COLOR_TEXTO,
                activebackground=COLOR_BOTON_HOVER,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda pos=i: self._click_celda(pos),
            )
            btn.grid(row=fila, column=col, padx=3, pady=3, ipadx=10, ipady=8)
            self.botones.append(btn)

        self.lbl_estado = tk.Label(
            contenedor,
            text="",
            font=("Helvetica", 12, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO,
        )
        self.lbl_estado.pack(pady=(14, 4))

        self.lbl_aprende = tk.Label(
            contenedor,
            text="El sistema aprenderá al terminar la partida.",
            font=("Helvetica", 9, "italic"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        self.lbl_aprende.pack(pady=(0, 8))

        barra = tk.Frame(contenedor, bg=COLOR_FONDO)
        barra.pack(pady=(8, 0))

        self.btn_cerrar = tk.Button(
            barra, text="Cerrar",
            command=self._al_cerrar,
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TITULO,
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=18, pady=6, cursor="hand2",
        )
        self.btn_cerrar.pack(side=tk.LEFT, padx=4)

    # ---------- Eventos ----------

    def _click_celda(self, pos):
        if self._procesando or self.partida.terminada:
            return
        if not self.partida.tablero.disponible(pos):
            return
        estado = self.partida.tablero.como_cadena()
        nodo = self.aplicacion.arbol_estados.obtener_estado(estado)
        mov = nodo.encontrar_movimiento(pos) if nodo else None
        if mov is None:
            return
        self.partida.aplicar_movimiento(mov, "X")
        self._refrescar_tablero()
        if self.partida.terminada:
            self._finalizar()
            return
        self._procesando = True
        self._actualizar_estado_texto("Pensando…")
        self.after(450, self._turno_sistema)

    def _turno_sistema(self):
        estado = self.partida.tablero.como_cadena()
        mov = self.aplicacion.aprendizaje.elegir_movimiento(estado, explorar=False)
        if mov is None:
            mov = self.aplicacion.aprendizaje.elegir_movimiento_aleatorio(estado)
        if mov is not None:
            self.partida.aplicar_movimiento(mov, "O")
        self._refrescar_tablero()
        self._procesando = False
        if self.partida.terminada:
            self._finalizar()
        else:
            self._actualizar_estado_texto("Tu turno (X)")

    # ---------- Render ----------

    def _refrescar_tablero(self):
        estado = self.partida.tablero.como_cadena()
        for i in range(9):
            c = estado[i]
            btn = self.botones[i]
            if c == "X":
                btn.config(text="X", fg=COLOR_X)
            elif c == "O":
                btn.config(text="O", fg=COLOR_O)
            else:
                btn.config(text=" ", fg=COLOR_TEXTO)
        if self.partida.linea_ganadora is not None:
            for idx in self.partida.linea_ganadora:
                self.botones[idx].config(bg=COLOR_LINEA, fg="#000000")

    def _actualizar_estado_texto(self, texto):
        self.lbl_estado.config(text=texto)

    # ---------- Cierre / cierre por victoria ----------

    def _finalizar(self):
        self.aplicacion.aprendizaje.ajustar_pesos(
            self.partida.trayectoria,
            self.partida.resultado,
            self.partida.simbolo_sistema,
        )
        reg = RegistroPartida(
            id_partida=self.partida.id_partida,
            resumen=self.partida.generar_resumen(),
            tablero_final=self.partida.tablero.como_cadena(),
            ganador=self.partida.resultado,
            fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            movimientos_realizados=self.partida.trayectoria.tamanio,
            modo="MANUAL",
        )
        self.aplicacion.arbol_historial.insertar(reg)

        try:
            ruta = GeneradorGrafico.visualizar_partida(self.partida)
        except Exception as e:
            ruta = f"(error: {e})"

        if self.partida.resultado == self.partida.simbolo_sistema:
            titulo = "Ganó el sistema"
            mensaje = "El sistema (O) ha ganado esta partida."
        elif self.partida.resultado == "EMPATE":
            titulo = "Empate"
            mensaje = "La partida terminó en empate."
        else:
            titulo = "¡Ganaste!"
            mensaje = "Ganaste esta partida. El sistema penalizó sus jugadas."

        self._actualizar_estado_texto(titulo + " · pesos ajustados")
        self.lbl_aprende.config(
            text=f"Visualización guardada en: {ruta}",
            fg=COLOR_ACENTO,
        )

        messagebox.showinfo(
            "Fin de partida",
            f"{mensaje}\n\n"
            f"Partidas jugadas: {self.aplicacion.contador_partidas}\n"
            f"Visualización: {ruta}",
            parent=self,
        )
        self.aplicacion.refrescar_panel_estadisticas()

    def _al_cerrar(self):
        self.destroy()
