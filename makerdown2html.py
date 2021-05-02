#!/usr/bin/python3
""" script that takes an argument 2 strings  """

if __name__ == '__main__':

import sys

nombre_sript = sys.argv[0]
cantidad_argumentos = len(sys.argv)
argumentos = str(sys.argv)

stderr_fileno = sys.stderr

if cantidad_argumentos < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    exit(1)
