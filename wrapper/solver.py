#!/usr/bin/python
# encoding: utf-8
from time import sleep
N = 100
GRUPO = 10
TRABAJOS = N / GRUPO

class Solver(object):
	
	def __init__(self):
		self.n = 3
		pass
		
	def isActive(self):
		"""Devuelve True si el Solver todavía no ha terminado"""
		return True
		
	def getJob(self, parameters):
		"""Devuelve el trabajo i cambiar nombre a dar trabajo"""
		parameters.n = self.n
		#self.n += 1
		return True

		
	def doneJob(self, res):
		"""El resultado del trabajo i es res"""
		print "========================================"
		print res.resultado
		sleep(2)
		
	
	def errorJob(self, i):
		"""Se produjo un error en el trabajo i. Desmarcarlo para enviarlo otra vez"""
		pass
	
	def endWork(self):
		""" Termina el procesado y guarda el resultado a un fichero """
		pass