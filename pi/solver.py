#!/usr/bin/python
# encoding: utf-8

N = 100
GRUPO = 10
TRABAJOS = N / GRUPO

class Solver(object):
	
	def __init__(self):
		self.resultados = [None]*TRABAJOS
		self.running = True		
		self.trabajosAEnviar = range(TRABAJOS)
		self.trabajosTerminados = []
		
	def isActive(self):
		"""Devuelve True si el Solver todavía no ha terminado"""
		return self.running;
		
	def getJob(self, parameters):
		"""Devuelve el trabajo i cambiar nombre a dar trabajo"""
		
		if(len(self.trabajosAEnviar) > 0):
			trabajo = self.trabajosAEnviar.pop()
			
			parameters.identificador = trabajo
			parameters.inicio = trabajo * GRUPO
			parameters.fin = parameters.inicio + GRUPO
			parameters.h = 1.0 / N
			
			return True
		return False

		
	def doneJob(self, res):
		"""El resultado del trabajo i es res"""
		self.resultados[res.identificador] = res.resultado
		self.trabajosTerminados.append(res.identificador)
		if(len(self.trabajosTerminados) == TRABAJOS):
			self.endWork()
		
	
	def errorJob(self, i):
		"""Se produjo un error en el trabajo i. Desmarcarlo para enviarlo otra vez"""
		self.trabajosAEnviar.append(i)
	
	def endWork(self):
		""" Termina el procesado y guarda el resultado a un fichero """
		aux = 0.
		print self.resultados
		for i in self.resultados:
			if i:
				aux += i
		print "El resultado es %f" % aux
		
		self.running = False
