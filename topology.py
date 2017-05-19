import requests

#OpenDayLight RESTCONF API settings.
# Add user input for odl IP and user/pass?
odl_ip = raw_input("Enter your OpenDayLight IP: ")
username = raw_input('Enter ODL username: ')
password = raw_input('Enter ODL password: ')

odl_url = 'http://' + odl_ip + ':8181/restconf/operational/network-topology:network-topology'
odl_username = username
odl_password = password

# Fetch information from API.
response = requests.get(odl_url, auth=(odl_username, odl_password))

# Find information about nodes in retrieved JSON file.
for nodes in response.json()['network-topology']['topology']:

    	# Walk through all node information.
        node_info = nodes['node']

	# Look for MAC and IP addresses in node information.
	for node in node_info:
		try:
			#node_id = node['host-tracker-service:attachment-points'][0]['corresponding-tp']
			ip_address = node['host-tracker-service:addresses'][0]['ip']
			mac_address = node['host-tracker-service:addresses'][0]['mac']
			#print 'Found host %s with MAC address %s and IP address %s' % (node_id, mac_address, ip_address)
			odl_parse = 'Found host with MAC address %s and IP address %s' % (mac_address, ip_address)
			print odl_parse
		except:
			pass

#mac = raw_input('Which MAC address would you like to select? ')
# make input go to config script to cross reference with the ethernetswitchingtable.




