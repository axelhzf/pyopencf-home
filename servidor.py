#!/usr/bin/python
# encoding: utf-8
from suds.client import Client
import random
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Boolean, Integer, Array
import cherrypy
from cola import BackgroundTaskQueue
from soaplib.serializers.clazz import ClassSerializer
from cherrypy.process.plugins import Monitor
from config import *
from time import sleep

#Importa el problema especificado en el fichero de configuración
exec("from " + PROBLEM + ".solver import Solver")
exec("from " + PROBLEM + ".result import Result")


asignaciones = {}

solver = Solver()
class PyOCFAtHomeServer(SimpleWSGISoapApp):
	@soapmethod(_returns=Boolean)
	def serverStatus(self):
		return True			
	
	@soapmethod(String, _returns=Integer)
	def newJob(self,wsdlfile):
		"""Codigos de retorno: 0 - No hay trabajo
							   1 - Trabajo realizado correctamente
							   2 - Error. Posible perdida de conexion"""
		
		retvalue = 0
		if(solver.isActive()):		
			cliente = Client(wsdlfile)
			parametros = cliente.factory.create('Parameters')
			if(solver.getJob(parametros)):
				asignaciones[parametros.identificador] = wsdlfile
				
				try:
					resultado = cliente.service.run(parametros)
					solver.doneJob(resultado)
					retvalue = 1 #Todo correcto
				except Exception, e:
					#Se produce excepcion cuando se pierde la comunicacion con el cliente
					print e
					solver.errorJob(parametros.identificador)
					retvalue = 2 #Error
				finally:
					asignaciones.pop(parametros.identificador)
				
				
		return retvalue
		
if __name__ == '__main__':
	from cherrypy.wsgiserver import CherryPyWSGIServer
	try:
		server = CherryPyWSGIServer((SERVER_ADDRESS, SERVER_PORT), PyOCFAtHomeServer())
		server.start()
	except KeyboardInterrupt:
		print "\n"
		server.stop()	
