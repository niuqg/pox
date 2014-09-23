'''
Created on Sep 19, 2014

@author: niuni
'''
from pox.openflow.flow_table import FlowTable
from pox.openflow.flow_table import TableEntry
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from pox.openflow.libopenflow_01 import ofp_match
from pox.openflow.libopenflow_01 import ofp_action_output
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.udp import udp
from estimation.timer import Timer
import socket
import struct
import ctypes
def ip2long (ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]
def long2ip (lint):
    return socket.inet_ntoa(struct.pack("!I", lint))
def GenerateACL():
    acl_rules=open(r'..\Data\acl3_4k_rules.txt')
    table = FlowTable()
    i=3874
    while True:
        r=acl_rules.readline().split()
        if not r:break
        table.add_entry(TableEntry(priority=i, cookie=0x1, match=ofp_match(dl_src=EthAddr("00:00:00:00:00:01"),nw_src=r[0],nw_dst=r[1]), actions=[ofp_action_output(port=5)]))
            #table.add_entry(TableEntry(priority=i, cookie=0x1, match=ofp_match(dl_src=EthAddr("00:00:00:00:00:01"),nw_src="53.45.14.183/32",nw_dst="18.184.25.126/32"), actions=[ofp_action_output(port=5)]))
        i=i-1
    return table
def GenerateTrace():
    acl_trace=open(r'..\Data\acl3_4k_rules.txt_trace')
    trace=acl_trace.readlines()
    packets=[]
    for line in trace:
        tum=line.split()
        src=long2ip(long(tum[0]))
        dst=long2ip(long(tum[1]))
        packet = ethernet(
                          src=EthAddr("00:00:00:00:00:01"),
                          payload=ipv4(srcip=IPAddr(src),
                                       dstip=IPAddr(dst),
                                       payload=udp(srcport=1234, dstport=53, payload="haha")))
        packets.append(packet)
    return packets
'''
t=GenerateACL()
table=t._table
for i in range(0,len(table)):
    print "priority is :%s"%(table[i].effective_priority)
    print table[i].match
    print "************************************8"
print len(t._table)
'''