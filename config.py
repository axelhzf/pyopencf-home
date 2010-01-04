#!/usr/bin/env python
# encoding: utf-8
"""
	config.py - Fichero de configuración

"""

#Carpeta donde está el problema que se va a resolver
PROBLEM = 'wrapper'

#Configuración del servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8023
SERVER_ENGINE_PORT = 8025

#Puertos del cliente
CLIENT_PORT_FROM = 8050
CLIENT_PORT_TO   = 8080

#Activa el control del uso de CPU. Sólo funciona en linux
CPU_USAGE_ACTIVE = False
# % Límite para pedir trabajo
CPU_USAGE_LIMIT = 80
# Segundos para volver a pedir trabajo cuando la CPU está cargada
CPU_USAGE_SLEEP = 20 
