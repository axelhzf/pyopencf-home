#!/usr/bin/python
# encoding: utf-8

from soaplib.serializers.primitive import Integer, Float
from soaplib.serializers.clazz import ClassSerializer

class Parameters(ClassSerializer):
	"""Clase que representa los parámetros de un job"""
	class types:
		identificador = Integer
		n = Integer
		
	def __str__(self):
		return str(self.n)