import os
import dpkt
import datetime

for host in range(1,15):
    path = './traffic2/h' + str(host)

    file_list = os.listdir(path)

    for file in file_list:
        name = file.split('.')[0]
        cmd = 'bittwiste -I ' + path + '/' + file + ' -O ' + path + '/' + name + '-ip-changed.pcap' + ' -T ip -s 10.0.0.' + str(host) + ' -d 10.0.0.' + name
        os.system(cmd)
        change_mac_cmd = 'tcprewrite --infile=' + path + '/' + name + '-ip-changed.pcap ' + ' --outfile=' + path + '/' + name + '.pcap' + ' --enet-smac=00:00:00:00:01:0' + str(host) + ' --enet-dmac=00:00:00:00:01:0' + name
        os.system(change_mac_cmd)

    for file in file_list:
        name = file.split('.')[0]
        os.remove(path + '/' + name + '-ip-changed.pcap')
