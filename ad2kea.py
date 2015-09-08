__author__ = 'chuyen'

from netaddr import *
import re
import json

AD = "dhcpcfg.txt"
KEA = "kea.json"
pool = []
def main():
    with open(AD, 'r') as msdhcp:
        dhcp_lines = msdhcp.readlines()
    keaconf = open(KEA, 'w')
    for lines in dhcp_lines:
        if 'add scope' in lines:
            vlan = lines.split(" ", 7)
            subnet = IPNetwork(vlan[5]+ "/" + vlan[6])
            # print subnet.cidr, subnet[1]  (gw = subnet index +1 )
            scope_info = re.findall(r'"(.*?)"', vlan[7])
            for lines in dhcp_lines:
                if 'reservedip' in lines:
                     host = lines.split(" ")
                     macaddr = ':'.join(s.encode('hex') for s in host[8].decode('hex'))
                if 'iprange' in lines:
                    scope_range = lines.split(" ")
                    if scope_range[4] in str(subnet):
                        pool = ({ "subnet": str(subnet.cidr), "pools": [ { "pool": str(scope_range[7] + " " + "-" + " " + str(scope_range[8]) ) } ], "option-data": [ { "code": "3" , "name": "routers", "data": str(subnet[1]) } ]}) 
                        keaconf.writelines(json.dumps(pool, indent=4) + "," + "\n")
    keaconf.close()

if __name__ == '__main__':
    main()
