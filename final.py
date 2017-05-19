import requests
import yaml
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.arp import ArpTable
from jnpr.junos.factory.factory_loader import FactoryLoader

#OpenDayLight RESTCONF API settings.
odl_ip = raw_input("Enter your OpenDayLight IP: ")
username = raw_input('Enter ODL username: ')
password = raw_input('Enter ODL password: ')
odl_url = 'http://' + odl_ip + ':8181/restconf/operational/network-topology:network-topology'
odl_username = username
odl_password = password

# Fetch information from API.
response = requests.get(odl_url, auth=(odl_username, odl_password))

# Find information about nodes in retrieved JSON file.
odl_macs = []
for nodes in response.json()['network-topology']['topology']:

    	# Walk through all node information.
        node_info = nodes['node']

	# Look for MAC and IP addresses in node information.
	for node in node_info:
		try:
			ip_address = node['host-tracker-service:addresses'][0]['ip']
			mac_address = node['host-tracker-service:addresses'][0]['mac']
			odl_parse = 'Found host with MAC address %s and IP address %s' % (mac_address, ip_address)
			odl_macs.append(mac_address)
			print odl_parse
		except:
			pass

# Part 2 ---------------------------------------------------------------------------------------------------


yaml_data="""
---
ArpTable:
  rpc: get-arp-table-information
  item: arp-table-entry
  key: mac-address
  view: ArpView
ArpView:
  fields:
    mac_address: mac-address
    ip_address: ip-address
    interface_name: interface-name
    host: hostname
"""
# Login to switch
host = raw_input('Enter Switch IP: ')
switch_user = raw_input('Enter switch username: ')
switch_password = raw_input('Enter switch password: ')
dev = Device(host='%s' % (host),user='%s' % (switch_user),password='%s' %(switch_password))
dev.open()

# Retrieve ArpTable info
globals().update(FactoryLoader().load(yaml.load(yaml_data)))
arp_table = ArpTable(dev)
arp_table.get()

# Organize Arp entries
arp_mac = []
for arp in arp_table:
        print 'mac_address: ', arp.mac_address
        print 'ip_address: ', arp.ip_address
        print 'interface_name:', arp.interface_name
        print 'hostname:', arp.host
        print ''
        arp_mac.append(arp.interface_name+'|'+arp.mac_address)

# Compare MACs from ODL and ARP Table
#check = list(set(odl_macs) & set(arp_mac))
arp_set = [i for e in odl_macs for i in arp_mac if e in i]
port_interface = [i.split('|', 1)[0] for i in arp_set]
port_mac = [i.split('|', 1)[1] for i in arp_set]

# Automate the port security for each entry in final list.
print arp_set
port_security = raw_input('These MACs match your ODL flow MACs. Would you like to bind these MACs to their current interface? (yes or no) ')
if port_security.lower() = 'yes':
	config_add =[]
	for i in arp_set:
		 interface = [i.split('|', 1)[0]]
		 mac = [i.split('|', 1)[1]]
		 config_add.append('set interface %s allowed-mac %s' % (interface, mac))
	set_add = '\n'.join(map(str,config_add))

	config_script = """
	edit ethernet-switching-options secure-access-port
	%s
	""" % (set_add)

	cu = Config(dev)
	cu.load(config_script, format="set", merge=True)
	print 'These are the changes:\n ' + cu.diff()
#	print cu.diff()
	cu.commit()
	print "Configuration Successful! Goodbye."
	dev.close()
else:
	print "Too bad. Switch, out."
	dev.close()