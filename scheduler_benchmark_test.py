import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
import novaclient.v1_1.client as nvclient
import credentials
import time
import sys
 
if len(sys.argv) > 1:
	filename = sys.argv[1]
 
def run_test(filename):
	test_properties = read_config(filename)
	num_repeat_instance_creation = test_properties["num_repeat_instance_creation"]
	repeat_time_interval = test_properties["repeat_time_interval"]
	if num_repeat_instance_creation:
		for i in range(int(num_repeat_instance_creation) + 1):
			print "creating: " + str(i)
			create_instances(test_properties)
			time.sleep(test_properties["repeat_time_interval"])
 
def read_config(filename):
	default_flavor = "m1.micro"
	default_num_instances = 1
	default_num_existing_hypervisors = 1
	default_num_repeat_instance_creation = 0
	default_repeat_time_interval = 0
 
	test_properties = {
		"num_instances" : default_num_instances,
		"num_existing_hypervisors" : default_num_existing_hypervisors,
		"num_instances_of_flavor" : {default_flavor : default_num_instances},
		"num_repeat_instance_creation" : default_num_repeat_instance_creation,
		"repeat_time_interval" : default_repeat_time_interval
	}
	with open(filename, 'r') as f:
		for line in f:
			key_value = line.split("=")
			if len(key_value) == 2:
				if key_value[0].strip() == "num_instances_of_flavor":
					test_properties["num_instances_of_flavor"] = eval(key_value[1].strip())
				else:
					test_properties[key_value[0].strip()] = int(key_value[1].strip())
	print test_properties
	return test_properties
 
def create_instances(test_properties):
	# (sri) Add creation of test environment here
 
	default_name = "ubuntu"
 
	keystone_creds = credentials.get_keystone_creds()
	#Get images containing Ubuntu
	keystone = ksclient.Client(**keystone_creds)
	glance_endpoint = keystone.service_catalog.url_for(
	                                    service_type='image',
	                                    endpoint_type='publicURL')
	glance = glclient.Client(glance_endpoint, token=keystone.auth_token)
	ubuntu_images = [ img for img in glance.images.list() 
	                            if default_name in img["name"]]
	#Create images
	nova_creds = credentials.get_nova_creds()
	nova = nvclient.Client(**nova_creds)
	for flavor_name, num_instances_of_flavor in test_properties["num_instances_of_flavor"].iteritems():
		flavor = nova.flavors.find(name=flavor_name)
		created_instances = [
		        nova.servers.create(name=img["name"]+"_vm",
		                            image=img["id"],
		                            flavor=flavor,
		                            max_count=num_instances_of_flavor)
		        for img in ubuntu_images
		        ]
		        
if __name__ == "__main__":
	run_test(filename)
