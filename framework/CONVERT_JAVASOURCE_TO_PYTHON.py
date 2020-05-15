
import glob
import os 
import re
import subprocess

if not os.path.exists('./tmp'):
    os.mkdir('./tmp')

javaSources = glob.glob('./java/src/framework/*.java')

classNames = [os.path.splitext(os.path.basename(javaSource))[0] 
    for javaSource in javaSources ]

classNames.remove("Main")
classNames.remove("MyArray")
classNames.remove("Utils")

newSourceName = "./tmp/framework.py"
txtNew = """\
from MyArray import MyArray
from Utils import Utils

"""
for className in classNames:

    print(className)

    pythonSourceName = "./tmp/%s.py" % className

    cmd = (
        r"C:\Python27\python.exe",
        r"C:\Python27\Scripts\j2py", 
        r"./java/src/framework/%s.java" % className,
        pythonSourceName)

    subprocess.run(cmd)

    with open(pythonSourceName, 'r') as fp:
        txt = fp.read()
        ptn = r"(class.*\n)(((.*)\n)*?)(\s*def)"
        txt = re.sub(ptn, "\g<1>\g<5>", txt) + "\n"

        txt = txt.replace(r"#!/usr/bin/env python", "")

        txtNew += txt

with open(newSourceName, "w", encoding="utf-8") as fp:
    fp.write(txtNew)

