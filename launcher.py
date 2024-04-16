import subprocess

subprocess.Popen('py m1.py',
                 creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen('py m2.py',
                 creationflags=subprocess.CREATE_NEW_CONSOLE)
subprocess.Popen('py m3.py',
                 creationflags=subprocess.CREATE_NEW_CONSOLE)
