#!/usr/bin/python
# encoding: utf-8

"""
	user.py - Programa usuario

"""


import cherrypy
from cherrypy.process.plugins import Monitor
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import Boolean, Integer
from time import sleep
from cola import BackgroundTaskQueue
from runForever import RunForever
from cpuUsage import *

from suds.client import Client
import random
import sys

from config import *
exec("from " + PROBLEM + ".job import Job")
exec("from " + PROBLEM + ".parameters import Parameters")
exec("from " + PROBLEM + ".result import Result")	

class PyOCFAtHomeUser(SimpleWSGISoapApp):		
	@soapmethod(Parameters, _returns=Result)
	def run(self, valor):	
		print "Haciendo el trabajo"
		#sleep(20) #Sleep para probar 
		resultado = Result()
		resultado.identificador = valor.identificador
		j = Job()
		j.run(valor, resultado)
				
		print "Trabajo terminado"
		return resultado
		

def requestJob():
	"""Se ejecuta periodicamente. Comprueba que el cliente esté trabajando. 
	   Si no está trabajando le pide trabajo al servidor"""
	

	print "Voy a pedir trabajo"
		
	try:		
		proxy = Client("http://" + SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/pyocfathome.wsdl")
		
		if(CPU_USAGE_ACTIVE):
			usage = CPUsage().result
			if(usage > CPU_USAGE_LIMIT):
				print "Uso de cpu excesivo :" + str(usage)
				sleep(CPU_USAGE_SLEEP)
				return None
		
		res =  proxy.service.newJob("http://" + clientAddress + ": " + str(clientPort) + "/pyocfathome.wsdl")
		
		if res == 0:
			print "No hay trabajo disponible en el servidor"
			sleep(60)
	except Exception, e:
		print "[Error]" + str(e)
		
		"""Normalmente el error se produce porque el servidor no está disponible
		   espera 60 segundos para volver a hacer el siguiente intento"""
		sleep(1)
			


def randomizePort():
	"""Busca puertos aleatorios dentro del rango establecido en el fichero de configuracion"""	
	global clientPort
	global clientEnginePort
		
	portDefined = False	
	intento = 0
	while portDefined == False:
		port = random.randint(CLIENT_PORT_FROM, CLIENT_PORT_TO)
		try:
			cherrypy.process.servers.check_port(clientAddress, port)
			clientPort = port
			portDefined = True
		except Exception, e:
			print e
			pass
		
		intento += 1
		if(intento == 10):
			print "No se pudo encontrar puerto para el servidor"
			sys.exit(0)
		
	intento = 0
	portEngineDefined = False
	while portEngineDefined == False:
		port = random.randint(CLIENT_PORT_FROM, CLIENT_PORT_TO)
		try:
			cherrypy.process.servers.check_port(clientAddress, port)
			
			if port == clientPort: #El puerto del servidor y del engine no debería ser el mismo
				continue
				
			clientEnginePort = port
			portEngineDefined = True
		except Exception:
			pass
			
		intento += 1
		if(intento == 10):
			print "No se pudo encontrar puerto para el engine"
			sys.exit(0)
			
	print "Puerto servidor: " + str(clientPort)
	print "Puerto engine: " + str(clientEnginePort)				
			


#Suscribe el hilo que pide trabajo
runForever = RunForever(cherrypy.engine, requestJob)
runForever.subscribe()


clientAddress = "localhost"
clientPort = 8045
clientEnginePort = 8046

if __name__ == '__main__':
	from cherrypy.wsgiserver import CherryPyWSGIServer
	
	randomizePort()
	try:	
		cherrypy.server.socket_port = clientEnginePort
		server = CherryPyWSGIServer(('localhost', clientPort), PyOCFAtHomeUser())
		cherrypy.engine.start()
		server.start()
	except KeyboardInterrupt:
		print "\n"
		server.stop()
		
		