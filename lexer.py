# lexer.py
# coding: utf-8
# ----------------------------------------------------------------------
# El siguiente import carga una función error(lineno,msg) que se debe
# utilizar para informar de todos los mensajes de error emitidos por su
# lexer. Las pruebas unitarias y otras caracteristicas del compilador
# confiarán en esta función. Ver el archivo errors.py para más documentación
# acerca del mecanismo de manejo de errores.
from errors import error

# ----------------------------------------------------------------------
# El paquete SLY. https://github.com/dabeaz/sly
import sly
import unidecode


class Lexer(sly.Lexer):
    # -------
    # Conjunto de palabras reservadas.  Este conjunto enumera todos los
    # nombres especiales utilizados en el lenguaje
    keywords = {
        'Título', 'Días', 'Horas', 'Actividades'
    }

    # ----------------------------------------------------------------------
    # Conjunto de token. Este conjunto identifica la lista completa de
    # nombres de tokens que reconocerá su lexer.
    tokens = {
        # keywords
        *{unidecode.unidecode(kw.upper()) for kw in keywords},
        DP, DIA, GUION, HORA, PYC, COMA, POR, MAS, CADENA
    }

    # ----------------------------------------------------------------------
    # Caracteres ignorados (whitespace)
    #
    # Los siguientes caracteres son ignorados completamente por el lexer.
    # No lo cambie.

    ignore = ' \t'

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escriba las expresiones regulares que se indican a continuación.
    #
    # Tokens para símbolos simples.
    #
    # Precaución: El orden de las definiciones es importante. Los símbolos
    # más largos deben aparecer antes de los símbolos más cortos que son
    # una subcadena (por ejemplo, el patrón para <= debe ir antes de <).

    DP = r':'
    DIA = r'L|M|X|J|V|S'
    GUION = r'\-'
    HORA = r'[0-1]\d|2[0-3]|\d'
    PYC = r';'
    COMA = r','
    POR = r'\*'
    MAS = r'\+'
    CADENA = r'\".*\"'

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escribir la expresión regular y agregar palabras reservadas
    #
    # Las palabras reservadas del lenguaje. Debe capturar estas y cambiar su tipo
    # de token para que coincida con la palabra clave adecuada.'

    TITULO = r'Título'
    DIAS = r'Días'
    HORAS = r'Horas'
    ACTIVIDADES = r'Actividades'
    # PALABRA = r'[A-zÀ-ú]+'
    # PALABRA['Título'] = TITULO
    # PALABRA['Días'] = DIAS
    # PALABRA['Horas'] = HORAS
    # PALABRA['Actividades'] = ACTIVIDADES

    @_(r'\n')
    def newline(self, t):
        self.lineno += 1

    # ----------------------------------------------------------------------
    # Manejo de errores de caracteres incorrectos
    def error(self, t):
        error(self.lineno, 'Caracter Ilegal %r' % t.value[0])
        self.index += 1


# ----------------------------------------------------------------------
#                   NO CAMBIE NADA POR DEBAJO DE ESTA PARTE
#
# Use este programa principal para probar/depurar su Lexer. Ejecutelo 
# usando la opción -m
#
#    bash% python3 -m minic.clexer filename.c
#
# ----------------------------------------------------------------------
def main():
    '''
	main. Para propósitos de depuracion
	'''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python3 -m clexer filename\n')
        raise SystemExit(1)

    lexer = Lexer()
    text = open(sys.argv[1], encoding="utf8").read()
    for tok in lexer.tokenize(text):
        print(tok)


if __name__ == '__main__':
    main()
