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

    precedence = (
    )

    @_("titulo dias horas actividades")
    def horario(self, p):
        return (p.titulo, p.dias, p.horas, p.actividades)

    @_("titulo dias actividades")
    def horario(self, p):
        return (p.titulo, p.dias, p.actividades)

    @_("titulo horas actividades")
    def horario(self, p):
        return (p.titulo, p.horas, p.actividades)

    @_("titulo actividades")
    def horario(self, p):
        return (p.titulo, p.actividades)

    @_("TITULO DP CADENA")
    def titulo(self, p):
        return (p.TITULO, p.DP, p.CADENA)

    @_("DIAS DP DIA GUION DIA")
    def dias(self, p):
        return (p.DIAS, p.DP, p.DIA0, p.GUION, p.DIA1)

    @_("HORAS DP HORA GUION HORA")
    def horas(self, p):
        return (p.HORAS, p.DP, p.HORA0, p.GUION, p.HORA1)

    @_("ACTIVIDADES DP lista_actividades")
    def actividades(self, p):
        return (p.ACTIVIDADES, p.DP, p.lista_actividades)

    @_("clase PYC lista_actividades")
    def lista_actividades(self, p):
        p.lista_actividades.append(p.clase)
        return p.lista_actividades

    @_("clase")
    def lista_actividades(self, p):
        return [p.clase]

    @_("empty")
    def lista_actividades(self, p):
        return []

    @_("CADENA franja_horaria")
    def clase(self, p):
        return (p.CADENA, p.franja_horaria)

    @_("empty")
    def franja_horaria(self, p):
        return ()

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


if __name__ == '__main__':
    main()
