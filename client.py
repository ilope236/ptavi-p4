#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
# Cliente UDP simple.

# Dirección IP, puerto y mensaje para servidor
SERVER = sys.argv[1]      
PORT = int(sys.argv[2])
METODO = sys.argv[3]
USUARIO = sys.argv[4]

client_address = (sys.argv[1],int(sys.argv[2]))

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

LINE = METODO.upper() + " sip:"+ USUARIO + " SIP/1.0\r\n\r\n"

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
