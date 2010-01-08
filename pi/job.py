#!/usr/bin/python
# encoding: utf-8

class Job(object):
	def run(self, parametros, resultado):
		"""Trabajo que realizan los usuarios. Devuelve True si el trabajo se realizó con exito"""
		suma = 0
		for i in range(parametros.inicio, parametros.fin):
			x = parametros.h * (i - 0.5)
			suma += (4.0 / (1.0 + x * x))
			
		resultado.resultado = suma * parametros.h
		return True
