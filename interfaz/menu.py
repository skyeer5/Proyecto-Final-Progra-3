import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime
import os

from estructuras.arbol_estados import ArbolEstados
from estructuras.arbol_b import ArbolB, RegistroPartida
from juego.aprendizaje import Aprendizaje
from interfaz.ventana_juego import VentanaJuego
from interfaz.ventana_historial import VentanaHistorial
from visualizacion.grafico import GeneradorGrafico


COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#282c34"
COLOR_TEXTO = "#abb2bf"
COLOR_TITULO = "#ffffff"
COLOR_BOTON = "#3e4451"
COLOR_BOTON_HOVER = "#4b5363"
COLOR_ACENTO = "#98c379"
COLOR_X = "#e06c75"
COLOR_O = "#61afef"
COLOR_AMARILLO = "#e5c07b"


INTEGRANTES = (
    ("Angela Paola García Azañón", "Carnet 9490-24-11686", "100%"),
    ("Robinson Daniel Dávila Alba", "Carnet 9490-24-3939", "100%"),
    ("Ingrid Elena Damián Chial ", "Carnet 9490-24-4375", "100%"),
    ("José Daniel Pineda Vicente", "Carnet 9490-24-4996", "100%"),
)


class AplicacionTotito:

    GRADO_BTREE_DEFECTO = 3

    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Totito · Tic-Tac-Toe con Aprendizaje Supervisado")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.geometry("560x720")
        self.raiz.resizable(False, False)

        # ---- Construcción de estructuras ----
        self._panel_carga_visible = False
        self._mostrar_carga()
        self.raiz.update_idletasks()

        self.arbol_estados = ArbolEstados()
        self.aprendizaje = Aprendizaje(self.arbol_estados)

        self.grado_btree = AplicacionTotito.GRADO_BTREE_DEFECTO
        self.arbol_historial = ArbolB(grado=self.grado_btree)

        self.contador_partidas = 0

        self._ocultar_carga()
        self._construir_ui()

    def siguiente_id_partida(self):
        self.contador_partidas += 1
        return self.contador_partidas

    # ---------- Construccion del UI ----------

    def _mostrar_carga(self):
        self.lbl_carga = tk.Label(
            self.raiz,
            text="Construyendo árbol con todos los movimientos posibles…\n(5478 estados)",
            font=("Helvetica", 12, "italic"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO,
        )
        self.lbl_carga.pack(expand=True, pady=200)
        self._panel_carga_visible = True

    def _ocultar_carga(self):
        if self._panel_carga_visible:
            self.lbl_carga.destroy()
            self._panel_carga_visible = False

    def _construir_ui(self):
        titulo = tk.Label(
            self.raiz, text="TOTITO",
            font=("Helvetica", 28, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        )
        titulo.pack(pady=(20, 0))
        subtitulo = tk.Label(
            self.raiz, text="Tic-Tac-Toe con Aprendizaje Supervisado",
            font=("Helvetica", 11, "italic"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        subtitulo.pack(pady=(0, 16))

        panel = tk.Frame(self.raiz, bg=COLOR_PANEL, padx=14, pady=10)
        panel.pack(padx=24, pady=4, fill=tk.X)
        tk.Label(panel, text="ESTADO ACTUAL",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_PANEL, fg=COLOR_AMARILLO).pack(anchor="w")
        self.lbl_stats = tk.Label(
            panel, text="", justify="left",
            font=("Consolas", 10),
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
        )
        self.lbl_stats.pack(anchor="w", pady=(4, 0))

        contenedor_botones = tk.Frame(self.raiz, bg=COLOR_FONDO)
        contenedor_botones.pack(padx=24, pady=14, fill=tk.X)

        opciones = (
            ("🎮  Entrenamiento Manual (jugar partida)", self._accion_manual, COLOR_ACENTO),
            ("⚙️  Entrenamiento Automático (simular partidas)", self._accion_automatico, COLOR_O),
            ("📜  Visualizar Historial (Árbol B)", self._accion_historial, COLOR_AMARILLO),
            ("📈  Iteraciones para alcanzar victoria", self._accion_iteraciones, COLOR_AMARILLO),
            ("🌳  Visualizar Árbol B del historial", self._accion_visualizar_btree, COLOR_O),
            ("🧹  Limpiar estructura de datos", self._accion_limpiar, COLOR_X),
            ("👥  Integrantes del grupo", self._accion_integrantes, COLOR_TEXTO),
        )
        for texto, comando, color in opciones:
            self._crear_boton(contenedor_botones, texto, comando, color)

        pie = tk.Label(
            self.raiz,
            text="Programación III · Universidad Mariano Gálvez",
            font=("Helvetica", 8, "italic"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        pie.pack(side=tk.BOTTOM, pady=10)

        self.refrescar_panel_estadisticas()

    def _crear_boton(self, padre, texto, comando, color_acento):
        marco = tk.Frame(padre, bg=COLOR_FONDO, pady=4)
        marco.pack(fill=tk.X)
        barra = tk.Frame(marco, bg=color_acento, width=4)
        barra.pack(side=tk.LEFT, fill=tk.Y)
        btn = tk.Button(
            marco, text=texto, command=comando,
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TITULO,
            font=("Helvetica", 11, "bold"),
            anchor="w", padx=18, pady=10,
            relief="flat", cursor="hand2",
        )
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def refrescar_panel_estadisticas(self):
        a = self.aprendizaje
        if a.iteraciones_para_primera_victoria is None:
            primera = "(aún sin victoria)"
        else:
            primera = f"{a.iteraciones_para_primera_victoria}"
        texto = (
            f"Partidas jugadas:      {self.contador_partidas}\n"
            f"Iteraciones aprend.:   {a.iteraciones_acumuladas}\n"
            f"  · Victorias sistema: {a.victorias_sistema}\n"
            f"  · Empates:           {a.empates}\n"
            f"  · Derrotas sistema:  {a.derrotas_sistema}\n"
            f"Iter. 1ra victoria:    {primera}\n"
            f"Árbol estados:         {self.arbol_estados.total_nodos} nodos\n"
            f"Árbol B (t={self.grado_btree}):       "
            f"{self.arbol_historial.cantidad()} registros, "
            f"{self.arbol_historial.total_nodos} nodos"
        )
        self.lbl_stats.config(text=texto)

    # ---------- Acciones del menu ----------

    def _accion_manual(self):
        VentanaJuego(self.raiz, self)

    def _accion_automatico(self):
        n = simpledialog.askinteger(
            "Entrenamiento automático",
            "¿Cuántas partidas desea simular?",
            parent=self.raiz, minvalue=1, maxvalue=10000,
        )
        if not n:
            return

        ventana_prog = tk.Toplevel(self.raiz)
        ventana_prog.title("Simulando…")
        ventana_prog.configure(bg=COLOR_FONDO)
        ventana_prog.geometry("360x130")
        ventana_prog.resizable(False, False)
        tk.Label(
            ventana_prog, text=f"Simulando {n} partidas…",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO,
        ).pack(pady=20)
        lbl_p = tk.Label(
            ventana_prog, text="0/0",
            font=("Helvetica", 10),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        lbl_p.pack()
        ventana_prog.update_idletasks()

        progreso = [0]
        def cb(partida):
            progreso[0] += 1
            reg = RegistroPartida(
                id_partida=partida.id_partida,
                resumen=partida.generar_resumen(),
                tablero_final=partida.tablero.como_cadena(),
                ganador=partida.resultado,
                fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                movimientos_realizados=partida.trayectoria.tamanio,
                modo="AUTOMATICO",
            )
            self.arbol_historial.insertar(reg)

            try:
                GeneradorGrafico.visualizar_partida(partida)
            except Exception:
                pass

            if progreso[0] % max(1, n // 20) == 0 or progreso[0] == n:
                lbl_p.config(text=f"{progreso[0]}/{n}")
                ventana_prog.update()

        reporte = self.aprendizaje.entrenamiento_automatico(
            n, self.siguiente_id_partida, callback_partida=cb,
        )
        ventana_prog.destroy()

        self._mostrar_reporte_simulacion(reporte, n)
        self.refrescar_panel_estadisticas()

    def _mostrar_reporte_simulacion(self, reporte, n_solicitado):
        v = tk.Toplevel(self.raiz)
        v.title("Reporte de entrenamiento automático")
        v.configure(bg=COLOR_FONDO)
        v.geometry("700x560")
        tk.Label(
            v, text=f"Reporte de simulación · {n_solicitado} partidas",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        ).pack(pady=(12, 4))

        resumen = (
            f"Iteraciones realizadas:     {reporte.iteraciones_realizadas}\n"
            f"Victorias del sistema:      {reporte.victorias_sistema} "
            f"({reporte.victorias_sistema*100/max(1,reporte.iteraciones_realizadas):.1f}%)\n"
            f"Empates:                    {reporte.empates}\n"
            f"Derrotas del sistema:       {reporte.derrotas_sistema}\n"
            f"Cambios de peso totales:    {reporte.cambios_pesos_totales}\n"
            f"Peso promedio inicial:      {reporte.peso_promedio_inicial:.4f}\n"
            f"Peso promedio final:        {reporte.peso_promedio_final:.4f}\n"
            f"Δ peso promedio (estrategia): {reporte.peso_promedio_final - reporte.peso_promedio_inicial:+.4f}\n"
        )
        tk.Label(
            v, text=resumen, justify="left", anchor="w",
            font=("Consolas", 10),
            bg=COLOR_PANEL, fg=COLOR_TEXTO, padx=12, pady=10,
        ).pack(padx=18, pady=6, fill=tk.X)

        tk.Label(
            v, text="Listado de partidas simuladas (id · resultado):",
            font=("Helvetica", 10, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        ).pack(anchor="w", padx=20, pady=(8, 2))

        st = scrolledtext.ScrolledText(
            v, height=14, font=("Consolas", 9),
            bg=COLOR_PANEL, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
        )
        st.pack(padx=18, pady=6, fill=tk.BOTH, expand=True)

        for elem in reporte.partidas:
            id_p, res, _ = elem
            etiqueta = ("VICTORIA" if res == "O"
                        else "EMPATE  " if res == "EMPATE"
                        else "DERROTA ")
            st.insert(tk.END, f"#{id_p:04d}  {etiqueta}  ganador={res}\n")
        st.config(state=tk.DISABLED)

        tk.Button(
            v, text="Cerrar", command=v.destroy,
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_HOVER,
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(pady=10)

    def _accion_historial(self):
        VentanaHistorial(self.raiz, self)

    def _accion_iteraciones(self):
        a = self.aprendizaje
        if a.iteraciones_para_primera_victoria is None:
            mensaje = (
                "El sistema aún no ha conseguido una victoria.\n\n"
                "Realice más partidas (manuales o automáticas) "
                "para que el aprendizaje progrese."
            )
        else:
            mensaje = (
                f"Iteraciones realizadas hasta la primera victoria del sistema:\n"
                f"    {a.iteraciones_para_primera_victoria}\n\n"
                f"Total de iteraciones acumuladas: {a.iteraciones_acumuladas}\n"
                f"Victorias totales del sistema:   {a.victorias_sistema}\n"
                f"Tasa de victoria actual:         "
                f"{a.victorias_sistema*100/max(1,a.iteraciones_acumuladas):.1f}%"
            )
        messagebox.showinfo("Iteraciones de aprendizaje", mensaje, parent=self.raiz)

    def _accion_visualizar_btree(self):
        if self.arbol_historial.cantidad() == 0:
            messagebox.showinfo(
                "Árbol B vacío",
                "Aún no hay partidas registradas. Juegue o simule algunas primero.",
                parent=self.raiz,
            )
            return
        ruta = GeneradorGrafico.visualizar_arbol_b(self.arbol_historial)
        messagebox.showinfo(
            "Visualización generada",
            f"Visualización del árbol B guardada en:\n{ruta}",
            parent=self.raiz,
        )

        import subprocess, sys
        try:
            if sys.platform.startswith("win"):
                os.startfile(ruta)  
            elif sys.platform == "darwin":
                subprocess.Popen(["open", ruta])
            else:
                subprocess.Popen(["xdg-open", ruta])
        except Exception:
            pass

    def _accion_limpiar(self):
        if not messagebox.askyesno(
            "Confirmar reinicio",
            "Esto eliminará TODO el aprendizaje, el historial y el contador "
            "de partidas. ¿Continuar?",
            parent=self.raiz,
        ):
            return
        nuevo_grado = simpledialog.askinteger(
            "Grado del árbol B",
            f"Grado mínimo t del nuevo árbol B (actual: {self.grado_btree}). Mínimo 2.",
            parent=self.raiz, minvalue=2, maxvalue=20,
            initialvalue=self.grado_btree,
        )
        if nuevo_grado is None:
            return

        self.aprendizaje.reiniciar()
        self.grado_btree = nuevo_grado
        self.arbol_historial = ArbolB(grado=self.grado_btree)
        self.contador_partidas = 0
        try:
            for archivo in os.listdir("visualizaciones"):
                if archivo.startswith("partida_") or archivo.startswith("arbol_b_"):
                    os.remove(os.path.join("visualizaciones", archivo))
        except FileNotFoundError:
            pass
        self.refrescar_panel_estadisticas()
        messagebox.showinfo(
            "Estructura reiniciada",
            f"Se reinició todo el sistema.\nNuevo grado del árbol B: t={nuevo_grado}",
            parent=self.raiz,
        )

    def _accion_integrantes(self):
        v = tk.Toplevel(self.raiz)
        v.title("Integrantes del grupo")
        v.configure(bg=COLOR_FONDO)
        v.geometry("480x340")
        tk.Label(
            v, text="Integrantes del grupo",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        ).pack(pady=(16, 4))
        tk.Label(
            v, text="Programación III · Sede Naranjo",
            font=("Helvetica", 10, "italic"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(0, 14))

        marco = tk.Frame(v, bg=COLOR_PANEL, padx=20, pady=14)
        marco.pack(padx=24, pady=4, fill=tk.X)
        for nombre, carnet, seccion in INTEGRANTES:
            fila = tk.Frame(marco, bg=COLOR_PANEL)
            fila.pack(fill=tk.X, pady=4)
            tk.Label(fila, text=f"• {nombre}",
                     font=("Helvetica", 11, "bold"),
                     bg=COLOR_PANEL, fg=COLOR_TITULO, anchor="w").pack(anchor="w")
            tk.Label(fila, text=f"   {carnet}   ·   {seccion}",
                     font=("Helvetica", 9),
                     bg=COLOR_PANEL, fg=COLOR_TEXTO, anchor="w").pack(anchor="w")

        tk.Button(
            v, text="Cerrar", command=v.destroy,
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_HOVER,
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(pady=14)

    # ---------- Bucle principal ----------

    def iniciar(self):
        self.raiz.mainloop()
