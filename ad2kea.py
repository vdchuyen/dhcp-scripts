__author__ = 'chuyen'

import csv
from netaddr import *
import re

AD = "dhcpcfg.txt"
KEA = "kea.json"

def main():
    with open(AD, 'r') as addhcp_src:
        dhcp_lines = addhcp_src.readlines()
    dhcp_dst = open(KEA, 'w')
    for lines in dhcp_lines:
        if 'add scope' in lines:
            vlan = lines.split(" ", 7)
            subnet = IPNetwork(vlan[5]+ "/" + vlan[6])
            # print subnet.cidr, subnet[1]  (gw = subnet index +1 )
            scope_info = re.findall(r'"(.*?)"', vlan[6])
            for lines in dhcp_lines:
                if 'reservedip' in lines:
                     host = lines.split(" ")
                     macaddr = ':'.join(s.encode('hex') for s in host[8].decode('hex'))
                if 'iprange' in lines:
                    scope_range = lines.split(" ")
                    if scope_range[4] in str(subnet):
                        dhcp_src = "#" + " ".join(scope_info) + "\n" +  "{" + "\n" + "\t" + "\"subnet\"" + ":" + " " +  "\"" + str(subnet.cidr) + "\"" + "," + "\n" + "\t" + "\"pools\"" + ":" + " " + "[" + " " + "{" + "\"pool\"" + ":" + " " +  "\"" + str(scope_range[7]) + " " + "-" + " " + str(scope_range[8]) + "\""  +  "}" + "]" + "," + "\n" + "\t" +  "\"option-data\"" + ":" + " " + "[" + "{" + "\n" + "\t" + "\"code\"" + ":" + " " + "3" + "," + "\n" + "\t" + "\"name\"" + ":" + " " + "\"routers\"" + "," + "\n" + "\t" + "\"data\"" + ":" + " " + "\"" + str(subnet[1]) + "\"" + "\n" + "\t" + "}" + "]" + "\n" +  "}" + ","
                        # print dhcp_src           
                        dhcp_dst.writelines(dhcp_src)
    dhcp_dst.close()

if __name__ == '__main__':
    main()
