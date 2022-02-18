#!/usr/local/bin/python3

import os
import subprocess

venv_path = os.path.join(os.getcwd(),"api", "api", "venv", "bin","activate")

print(venv_path)

if os.path.isfile(venv_path):
	print(subprocess.Popen("echo $SHELL", shell=True, stdout=subprocess.PIPE))
	#subprocess.Popen(f'source (venv_path)', shell=True, executable='/bin/bash',  stdout=subprocess.PIPE)
	
	subprocess.Popen(['/bin/bash/ source', venv_path])
	
	subprocess.Popen("api/api/venv/bin/flask run", shell=True, executable='/bin/bash',  stdout=subprocess.PIPE)
