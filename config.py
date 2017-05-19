from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.arp import ArpTable
#from jnpr.junos.op.ethport import EthernetSwitchingTable
from lxml import etree

host = raw_input('Enter Switch IP: ')
switch_user = raw_input('Enter switch username: ')
switch_password = raw_input('Enter switch password: ')
dev = Device(host='%s' % (host),user='%s' % (switch_user),password='%s' %(switch_password))
#eth = dev.rpc.get-ethernet-switching-table-information(normalize=True)
# dev = Device(host='192.168.140.240', user='root', password='admin12345')
dev.open()

# Get arptable from switch
arp_table = dev.get_arp_table_information(normalize=True)
# Print response of device
print (etree.tostring(arp))

# Get EthernetSwitchingTable output working
#ethswitch = EthernetSwitchingTable(dev)
#ethswitch.get()

# Port Security Config
# Apply %s for script Mac address
'''config_script = """
edit ethernet-switching-options secure-access-port
set interface ge-0/0/46 allowed-mac 8C:AE:4C:F4:6B:50
""" '''
interface = raw_input("Enter port number (0-47): ")
mac = raw_input("Enter MAC Address to allow on the port: ")
config_script = """
edit ethernet-switching-options secure-access-port
set interface ge-0/0/%s allowed-mac %s
""" % (interface, mac)

cu = Config(dev)
cu.load(config_script, format="set", merge=True)
print cu.diff()
cu.commit()
print "Configuration Successful! Goodbye."
#pprint dev.cli('show ethernet-switching-options')
dev.close()
#show ethernet-switching-options