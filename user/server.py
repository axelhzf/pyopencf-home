#!/opt/local/bin/python2.5

from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Any
from soaplib.serializers.clazz import ClassSerializer

import sys
import os
import xml.dom.minidom

####################### CONFIG OPTIONS #########################
from config.config import *
from problems.superclass import *
import logging

logger = logging.getLogger('pyOpenCFServer')

################################################################
########################## pyOpenCF ############################
################################################################
class Service(ClassSerializer):
	class types:
		name = String
		desc = String
		serv_name = String

class ServiceArray(ClassSerializer):
	class types:
		ret = Array(Service)


class pyOpenCFService(pyOpenCFSimple):

	@soapmethod(_returns=String)
	def serverStatus(self):
		logger.info("Consultando el estado del servidor")
		results = "Status = OK (no errors)"
		return results

	@soapmethod(_return=Integer)
	def is_pyopencf(self):
		logger.debug("Consultando tipo de servidor")
		result = True
		return result

	@soapmethod(String,_returns=String)
	def getJobDesc(self,jobName):
		logger.info("Consultando la descripcion de " + jobName)
		path = xml_dir + '/' + jobName + '.xml'
		if os.path.isfile(path):
			f = open(path,"r")
			xml_content = f.read()
			f.close()
			logger.debug("Se envia la descripcion de " + jobName)
			return xml_content
		logger.warning("No se encontro la descripcion de " + jobName)
		return ""
	
	@soapmethod(String,_returns=String)
	def status(self,jobId):
		if jobId:
			logger.debug("Se consulta el estado de " + jobId)
			if os.path.isdir('/proc/' + jobId):
				return "Running"
			else:
				return "Finished"
		else:
			logger.error("No se proporciono un ID valido")
			return ""
	
	@soapmethod(String,_returns=String)
	def jobDelete(self,jobId):
		if jobId:
			if os.path.isdir('/proc/' + jobId):
				logger.info("Se intenta eliminar el job " + jobId + " del sistema")
				exe = SUDO + ' kill ' + jobId
				try:
					os.system(exe)
				except:
					logger.warning("El job " + jobId + " ha finalizado correctamente")
					return ""
				logger.info("Se ha eliminado el job " + jobId + " del sistema correctamente")
				return "Deleted"
		logger.error("No se proporciono un ID valido")
		return ""	
	
	@soapmethod(_returns=Array(Service))
	def availableJobs(self):
		import glob
		exe = xml_dir + "/*.xml"
		problems = glob.glob(exe)
		jobs = []
		for file in problems:
			job = Service()
			info = open(file,"r")
			xmldoc = xml.dom.minidom.parseString(info.read())
			nombre = xmldoc.getElementsByTagName("name")
			job.name = nombre[0].childNodes[0].nodeValue
			descrip = xmldoc.getElementsByTagName("description")
                	job.desc = descrip[0].childNodes[0].nodeValue
			servicio = xmldoc.getElementsByTagName("service_name")
			job.serv_name = servicio[0].childNodes[0].nodeValue
			info.close()
			jobs.append(job)
		logger.info("Se envian los servicios disponibles")
		return jobs


application = pyOpenCFService()

########################################################
################## CREATE SERVER #######################
########################################################
if __name__=='__main__':
	from cherrypy.wsgiserver import CherryPyWSGIServer
	try:
		server = CherryPyWSGIServer(('localhost',8021),pyOpenCFService())
		logger.info("El servidor comenzo a funcionar")
		server.start()
	except KeyboardInterrupt:
		logger.info("El servidor ceso de funcionar manualmente")
		print "\n"
		server.stop()	
