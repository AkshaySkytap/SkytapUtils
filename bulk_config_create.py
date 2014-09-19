#! /usr/bin/python

import sys
import requests
import json
import time

def print_usage():
	print "Usage: " + sys.argv[0] + " <template id> <number of instances> <optional configuration name prefix>"

username = "akshay_devqa"
apikey = "356d63b765b9962c3f01d4b9ff6cf2053c0ad2b8"
skytap_url = "https://cloud.skytap.com"
config_url = skytap_url + "/configurations"
template_url = skytap_url + "/templates"
user_url = skytap_url + "/users"

# Standard headers
headers = {
	"Accept": "application/json",
	"Content-Type": "application/json"
	}

# Assuming we use username and api key for authentication
auth = ( username, apikey )
if (apikey.strip() == ""):
	auth = (username, password)

if (len(sys.argv) < 3):
	print_usage()
	sys.exit()

template_id = sys.argv[1]
num_instances = int(sys.argv[2])
config_prefix = ""

if (len(sys.argv) > 3):
	
	for x in range(3, len(sys.argv)):
		config_prefix += " " + sys.argv[x]

	config_prefix = config_prefix.strip()

print "Config ID: " + template_id
print "Number of Instances: %d" % num_instances
print "Config Prefix: " + config_prefix

# First get the template
rsp = requests.get(template_url + "/" + template_id, headers = headers, auth = auth)

if (rsp.status_code == 200):
	json_rsp = json.loads(rsp.text)
	if (config_prefix.strip() == ""):
		config_prefix = json_rsp['name']
		print "Since Configuration Prefix was not set, setting it to template name: " + config_prefix
else:
	print "Error: Could not access template with ID: " + template_id
	sys.exit(1)


for x in range(0, num_instances):
	config_name = config_prefix + (" - %d" % (x + 1))
	print "Creating Environment '" + config_name + "'"

	data = {
		"name" : config_name
	}

	rsp = requests.post(config_url + "?template_id=" + template_id, headers = headers, auth = auth, data = json.dumps(data))
	if (rsp.status_code == 200):
		json_rsp = json.loads(rsp.text)
		print "Created Config '%s' with ID '%s'.  Now Changing Run State to 'running'." % (json_rsp['name'], json_rsp['id'])


		data = { "runstate" : "running" }
		rsp = requests.put(config_url + "/" + json_rsp['id'], headers = headers, auth = auth, data = json.dumps(data))
		if (rsp.status_code == 200):
			print "Config now running!"
		else:
			print "ERROR: Could not run config."

	time.sleep(5)