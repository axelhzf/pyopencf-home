#!/usr/bin/python
# encoding: utf-8

from suds.client import Client
proxy = Client("http://localhost:8023/pyocfathome.wsdl")
res =  proxy.service.newJob("http://localhost:8045/abbs.wsdl")

print res
