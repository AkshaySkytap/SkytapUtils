#! /usr/bin/python

'''
Copyright 2014 Skytap Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#-----------------------------------------------------------------------
A python script to run a create multiple configurations from a single template.
The script takes a minimum of 2 arguments:
	1) Template ID: The ID of the template to create the configurations from
	2) Number of Instances: Number of configurations to make

Anything after the 2nd argument will be treated as an optional 3rd argument which
is the name of the generated configurations.  If nothing is supplied, it will default
to the template name.  Once each configuration is created, the final name will be
appended with a hyphen and number signifying where in the order it was created.

This code was tested with python 2.7.5

Note: requires the requests python module which is
open source (Apache2 licensed) and can be installed via Pip
'''

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