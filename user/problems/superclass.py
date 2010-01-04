from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Any, Null, Float, Boolean
from soaplib.serializers.binary import Attachment
from soaplib.serializers.clazz import ClassSerializer

import sys
import os
import string
from tempfile import mkstemp

####################### CONFIG OPTIONS #########################
bin_path = os.path.dirname(os.path.abspath(sys.argv[0]))
proyect_path = os.path.abspath(bin_path + '/../')
sys.path.append(proyect_path)
from config.config import *

######################### LOG OPTIONS ##########################
import logging

logger = logging.getLogger("pyOpenCFServer") 
log = logging.FileHandler(LOG_FILE)
if (LOG_LEVEL == DEBUG):
    logger.setLevel(logging.DEBUG)
elif (LOG_LEVEL == WARN):
    logger.setLevel(logging.WARNING)
else:
    logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log.setFormatter(formatter)
logger.addHandler(log)

########################## SEND MAIL ###########################
def sendmail(email,job, results):
    if SEND:
        p = os.popen("%s -t" % SENDMAIL, "w")
        receiver = "To: " + email + "\n"
        p.write(receiver)
        subject = "Subject: " + job + " results on " + server_name + "\n"
        p.write(subject)
        p.write("\n") # blank line separating headers from body
        p.write("You receive this email because you launch a job in this server\n")
        if results:
            r = "\nYou can access to the results of your job in this address " + results + "\n"
            p.write(r)
        p.write("\n")
        sts = p.close()
        if sts != 0:
            logger.error("Sendmail to %s exit status %s" %(email,sts))
        else:
            logger.info("Sendmail to %s status ok" %email)
    else:
        logger.debug("Sendmail is switched off, sorry %s" % email)
################################################################
############################# RUN ##############################
################################################################
def Run(bin,email,args,namedArgs = False):
    cmd = "python " + bin_dir + "/wrapper.py " + email 
    cmd += " \'" + OPENCF_BASE + "/" + bin
    if args:
        for arg in args:
            if namedArgs: 
                cmd += ' --' + arg[0] + " " + str(arg[1])
            else:
                cmd += " " + str(arg[1])
    mypid = OPENCF_BASE + "/" + bin + "_id"
    cmd += " > results/tmp\' > " + mypid
    try:
        logger.info("Ejecutando: " + bin)
        a = os.system(cmd)
    except:
        logger.error("No se pudo ejecutar " + bin)
        return ""
    f = open(mypid,"r")
    pid = string.rstrip(f.read())
    f.close()
    cmd = "rm %s" %mypid
    os.system(cmd)
    logger.info("Ejecutado con exito " + bin)
    return pid

################################################################
########################## pyOpenCF ############################
################################################################
class Result(ClassSerializer):
    class types:
        job_id = String
        out = String

class pyOpenCFSimple(SimpleWSGISoapApp):

    __tns__ = 'http://opencf.pcg.ull.es/soap/'

    @soapmethod(String,Integer,_returns=Result)
    def helloworld(self, email, num):
        output = os.tempnam(output_dir + "/")
        pid = Run("bin/helloworld",email,[["num",num],["out",output]])
        results = Result()
        results.job_id = pid
        results.out = output
        sendmail(email,"helloworld",output)
        return results

