# coding: utf-8
r'''
Proyecto 2: Escribir un analizador
==================================
Su tarea es escribir las reglas de análisis y
construir el AST para esta gramática usando SLY.

'''
# ----------------------------------------------------------------------
# Analizadores son definidos usando SLY.  Se hereda de la clase Parser
#
# vea http://sly.readthedocs.io/en/latest/
# ----------------------------------------------------------------------
import sly

# ----------------------------------------------------------------------
# El siguiente import carga la función error(lineno, msg) que se debe
# usar para informar todos los mensajes de error emitidos por su analizador. 
# Las pruebas unitarias y otras características del compilador se basarán 
# en esta función. Consulte el archivo errors.py para obtener más 
# documentación sobre el mecanismo de manejo de errores.
from errors import error

# ------------------------------------------------- ---------------------
# Importar la clase lexer. Su lista de tokens es necesaria para validar y
# construir el objeto analizador.
from lexer import Lexer

# ----------------------------------------------------------------------
# Obtener los nodos AST.
# Lea las instrucciones en ast.py
from syntax_tree import *


class Parser(sly.Parser):

    debugfile = 'parser.txt'

    tokens = Lexer.tokens

    @_("titulo dias horas actividades")
    def horario(self, p):
        return Horario(p.titulo, p.dias, p.horas, p.actividades)

    @_("titulo dias actividades")
    def horario(self, p):
        return Horario(p.titulo, p.dias, None, p.actividades)

    @_("titulo horas actividades")
    def horario(self, p):
        return Horario(p.titulo, None, p.horas, p.actividades)

    @_("titulo actividades")
    def horario(self, p):
        return Horario(p.titulo, None, None, p.actividades)

    @_("TITULO DP CADENA")
    def titulo(self, p):
        return BloqueTitulo(p.CADENA, lineno=p.lineno)

    @_("DIAS DP rango_dias")
    def dias(self, p):
        return BloqueDias(p.rango_dias, lineno=p.lineno)

    @_("HORAS DP rango_horas")
    def horas(self, p):
        return BloqueHoras(p.rango_horas, lineno=p.lineno)

    @_("ACTIVIDADES DP lista_clases")
    def actividades(self, p):
        return BloqueActividades(p.lista_clases, lineno=p.lineno)

    @_("lista_clases clase PYC")
    def lista_clases(self, p):
        p.lista_clases.append(p.clase)
        return p.lista_clases

    @_("empty")
    def lista_clases(self, p):
        return []

    @_("CADENA lista_franjas")
    def clase(self, p):
        return Clase(p.CADENA, p.lista_franjas, lineno=p.lineno)

    @_("lista_franjas COMA franja")
    def lista_franjas(self, p):
        p.lista_franjas.append(p.franja)
        return p.lista_franjas

    @_("franja")
    def lista_franjas(self, p):
        return [p.franja]

    @_("lista_dias POR rango_horas")
    def franja(self, p):
        return FranjaHoraria(p.lista_dias, p.rango_horas, lineno=p.lineno)

    @_("lista_dias MAS rango_dias")
    def lista_dias(self, p):
        p.lista_dias.append(p.rango_dias)
        return p.lista_dias

    @_("rango_dias")
    def lista_dias(self, p):
        return [p.rango_dias]

    @_("empty")
    def lista_dias(self, p):
        return []

    @_("DIA")
    def rango_dias(self, p):
        return Dia(p.DIA, lineno=p.lineno)

    @_("DIA GUION DIA")
    def rango_dias(self, p):
        return RangoDias(p.DIA0, p.DIA1, lineno=p.lineno)

    @_("HORA GUION HORA")
    def rango_horas(self, p):
        return RangoHoras(p.HORA0, p.HORA1, lineno=p.lineno)

    @_("")
    def empty(self, p):
        pass

    # ----------------------------------------------------------------------
    # NO MODIFIQUE
    #
    # manejo de errores catch-all. Se llama a la siguiente función en
    # cualquier entrada incorrecta. p es el token ofensivo o None si
    # el final de archivo (EOF).
    def error(self, p):
        if p:
            error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
        else:
            error('EOF', 'Error de sintaxis. No mas entrada.')


# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA A CONTINUACIÓN
# ----------------------------------------------------------------------

def parse(source):
    '''
	Parser el código fuente en un AST. Devuelve la parte superior del árbol AST.
	'''
    lexer = Lexer()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(source))
    return ast


def main():
    '''
	Programa principal. Usado para probar.
	'''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python -m minic.parser filename\n')
        raise SystemExit(1)

    # Parse y crea el AST
    ast = parse(open(sys.argv[1], encoding="utf8").read())

    # Genera el árbol de análisis sintáctico resultante
    for depth, node in flatten(ast):
        print('%s: %s%s' % (getattr(node, 'lineno', None), ' ' * (4 * depth), node))

    dot = DotVisitor()
    dot.visit(ast)
    ast_file = open("AST.txt", "w", encoding="utf8")
    ast_file.write(str(dot))
    ast_file.close()


if __name__ == '__main__':
    main()
