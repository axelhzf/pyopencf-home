import sys
import os

DEBUG = 1
WARN  = 2
ERROR = 3
 
# The FQDN of the server
server_name = 'PYOPENCF_SERVER'

# The URL of the web service
ws_url = "http://url/"

# sendmail path
SENDMAIL = '/usr/sbin/sendmail'

# Always send an email
SEND = False

# Absolute path to this module
# Leave it if you want to use environment information
OPENCF_BASE = ''

# Relative directory to xml files
XML_DIR = 'Xml'

# Relative directory to libraries
INCLUDE_DIR = 'include'

# Relative directory to templates
SKEL_DIR = 'skel'

# Relative directory to problems
PROBLEMS_DIR = 'problems'

# Relative directory where outputs will be stored
OUTPUT_DIR = 'results'

# Log options
# Path and filename of log file
LOG_FILE = 'pyopencf.log'
# DEBUG = All verbose - by defect
# WARN  = Only warn and error messages will be shown 
# ERROR = Only error messages will be shown
LOG_LEVEL = DEBUG

# Queue manager
# Options: NOQMGR, PBS
# Not implemented yet
QUEUE_MGR = 'NOQMGR'

# User for sudo
S_USER = ''
S_PASS = ''
SUDO = '/usr/bin/sudo -u' + S_USER + ' -p' + S_PASS

if (OPENCF_BASE == ''):
	OPENCF_BASE = os.path.dirname(os.path.abspath(sys.argv[0]))

# Application path constants
xml_dir = OPENCF_BASE + '/' + XML_DIR
problems_dir = OPENCF_BASE + '/' + PROBLEMS_DIR
include_dir = OPENCF_BASE + '/' + INCLUDE_DIR
skel_dir = OPENCF_BASE + '/' + SKEL_DIR
output_dir = OPENCF_BASE + '/' + OUTPUT_DIR
bin_dir = OPENCF_BASE + '/bin'
