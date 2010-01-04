#!/usr/bin/python
# encoding: utf-8

import commands
class Job(object):
	def run(self, parametros, resultado):
		"""Trabajo que realizan los usuarios. Devuelve True si el trabajo se realizó con exito"""

		cmd = "wrapper/helloworld " + str(parametros)
	    
		try:
			resultado.resultado = commands.getoutput(cmd)
			return True
		except Exception,e:
			print e
			print("No se pudo ejecutar " + cmd)
			return False