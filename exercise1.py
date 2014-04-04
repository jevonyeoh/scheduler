import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as novaclient	
import glanceclient.v2.client as glanceclient

# define credentials
def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'password'
    d['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
    d['tenant_name'] = 'demo'
    return d

def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = 'password'
    d['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
    d['project_id'] = 'demo'
    return d

kscreds = get_keystone_creds()
novacreds = get_nova_creds()

# establish connections
ks = ksclient.Client(**kscreds)
glance_endpoint = ks.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
glance = glanceclient.Client(glance_endpoint, token=ks.auth_token)
nova = novaclient.Client(**novacreds)

# find images with ubuntu in it
images = glance.images.list()
for i in images:
	if "ubuntu" in i["name"]:
		print "image found: " + i["name"]
		imageToCreate = i

# create VM
flavor = nova.flavors.find(name="m1.micro")
newInstance = nova.servers.create(name="scriptCreatedServer", image=imageToCreate, flavor=flavor, min_count=5)