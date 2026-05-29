import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys


COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#282c34"
COLOR_TEXTO = "#abb2bf"
COLOR_TITULO = "#ffffff"
COLOR_BOTON = "#3e4451"
COLOR_BOTON_HOVER = "#4b5363"
COLOR_ACENTO = "#98c379"
COLOR_X = "#e06c75"
COLOR_O = "#61afef"


class VentanaHistorial(tk.Toplevel):
    def __init__(self, master, aplicacion):
        super().__init__(master)
        self.aplicacion = aplicacion
        self.title("Totito · Historial (Árbol B)")
        self.configure(bg=COLOR_FONDO)
        self.geometry("780x520")
        self._construir_ui()
        self._cargar_lista()

    def _construir_ui(self):
        cont = tk.Frame(self, bg=COLOR_FONDO, padx=16, pady=14)
        cont.pack(fill=tk.BOTH, expand=True)

        encabezado = tk.Frame(cont, bg=COLOR_FONDO)
        encabezado.pack(fill=tk.X)
        tk.Label(
            encabezado, text="Historial de Partidas",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO,
        ).pack(side=tk.LEFT)
        self.lbl_info = tk.Label(
            encabezado, text="",
            font=("Helvetica", 10),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        )
        self.lbl_info.pack(side=tk.RIGHT)

        cuerpo = tk.Frame(cont, bg=COLOR_FONDO)
        cuerpo.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Tabla
        marco_tabla = tk.Frame(cuerpo, bg=COLOR_PANEL, padx=6, pady=6)
        marco_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Hist.Treeview",
            background=COLOR_PANEL, foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL, rowheight=24,
            font=("Helvetica", 10),
        )
        style.configure(
            "Hist.Treeview.Heading",
            background=COLOR_BOTON, foreground=COLOR_TITULO,
            font=("Helvetica", 10, "bold"),
        )
        style.map("Hist.Treeview",
                  background=[("selected", COLOR_ACENTO)],
                  foreground=[("selected", "#000000")])

        cols = ("id", "ganador", "movs", "modo", "fecha")
        self.tabla = ttk.Treeview(
            marco_tabla, columns=cols, show="headings",
            style="Hist.Treeview", height=18,
        )
        for c, t, w in (("id", "ID", 60),
                        ("ganador", "Ganador", 90),
                        ("movs", "Movs.", 60),
                        ("modo", "Modo", 110),
                        ("fecha", "Fecha", 160)):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=w, anchor="center")
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        marco_detalle = tk.Frame(cuerpo, bg=COLOR_FONDO, padx=12)
        marco_detalle.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(marco_detalle, text="Detalle de partida",
                 font=("Helvetica", 12, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(anchor="w")
        self.lbl_detalle = tk.Label(
            marco_detalle, text="(seleccione una partida)",
            font=("Helvetica", 10), justify="left",
            bg=COLOR_FONDO, fg=COLOR_TEXTO, wraplength=240,
        )
        self.lbl_detalle.pack(anchor="w", pady=(6, 10))

        # Tablero final pintaoo
        tk.Label(marco_detalle, text="Tablero representativo:",
                 font=("Helvetica", 10, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
        marco_tab = tk.Frame(marco_detalle, bg=COLOR_PANEL, padx=4, pady=4)
        marco_tab.pack(anchor="w", pady=(4, 10))
        self.celdas_detalle = []
        for i in range(9):
            fila = i // 3
            col = i % 3
            lbl = tk.Label(
                marco_tab, text=" ",
                font=("Helvetica", 16, "bold"),
                width=2, height=1,
                bg=COLOR_PANEL, fg=COLOR_TEXTO,
            )
            lbl.grid(row=fila, column=col, padx=2, pady=2, ipadx=4, ipady=2)
            self.celdas_detalle.append(lbl)

        # Botones
        botones = tk.Frame(marco_detalle, bg=COLOR_FONDO)
        botones.pack(anchor="w", pady=(8, 0))

        self.btn_abrir = tk.Button(
            botones, text="Abrir visualización",
            command=self._abrir_visualizacion,
            bg=COLOR_ACENTO, fg="#1e1e2e",
            activebackground="#a8d68e",
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=12, pady=6, cursor="hand2",
        )
        self.btn_abrir.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_cerrar = tk.Button(
            botones, text="Cerrar",
            command=self.destroy,
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TITULO,
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=12, pady=6, cursor="hand2",
        )
        self.btn_cerrar.pack(side=tk.LEFT)

        self._registro_actual = None

    def _cargar_lista(self):
        registros = self.aplicacion.arbol_historial.recorrido_in_orden()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        n = 0
        for r in registros:
            self.tabla.insert(
                "", "end", iid=str(r.id_partida),
                values=(r.id_partida, r.ganador, r.movimientos_realizados,
                        r.modo, r.fecha),
            )
            n += 1
        self.lbl_info.config(
            text=f"{n} partidas · Árbol B grado t={self.aplicacion.arbol_historial.grado}"
                 f" · {self.aplicacion.arbol_historial.total_nodos} nodos"
        )

    def _al_seleccionar(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_p = int(seleccion[0])
        reg = self.aplicacion.arbol_historial.buscar(id_p)
        if reg is None:
            return
        self._registro_actual = reg
        self.lbl_detalle.config(
            text=(f"ID: {reg.id_partida}\n"
                  f"Modo: {reg.modo}\n"
                  f"Ganador: {reg.ganador}\n"
                  f"Movimientos: {reg.movimientos_realizados}\n"
                  f"Fecha: {reg.fecha}\n\n"
                  f"Resumen:\n{reg.resumen}")
        )
        for i in range(9):
            c = reg.tablero_final[i]
            lbl = self.celdas_detalle[i]
            if c == "X":
                lbl.config(text="X", fg=COLOR_X)
            elif c == "O":
                lbl.config(text="O", fg=COLOR_O)
            else:
                lbl.config(text="·", fg="#5c6370")

    def _abrir_visualizacion(self):
        if self._registro_actual is None:
            messagebox.showinfo("Visualización",
                                "Seleccione una partida primero.",
                                parent=self)
            return
        id_p = self._registro_actual.id_partida
        base = os.path.join("visualizaciones", f"partida_{id_p:04d}")
        ruta_png = base + ".png"
        ruta_dot = base + ".dot"
        ruta = ruta_png if os.path.exists(ruta_png) else (
               ruta_dot if os.path.exists(ruta_dot) else None)
        if ruta is None:
            messagebox.showwarning(
                "Visualización",
                "No se encontró archivo de visualización para esta partida.",
                parent=self,
            )
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(ruta) 
            elif sys.platform == "darwin":
                subprocess.Popen(["open", ruta])
            else:
                subprocess.Popen(["xdg-open", ruta])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}",
                                 parent=self)
