# lexer.py
# coding: utf-8
r'''
Proyecto 1 - Escribir un Lexer
==============================

En este primer proyecto, usted debe escribir un lexer sencillo para 
un lenguaje de instrucciones: MiniC. 

El proyecto es basado en código que usted debe leer (en este archivo) 
y completar. Por favor, lea el contenido completo de este archivo y 
cuidadosamente complete los pasos indicados como comentarios.

Revisión:
---------
El proceso del analizador léxico es la de tomar el texto de entrada y 
descomponerlo en un flujo de símbolos (tokens). Cada token es como una 
palabra válida del diccionario.  Escencialmente, el papel del lexer es 
simplemente asegurarse de que el texto de entrada se compone de símbolos 
válidos antes de cualquier procesamiento adicional relacionado con el 
análisis sintático.

Cada token es definido por una expresion regular. Por lo tanto, su 
principal tarea en este primer proyecto es definir un conjunto de 
expresiones regulares para el lenguaje. El trabajo actual del análisis 
léxico deberá ser manejado por SLY.

'''

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
		'Tı́tulo', 'Dı́as', 'Horas', 'Actividades'
	}

	# ----------------------------------------------------------------------
	# Conjunto de token. Este conjunto identifica la lista completa de 
	# nombres de tokens que reconocerá su lexer.
	tokens = {
		# keywords
		* { unidecode.unidecode(kw.upper()) for kw in keywords },

		CADENA,
	}
	literals = ''
	
	# ----------------------------------------------------------------------
	# Caracteres ignorados (whitespace)
	#
	# Los siguientes caracteres son ignorados completamente por el lexer.
	# No lo cambie.

	ignore = ' \t\r'

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
	GN = r'\-'
	PYC = r';'


	# ----------------------------------------------------------------------
	#                           *** DEBE COMPLETAR ***
	#
	# escriba las expresiones regulares y el código adicional a continuación
	#
	# Tokens para literales.
	#


	# ----------------------------------------------------------------------
	#                           *** DEBE COMPLETAR ***
	#
	# escribir la expresión regular y agregar palabras reservadas
	#
	# Identificadores y palabras reservadas
	#
	# Concuerde con un identificador. Los identificadores siguen las mismas 
	# reglas que Python. Es decir, comienzan con una letra o un guión bajo (_)
	# y pueden contener una cantidad arbitraria de letras, dígitos o guiones
	# bajos después de eso.
	# Las palabras reservadas del lenguaje como "if" y "while" también se 
	# combinan como identificadores. Debe capturar estos y cambiar su tipo 
	# de token para que coincida con la palabra clave adecuada.
	
	CADENA = r'\"(\\.|[^\n\"\\])*\"'

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
	text = open(sys.argv[1]).read()
	for tok in lexer.tokenize(text):
		print(tok)

if __name__ == '__main__':
	main()
