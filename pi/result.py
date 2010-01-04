#!/usr/bin/python
# encoding: utf-8

from soaplib.serializers.primitive import Integer, Float
from soaplib.serializers.clazz import ClassSerializer

class Result(ClassSerializer):
	"""Clase que representa el resultado de un job"""
	class types:
		identificador = Integer
		
		resultado = Float