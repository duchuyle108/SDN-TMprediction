from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time

def bso():
    net = Mininet(controller=RemoteController)

    node_num = 14

    # Create switches
    for i in range(1, node_num + 1):
        net.addSwitch('s%d' %i)

    # Create nodes
    for i in range(1, node_num + 1):
        if i < 10:
            net.addHost('h%d' %i, ip = '10.0.0.%d' %i, mac = '00:00:00:00:01:0%d' %i)
        else:
            net.addHost('h%d' %i, ip = '10.0.0.%d' %i, mac = '00:00:00:00:01:%d' %i)

    print "*** Creating host-switch links"
    for i in range(1, node_num + 1):
        net.addLink('h%d'%i, 's%d' %i, cls=TCLink, bw=20)

    print "*** Creating switch-switch links"
    link_from = [1,2,2,2,2,2,3,3,5,7,8,8,9,9,10,11,12,13]
    link_to = [2,3,4,5,7,8,4,5,6,9,9,12,10,13,11,13,13,14]

    for lf, lt in zip(link_from, link_to):
        net.addLink('s%d' % int(lf), 's%d' % int(lt), cls=TCLink, bw=30)

    # Add Controllers
    c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    net.start()

    #Wait for controller to update paths in network
    time.sleep(10)

    #Run traffic generator script
    CLI(net, script='traffic-gen-script1.sh')
    CLI( net )

    for host in net.hosts:
        print(host)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    bso()