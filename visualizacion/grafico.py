import os

try:
    from graphviz import Source
    _GRAPHVIZ_LIB = True
except ImportError:
    _GRAPHVIZ_LIB = False

from estructuras.tablero import Tablero


def _escapar(texto):
    return (texto.replace("\\", "\\\\")
                  .replace('"', '\\"'))


def _tabla_html_tablero(estado_str, titulo, linea_ganadora=None):
    filas_html = ""
    for fila in range(3):
        celdas_html = ""
        for col in range(3):
            idx = fila * 3 + col
            c = estado_str[idx]
            display = c if c != " " else "·"
            if c == "X":
                color = "#e06c75"   
            elif c == "O":
                color = "#61afef"   
            else:
                color = "#5c6370"   
            bg = "#ffffff"
            if (linea_ganadora is not None) and (idx in linea_ganadora):
                bg = "#fff5b8"  
            celdas_html += (
                f'<TD WIDTH="34" HEIGHT="34" BGCOLOR="{bg}" '
                f'ALIGN="CENTER" VALIGN="MIDDLE">'
                f'<FONT COLOR="{color}" POINT-SIZE="22"><B>{display}</B></FONT>'
                f'</TD>'
            )
        filas_html += f'<TR>{celdas_html}</TR>'
    return (
        f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0">'
        f'<TR><TD COLSPAN="3" BGCOLOR="#282c34">'
        f'<FONT COLOR="#abb2bf" POINT-SIZE="11"><B>{titulo}</B></FONT>'
        f'</TD></TR>{filas_html}</TABLE>'
    )


class GeneradorGrafico:

    DIRECTORIO_BASE = "visualizaciones"

    @staticmethod
    def visualizar_partida(partida, directorio=None):

        if directorio is None:
            directorio = GeneradorGrafico.DIRECTORIO_BASE
        os.makedirs(directorio, exist_ok=True)

        nombre = f"partida_{partida.id_partida:04d}"
        ruta_base = os.path.join(directorio, nombre)

        estados_cadenas = []
        estados_cadenas.append(" " * 9)
        tab = Tablero()
        for paso in partida.trayectoria:
            tab.colocar(paso.movimiento.posicion, paso.simbolo)
            estados_cadenas.append(tab.como_cadena())

        linea_gan = partida.linea_ganadora

        # Cabecera del .dot
        lineas = []
        lineas.append(f'digraph Partida_{partida.id_partida} {{')
        lineas.append('    rankdir=LR;')
        lineas.append('    bgcolor="#1e1e2e";')
        lineas.append('    node [shape=plaintext, fontname="Helvetica"];')
        lineas.append('    edge [fontname="Helvetica", fontsize=10, color="#abb2bf", fontcolor="#abb2bf"];')

        if partida.resultado == partida.simbolo_sistema:
            res_txt = f"Victoria SISTEMA ({partida.simbolo_sistema})"
            color_titulo = "#98c379"
        elif partida.resultado == "EMPATE":
            res_txt = "Empate"
            color_titulo = "#e5c07b"
        else:
            res_txt = f"Victoria oponente ({partida.resultado})"
            color_titulo = "#e06c75"

        etiqueta_grafo = (
            f'<<FONT COLOR="#ffffff" POINT-SIZE="18"><B>Partida #{partida.id_partida}</B></FONT>'
            f'<BR/><FONT COLOR="{color_titulo}" POINT-SIZE="13">Resultado: {res_txt}</FONT>'
            f'<BR/><FONT COLOR="#abb2bf" POINT-SIZE="11">Modo: {partida.modo} | '
            f'Movimientos: {partida.trayectoria.tamanio} | '
            f'Jugador: {partida.simbolo_jugador} vs Sistema: {partida.simbolo_sistema}</FONT>>'
        )
        lineas.append(f'    label={etiqueta_grafo};')
        lineas.append('    labelloc=t;')

        # Nodos
        total_pasos = len(estados_cadenas)
        for i in range(total_pasos):
            es_ultimo = (i == total_pasos - 1)
            lg = linea_gan if es_ultimo else None
            titulo = f"Paso {i}" if i > 0 else "Inicio"
            if es_ultimo and partida.resultado is not None:
                titulo = f"Paso {i} (final)"
            html = _tabla_html_tablero(estados_cadenas[i], titulo, linea_ganadora=lg)
            lineas.append(f'    n{i} [label=<{html}>];')

        # Aristas 
        i = 0
        for paso in partida.trayectoria:
            color_jugador = "#e06c75" if paso.simbolo == "X" else "#61afef"
            es_del_sistema = (paso.simbolo == partida.simbolo_sistema)
            etiqueta_sistema = "  [SISTEMA]" if es_del_sistema else ""
            delta = paso.peso_despues - paso.peso_antes
            signo = "+" if delta >= 0 else ""
            if es_del_sistema:
                etiqueta_peso = (
                    f"Pos {paso.movimiento.posicion} ({paso.simbolo}){etiqueta_sistema}"
                    f"\\nPeso: {paso.peso_antes:.2f} → {paso.peso_despues:.2f} ({signo}{delta:.2f})"
                )
            else:
                etiqueta_peso = (
                    f"Pos {paso.movimiento.posicion} ({paso.simbolo})"
                    f"\\nPeso: {paso.peso_antes:.2f} (sin ajuste)"
                )
            estilo_pluma = "bold" if es_del_sistema else "solid"
            lineas.append(
                f'    n{i} -> n{i+1} '
                f'[label="{etiqueta_peso}", color="{color_jugador}", '
                f'fontcolor="{color_jugador}", style="{estilo_pluma}", penwidth=2];'
            )
            i += 1

        lineas.append('}')

        # Guardar
        codigo_dot = "\n".join(lineas)
        ruta_dot = ruta_base + ".dot"
        with open(ruta_dot, "w", encoding="utf-8") as f:
            f.write(codigo_dot)

        # Intentar renderizar imagen
        if _GRAPHVIZ_LIB:
            try:
                src = Source(codigo_dot, filename=ruta_base, format="png")
                src.render(cleanup=True)
                ruta_png = ruta_base + ".png"
                if os.path.exists(ruta_png):
                    return ruta_png
            except Exception as e:
                print(f"[Graphviz] No se pudo renderizar PNG: {e}")
        return ruta_dot

    @staticmethod
    def visualizar_arbol_b(arbol_b, directorio=None):
        """Genera un .dot/.png con la estructura completa del árbol B del historial."""
        if directorio is None:
            directorio = GeneradorGrafico.DIRECTORIO_BASE
        os.makedirs(directorio, exist_ok=True)
        ruta_base = os.path.join(directorio, "arbol_b_historial")

        lineas = []
        lineas.append('digraph ArbolB {')
        lineas.append('    rankdir=TB;')
        lineas.append('    bgcolor="#1e1e2e";')
        lineas.append('    node [shape=plaintext, fontname="Helvetica"];')
        lineas.append('    edge [color="#abb2bf"];')
        lineas.append(
            f'    label=<<FONT COLOR="#ffffff" POINT-SIZE="16"><B>Árbol B del historial</B></FONT>'
            f'<BR/><FONT COLOR="#abb2bf" POINT-SIZE="11">'
            f'grado mínimo t = {arbol_b.grado} | registros = {arbol_b.total_registros} | '
            f'nodos = {arbol_b.total_nodos}</FONT>>;'
        )
        lineas.append('    labelloc=t;')

        ids = {}
        contador = [0]

        def asignar_id(nodo):
            if id(nodo) not in ids:
                ids[id(nodo)] = f"b{contador[0]}"
                contador[0] += 1
            return ids[id(nodo)]

        # BFS para emitir nodos y aristas
        if arbol_b.raiz is not None and arbol_b.raiz.num_claves() > 0:
            cola_visual = [arbol_b.raiz]
            while cola_visual:
                siguiente = []
                for nodo in cola_visual:
                    nid = asignar_id(nodo)
                    celdas = ""
                    for k in nodo.claves:
                        gan = k.ganador if k.ganador != "EMPATE" else "="
                        color_gan = "#98c379" if gan == "O" else (
                            "#e06c75" if gan == "X" else "#e5c07b")
                        celdas += (
                            f'<TD BGCOLOR="#282c34" CELLPADDING="4">'
                            f'<FONT COLOR="#ffffff" POINT-SIZE="11">#{k.id_partida}</FONT>'
                            f'<BR/><FONT COLOR="{color_gan}" POINT-SIZE="10"><B>{gan}</B></FONT>'
                            f'</TD>'
                        )
                    if not celdas:
                        celdas = '<TD BGCOLOR="#282c34" CELLPADDING="4">' \
                                 '<FONT COLOR="#abb2bf">∅</FONT></TD>'
                    html = (
                        f'<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" '
                        f'COLOR="#61afef"><TR>{celdas}</TR></TABLE>'
                    )
                    lineas.append(f'    {nid} [label=<{html}>];')
                    if not nodo.hoja:
                        for hijo in nodo.hijos:
                            hid = asignar_id(hijo)
                            lineas.append(f'    {nid} -> {hid};')
                            siguiente.append(hijo)
                cola_visual = siguiente

        lineas.append('}')
        codigo_dot = "\n".join(lineas)
        ruta_dot = ruta_base + ".dot"
        with open(ruta_dot, "w", encoding="utf-8") as f:
            f.write(codigo_dot)

        if _GRAPHVIZ_LIB:
            try:
                src = Source(codigo_dot, filename=ruta_base, format="png")
                src.render(cleanup=True)
                ruta_png = ruta_base + ".png"
                if os.path.exists(ruta_png):
                    return ruta_png
            except Exception as e:
                print(f"[Graphviz] No se pudo renderizar PNG del árbol B: {e}")
        return ruta_dot
