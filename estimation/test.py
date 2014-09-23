
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from pox.openflow.libopenflow_01 import ofp_match
from pox.core import core
import pox.openflow.libopenflow_01 as of
from estimation.timer import Timer
import time
import testData
def entry_for_packet (tables, packet, in_port):
    packet_match = ofp_match.from_packet(packet, in_port, spec_frags = True)
    for entry in tables._table:
        if entry.match.matches_with_wildcards(packet_match,
                                                consider_other_wildcards=False):
            break
def testS():
    with Timer() as time1:
        msg=of.ofp_flow_mod()
        i=0
        while i<10:
            msg.match.dl_type=0x800
            msg.match.dl_src=EthAddr("00:03:0f:01:12:4%s"%i)
            msg.match.nw_proto=6
            msg.match.nw_dst="1.0.0.0/8"
            msg.match.nw_src="1.2.3.4"
            msg.match.tp_src=1
            msg.match.tp_dst=2
            msg.actions.append(of.ofp_action_output(port=194))
            core.openflow.connections[1].send(msg)
            print str(i)+"***"
            i=i+1
    print "=>Time: %s s" % time1.secs
def print_write(strs):
    result=open(r"..\Data\result",'a')
    print strs
    result.write("\n"+strs)
    result.close()
def average ():
    file=open(r"..\Data\result",'r')
    lines=file.readlines()
    p=0
    t=0
    for line in lines:
        if line.find('Entry_for_packet')!=-1:
            tem=line.split('.')
            t=t+int(filter(str.isdigit,tem[0]))
        if line.find('number of packets')!=-1:
            tem=line.split('.')
            p=p+int(filter(str.isdigit,tem[0]))
    return p/t
            
def testC():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    table=testData.GenerateACL()
    packets=testData.GenerateTrace()
    pnum=len(packets)
    tnum=len(table)
    startTime= time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
    print_write(startTime)
    print_write("go!!")
    with Timer() as time2:
        for packet in packets:
            entry_for_packet(table, packet, 1)
    times=time2.secs
    print_write( "=>Time of Entry_for_packet: %s s" %  times)
    print_write( "The size of table is :%s"%tnum)
    print_write( "The number of packets is:%s "%pnum)
    print_write( "The speed is:%s packet/s"%(int(pnum/times)))
    print_write("The averate speed is:%s packet/s"%average())
    endTime = time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
    print_write( endTime)
    print_write( "end.\n**************************************")
