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
def testS():
        msg=of.ofp_flow_mod()
        i=0
        while i<=10:
            msg.priority=i
            msg.actions.append(of.ofp_action_output(port=194))
            core.openflow.connections[1].send(msg)
            print str(i)+"***"
            i=i+1
def testC():
    def entry_for_packet (tables, packet, in_port):
        packet_match = ofp_match.from_packet(packet, in_port, spec_frags = True)
        for entry in tables._table:
            if entry.match.matches_with_wildcards(packet_match,
                                                  consider_other_wildcards=True):
                print"match"
        print "notmatch"
    t = FlowTable()
    t.add_entry(TableEntry(priority=6, cookie=0x1, match=ofp_match(dl_src=EthAddr("00:00:00:00:00:01"),nw_src="1.2.3.4"), actions=[ofp_action_output(port=5)]))
    t.add_entry(TableEntry(priority=5, cookie=0x2, match=ofp_match(dl_src=EthAddr("00:00:00:00:00:02"), nw_src="1.2.3.0/24"), actions=[ofp_action_output(port=6)]))
    packet = ethernet(
        src=EthAddr("00:00:00:00:00:01"),
        dst=EthAddr("00:00:00:00:00:02"),
        payload=ipv4(srcip=IPAddr("1.2.3.4"),
        dstip=IPAddr("1.2.3.5"),
        payload=udp(srcport=1234, dstport=53, payload="haha")))
    if packet is None:
        print "packet is none"
    else:
        entry_for_packet(t, packet, 1)