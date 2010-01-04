import sys
import os

import string
import xml.dom.minidom

outfile = 'problems/superclass.py'
tab = " "*4
tab = "%s"*2 % (tab, tab)

if len(sys.argv) > 1:

    for i in range(len(sys.argv)-1):
        i += 1
        input = sys.argv[i]
        # INPUT FILE
        try:
            fin = open(input,'r')
        except:
            print "*** ERROR: File %s cannot be opened" %input
            break
        # OUTPUT FILE
        try:
            fout = open(outfile,'a')
        except:
            print "*** ERROR: File %s cannot be opened" %out
            exit
        # OUTPUT WRITTING
        fout.write("\n")
        doc = xml.dom.minidom.parseString(fin.read())
        fin.close()
        service = "%s@soapmethod(String,&&_returns=Result)\n%sdef " % (tab, tab)
        base64 = []
        args = []
        namedArgs = 0
        if doc:
            jobs = doc.getElementsByTagName('job')
            for job in jobs:
                for usedNamedArg in job.getElementsByTagName('useNamedArgs'):
                    namedArgs = 1
                serv_name = job.getElementsByTagName('service_name')[0].childNodes[0].nodeValue
                service += serv_name + "(self, email"
                for arg in job.getElementsByTagName('argument'):
                    name = arg.getElementsByTagName('name')[0].childNodes[0].nodeValue
                    service += ", " + name
                    if (arg.getAttribute('type') == "string"):
                        service = service.replace("&&","String,&&")
                    elif (arg.getAttribute('type') == "integer"):
                        service = service.replace("&&","Integer,&&")
                    elif (arg.getAttribute('type') == "base64Binary"):
                        service = service.replace("&&","Attachment,String,&&")
                        service += ", " + name + "_fn"
                        base64.append(name)
                    elif (arg.getAttribute('type') == "double"):
                        service = service.replace("&&","Float,&&")
                    elif (arg.getAttribute('type') == "boolean"):
                        service = service.replace("&&","Boolean,&&")
                    args.append(name)
                service = service.replace("&&","")
                service += "):\n\t\t"
                o_file = job.getElementsByTagName('output_file')
                if o_file:
                    aux = o_file[0].getElementsByTagName('name')
                    service += "output = os.tempnam(output_dir + \"/\")\n%s" % tab2
                else:
                    service += "output = \"\"\n%s" % tab2
                for f in base64:
                    service += '%s_fn = os.tempnam(output_dir + \"/\")\n%s' % (f, tab2)
                    service += f + '.fileName = %s_fn\n%s' % (f, tab2)
                    service += f + '.save_to_file()\n%s' % tab2
                bin = job.getElementsByTagName('binary')[0].childNodes[0].nodeValue
                service += "pid = Run(\"" + bin + "\",email,["
                for a in args:
                    service += "[\"" + a + "\","
                    if a in base64:
                        service += a + "_fn],"
                    else:
                        service  += a + "],"
                if o_file:
                    aux = o_file[0].getElementsByTagName('name')
                    service += "[\"" + aux[0].childNodes[0].nodeValue + "\",output]"
                if namedArgs:
                    service += "],True)\n%s" % tab2
                else:
                    service += "])\n%s" % tab2
                service += "results = Result()\n%s" % tab2
                service += "results.job_id = pid\n%s" % tab2
                service += "results.out = output\n%s" % tab2
                service += "sendmail(email,\"" + serv_name + "\",output)\n%s" % tab2 
                service += "return results%s" % tab2
        fout.write(service)    
        fout.close()
      
