from estructuras.lista_enlazada import ListaEnlazada
from estructuras.tablero import Tablero


class PasoTrayectoria:
    __slots__ = ("estado_antes", "movimiento", "simbolo", "peso_antes", "peso_despues")

    def __init__(self, estado_antes, movimiento, simbolo):
        self.estado_antes = estado_antes        
        self.movimiento = movimiento            
        self.simbolo = simbolo                  
        self.peso_antes = movimiento.peso
        self.peso_despues = movimiento.peso    


class Partida:
    def __init__(self, id_partida, simbolo_jugador, simbolo_sistema, modo="MANUAL"):
        self.id_partida = id_partida
        self.tablero = Tablero()
        self.simbolo_jugador = simbolo_jugador  
        self.simbolo_sistema = simbolo_sistema  
        self.modo = modo
        self.trayectoria = ListaEnlazada()      
        self.turno_actual = "X"                
        self.terminada = False
        self.resultado = None                  
        self.linea_ganadora = None              

    def aplicar_movimiento(self, movimiento_obj, simbolo):
        if self.terminada:
            return False
        estado_antes = self.tablero.como_cadena()
        paso = PasoTrayectoria(estado_antes, movimiento_obj, simbolo)
        self.trayectoria.agregar(paso)
        ok = self.tablero.colocar(movimiento_obj.posicion, simbolo)
        if not ok:
            return False
        # Verificar fin de partida
        gan, linea = self.tablero.ganador()
        if gan is not None:
            self.terminada = True
            self.resultado = gan
            self.linea_ganadora = linea
        elif self.tablero.lleno():
            self.terminada = True
            self.resultado = "EMPATE"
        # Alternar turno
        self.turno_actual = "O" if self.turno_actual == "X" else "X"
        return True

    def generar_resumen(self):
        n_movs = self.trayectoria.tamanio
        if self.resultado == "EMPATE":
            res_txt = "Empate"
        elif self.resultado == self.simbolo_sistema:
            res_txt = f"Victoria SISTEMA ({self.simbolo_sistema})"
        else:
            res_txt = f"Victoria {'JUGADOR' if self.modo == 'MANUAL' else 'OPONENTE'} ({self.resultado})"
        return f"[{self.modo}] {n_movs} movimientos. {res_txt}."
