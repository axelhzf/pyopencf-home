import os
import sys

pid = os.fork()

if pid:
	print pid
	exit(1)

try:
	a = os.system(sys.argv[2])
except:
	print "Error","*",sys.argv[0],"*",sys.argv[1],"*",sys.argv[2]

