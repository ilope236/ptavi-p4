#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time
registro = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def register2file(self):
        """
        Escribe en un fichero los usuarios registrados o dados de baja
        con sus valores.
        """

        fich = open("registered.txt", "w")
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\r\n")
        for clave in registro:
            tiempo = time.gmtime(registro[clave][2])
            hora = time.strftime('%Y-%m-%d %H:%M:%S', tiempo)
            fich.write(clave + "\t" + registro[clave][0] + "\t" + hora + "\r\n")
        fich.close()

    def borrar_caducados(self):
        """
        Gestiona la caducidad de los usuarios registrados
        """
        list_caducados = []
        for clave in registro:
            hora_entrada = registro[clave][2]
            expires = registro[clave][1]
            tiemp_a = time.time()
            if int(hora_entrada) + int(expires) <= tiemp_a:
                list_caducados.append(clave)
        for clave in list_caducados:
            del registro[clave]
            print 'Borramos al cliente: ' + clave

    def handle(self):
        while 1:
            # Lee linea a lina lo que llega del cliente
            line = self.rfile.read()
            #Comprobamos si hay linea en blanco
            if not line:
                break
            print "El cliente " + str(self.client_address) + " nos manda " + line
            #troceoamos la linea que nos llega
            line = line.split()
            #Verificamos que la formacion del regristrer es la correcta
            if line[0] == "REGISTER" and line[2] == "SIP/2.0":
                self.wfile.write(" SIP/2.0 200 OK\r\n\r\n")
                line[1] = line[1].split(":")
                #Solo metemos en el diccionario si el expires no es 0
                usuario = line[1][1]
                if line[4] != "0":
                    hora_s = time.time()
                    registro[usuario] = [str(self.client_address[0]), line[4], hora_s]
                    print 'Guardamos al cliente: ' + usuario
                else:
                #Si un usuario se da de baja y esta en el registro, le borramos
                    if usuario in registro:
                        del registro[usuario]
                        self.wfile.write(" SIP2.0 200 OK\r\n\r\n")
                #Borro usuarios caducados y escribimos en el fichero
                self.borrar_caducados(registro)
                self.register2file()
            else:
                self.wfile.write(" SIP/2.0 400 Bad Request\r\n\r\n")
            print registro
"""
Empieza programa principal
"""
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    SERVER = int(sys.argv[1])
    #Instanciamos EchoHandler
    serv = SocketServer.UDPServer(("", SERVER), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
