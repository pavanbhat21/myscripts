#!/usr/bin/python

from avocado import Test
from avocado import main
from avocado.utils import process
import re, os, imp, vagrant, pexpect
vsm = imp.load_source('vsm', '/home/pavan/tests/cdk_tests/new/vsm.py')
vagrant_lib = imp.load_source('vagrant_lib', '/home/pavan/tests/cdk_tests/new/vagrant_lib.py')


class VSM(Test):
    def setUp(self):
        self.vagrant_BOX_PATH = self.params.get('vagrant_BOX_PATH')
	self.vagrant_PLUGIN_PATH = self.params.get('vagrant_PLUGIN_PATH')	
	self.service = self.params.get('service', default='')
        self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='')
	os.chdir(self.vagrant_BOX_PATH)
	self.v = vagrant.Vagrant(self.vagrant_BOX_PATH)
    
    def test_vagrant_up(self):
	''' bring up vagrant box '''
	self.v.destroy()
        cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
        child = pexpect.spawn ('vagrant up')
        child.expect('.*Would you like to register the system now.*')
        child.sendline ('y')
        child.expect('.*username.*')
        child.sendline('self.vagrant_RHN_USERNAME')
        child.expect('.*password.*')
        child.sendline('self.vagrant_RHN_PASSWORD')
	

    def est_plugin_install(self):	
	''' test to install the vagrant plugins '''
	os.chdir(self.vagrant_PLUGIN_PATH)
	output = vsm.vsm_plugin_install()
	self.log.info(output)
	self.assertIn("Installed the plugin", output.stdout)	
    
    def test_vsm_box_version(self):
	''' test to get box version '''
	output = vsm.vsm_box_info(self.vagrant_BOX_PATH, "version", "--script-readable")
        self.log.info(output)
	self.assertIn("Container Development Kit (CDK)", output.stdout)


    def test_vsm_box_ip(self):
        ''' test to get box IP '''
        output = vsm.vsm_box_info(self.vagrant_BOX_PATH, "ip", "")
        self.log.info(output)
        self.assertIn("10.1.2.2", output.stdout)


    def test_vsm_env_info(self):
	''' test to get info about services '''
	output = vsm.vsm_env_info(self.vagrant_BOX_PATH, self.service)
	self.log.info(output)
	self.assertIn("eval", output.stdout)


    def test_vsm_service_status_isrunning(self):
        ''' test to confirm service status '''
	#output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", self.service)
        #self.log.info(output)
        #self.assertEqual("%s - running\n" %(self.service), output.stdout)
	output = vsm.vsm_is_service_running(self.vagrant_BOX_PATH, self.service)
	self.assertTrue(output)

    def test_vsm_service_status_isstopped(self):
        ''' test to get service status '''
        output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "status", self.service)
        self.log.info(output)
        self.assertEqual("%s - stopped\n" %(self.service), output.stdout)

    def test_vsm_service_restart(self):
        ''' test to restart services '''
	output = vsm.vsm_service_handling(self.vagrant_BOX_PATH, "restart", self.service)
        self.log.info(output)
	self.test_vsm_service_status_isrunning()

if __name__ == "__main__":
    main()


