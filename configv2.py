from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.arp import ArpTable
from lxml import etree
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

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

host = raw_input('Enter Switch IP: ')
switch_user = raw_input('Enter switch username: ')
switch_password = raw_input('Enter switch password: ')
dev = Device(host='%s' % (host),user='%s' % (switch_user),password='%s' %(switch_password))
dev.open()

globals().update(FactoryLoader().load(yaml.load(yaml_data)))
arp_table = ArpTable(dev)
arp_table.get()

arp_mac = []
for arp in arp_table:
        print 'mac_address: ', arp.mac_address
        print 'ip_address: ', arp.ip_address
        print 'interface_name:', arp.interface_name
        print 'hostname:', arp.host
        print ''
        arp_mac.append(arp.ip_address+'-'+arp.mac_address)

# Compare MACs from ODL and ARP Table
set(odl_macs) & set(arp_mac)

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
dev.close()
