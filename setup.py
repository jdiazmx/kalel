#!/usr/bin/env python
import os
import time
import subprocess
import sys
import pip

# Verify that the user is root
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\nTry with $ sudo python setup.py")

print("Setting up KalEl For You...")

#Create and Copy files to installdir /opt/KalEl
if os.path.isfile('/opt/KalEl/run.py'):
    reinstall = raw_input('KalEl is allready installed!\nDo you want to reinstall? (y/n): ')
    if reinstall == ('y'):
        subprocess.Popen("rm -fr /opt/KalEl", shell=True).wait()
    else:
        exit(1)

print("[*] Copying KalEl into the /opt/KalEl directory...")
cwdpath = os.getcwd()
subprocess.Popen("cp -rf %s /opt/KalEl" % cwdpath, shell=True).wait()

# Create a link in /usr/bin for easy start
print("[*] Installing KalEl installer to /usr/bin/kalel...")
if os.path.isfile("/usr/bin/kalel"):
    subprocess.Popen("rm /usr/bin/kalel", shell=True).wait()
else:
    pass
subprocess.Popen("echo #!/bin/bash > /usr/bin/kalel", shell=True).wait()
subprocess.Popen("echo cd /opt/KalEl >> /usr/bin/kalel", shell=True).wait()
subprocess.Popen("echo exec python2 kalel $@ >> /usr/bin/kalel", shell=True).wait()
subprocess.Popen("cp /opt/KalEl/kalelupdate /usr/bin/", shell=True).wait()
subprocess.Popen("chmod +x /usr/bin/kalel", shell=True).wait()

# Create a symbolic link for launching the toolkit via usr/bin
subprocess.Popen("ln -s /opt/KalEl/run.py /opt/KalEl/kalel", shell=True).wait()

# Write permission to run
subprocess.call(['chmod', '+x', '/opt/KalEl/run.py'])
subprocess.call(['chmod', '+x', '/opt/KalEl/module/harvester/engine.py'])

# Check if config files is present, if they are we will remove them
if os.path.isfile("/opt/KalEl/src/setupOK"):
    subprocess.call(['rm', '/opt/KalEl/src/setupOK'])

if os.path.isfile("/opt/KalEl/src/config.cfg"):
    subprocess.call(['rm', '/opt/KalEl/src/config.py'])

############# CHECK REQUIRED DEPENDENCIES ####################
FNULL = open(os.devnull, 'w')
# Install sendemail for mail spoofing
try:
    subprocess.call(["sendemail"], stdout=FNULL, stderr=subprocess.STDOUT)
except OSError as e:
    if e.errno == os.errno.ENOENT:
        print('sendemail not install, installing now')
        subprocess.call(['sudo', 'apt-get', 'install', '-y', 'sendemail'])
    else:
        print("something else went wrong, try again")
        raise

# Check if ettercap is installed or present
try:
    subprocess.call(["ettercap"], stdout=FNULL, stderr=subprocess.STDOUT)
except OSError as e:
    if e.errno == os.errno.ENOENT:
        print("We cant seem to find ettercap-ng")
        print("Please install ettercap or define it's install directory")
        etterdir = raw_input("Define ettercap installation directory\nexample (default): /usr/bin/ettercap\nDir: ")
        with open("/opt/KalEl/src/config.py", "w") as filewrite:
            filewrite.write("\n#[ETTERCAP DIR]\n")
            filewrite.write("etterdir")
            filewrite.write(" = ")
            filewrite.write("'%s'\n" % etterdir)
    else:
        print("something else went wrong, try again")
        raise

# Install Tor bundle
#subprocess.call(['apt-get', 'install', 'tor', '-y' '-qq'])

# Install dependencies
#pip.main(['install', 'stem'])

# Write setup to src/setupOK to let the tool know setup is complete
with open("/opt/KalEl/src/setupOK", "w") as filewrite:
    filewrite.write("Installed")

print("[*] We are now finished! To run KalEl, type kalel...")
exit(1)