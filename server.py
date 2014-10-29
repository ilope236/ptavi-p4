#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

clients = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP Register server class

    Métodos (más detallados en el propio método:
        register2file: crea un archivo con los clientes
        register: se encarga de procesar los mensajes register
    """
    def register2file(self):
        """
        Imprime la lista de clientes en el archivo 'registered.txt',
        con el formato:

        User \t IP \t Expires
        luke@polismassa.com \t localhost \t 2013-10-23 10:37:12
        papa@darthwader.com \t localhost \t 2013-10-23 10:21:15
        """
        fich = open("registered.txt", 'w')
        info = "User \t IP \t Expires\r\n"
        for client in clients:
            info += client + " \t "
            info += clients[client]["IP"] + " \t "
            tiempo = time.gmtime(clients[client]["time"])
            str_time = time.strftime('%Y-%m-%d %H:%M:%S', tiempo)
            info += str_time + " \t "
            info += "\r\n"
        fich.write(info)
        fich.close()

    def register(self, line):
        """
        Si es un mensaje register, agrega al cliente en cuestión
        a la variable global 'clients', informando por pantalla
        de cada paso.
        Guarda cada cliente como un diccionario del tipo
        Cliente:
            Nombre, un string generalmente de la forma nombre@dominio.com
            Valores:
                IP, un string con la IP del cliente
                time: segundo desde el 1 de enero de 1979 en el
                cual expirará
        """
        lineas = line.split("\r\n")
        palabras = lineas[0].split(" ") + lineas[1].split(" ")
        if palabras[0] == "REGISTER":
            cliente = palabras[1][4:]
            #prot_ver es una lista que incluye portocolo y versión
            prot_ver = palabras[2].split("/")
            Data = prot_ver[0] + "/" + prot_ver[1] + " 200 OK\r\n\r\n"
            expires = int(palabras[4])

            print "Registrando cliente nuevo..."
            time_act = time.time() + expires
            valor = {"IP": self.client_address[0], "time": time_act}
            clients[cliente] = valor
            print "...cliente agregado: ",
            print cliente + ": ",
            print valor

            if expires == 0:
                #Solo borramos el cliente si esta en clients
                if cliente in clients:
                    print "El tiempo de expiración es 0.",
                    del clients[cliente]
                    print "El cliente '" + cliente + "' ha sido borrado"

            self.wfile.write(Data)
        else:
            self.wfile.write("SIP/2.0 400 Bad Request" + '\r\n\r\n')

    def update(self):
        """ Actualiza la lista de clientes a la hora actual"""
        lista_tmp = []  # Para guardar qué clientes (key) debemos borrar
        for client in clients:
            if clients[client]["time"] < time.time():
                lista_tmp.append(client)
        for client in lista_tmp:
            print 'El cliente ' + client + ' ha sido borrado'
            del clients[client]

    def handle(self):
        """
        Entra en un bucle infinito a la espera de mensajes de clientes.
        Cuando llega un mensaje llama a los procesos correspondientes
        """
        print "Dirección del cliente: ",
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            # Asumo que el mensaje REGISTER estará bien construido
            line = self.rfile.read()
            if not line:
                break

            print 'El cliente nos envia: ' + line

            self.register(line)
            self.update()
            self.register2file()

            print "\r\n\r\n>> A la espera de nuevos clientes...\r\n\r\n"

if __name__ == "__main__":
    # Creamos servidor de register y escuchamos
    if len(sys.argv) == 2:
        s = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
        print "Lanzando servidor UDP de SIP Register...\r\n\r\n"
        s.serve_forever()
    else:
        print "Usage: $python server.py <port>"
