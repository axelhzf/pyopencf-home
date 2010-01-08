#!/usr/bin/python
# encoding: utf-8

from soaplib.serializers.primitive import Integer, Float
from soaplib.serializers.clazz import ClassSerializer

class Parameters(ClassSerializer):
	"""Clase que representa los parámetros de un job"""
	class types:
		identificador = Integer
		
		inicio = Integer
		fin = Integer
		h = Float
