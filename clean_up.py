#!/usr/bin/python

import os, subprocess
import sys
from avocado.utils import process
HOST_PLATFORM="FEDORA"
INSTALL_DIR="/home/pavan/Downloads/20160630"

def refresh_pools():
    pool_get = "sudo virsh pool-list | egrep -v 'Autostart|------|^$' | awk '{print $1}'"
    print "Refreshing storage pools.."
    out = process.run(pool_get, shell=True)
    for pool in out.stdout.split():
        pool_refresh = "sudo virsh pool-refresh %s" %(pool)
        out = process.run(pool_refresh, shell=True)
        print "Storage pool %s refreshed." %(pool)


def destroy_old_box():
    #cmd = "vagrant global-status | awk '/default/ {print $NF}'"
    cmd = "vagrant global-status"
    destroy = "vagrant destroy -f && rm -fr .vagrant/"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
	if "default" in line:
    	    dir = line.split()[4]   
	    try:
	        print "print ;;;;;;", dir
	        '''os.chdir(dir)
	        q = subprocess.Popen(destroy, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	        out, err = q.communicate()
	        print "Destroying vagrant box from %s" %(dir)
	        '''
	    except:
	        print "Error destroying Vagrant Box from %s" %(dir)
   
def remove_box():
    cmd = "vagrant box list | awk '{print $1}'"
    out = process.run(cmd, shell=True)
    print "Removing box %s" %(out.stdout.split())
    if "There are no installed boxes" NOT in out.stdout:
	for box in out.stdout.split():
            cmd_remove = "vagrant box remove %s" %(box)
	    try:
                process.run(cmd_remove, shell=True)
            except:
                print "Error deleting box.."

def remove_image():
    remove_img = "sudo rm -fr /var/lib/libvirt/images/*_0.img && sudo systemctl restart libvirtd"    
    try:
	process.run(remove_img, shell=True)
    except:
	print "Error deleting images.."

if __name__ == "__main__":
    if HOST_PLATFORM == "FEDORA":
	refresh_pools()
	destroy_old_box()
	remove_box()
	remove_image()


 
