# CIS347 Group 5

Make sure you have python installed.

Run the "final.py" script like this: python final.py

It will ask you for your ODL IP + login and Juniper switch login.

This script will login to your ODL and output the IP + MAC of your connected nodes. It will then login to your switch and cross-reference the MACs on your EthernetSwitchingTable. It will lock down the ports to the specific MACs that match with the ODL MACs.