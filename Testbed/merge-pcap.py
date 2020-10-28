import os
import dpkt
import datetime

for host in range(1,15):
    path = './traffic/h' + str(host)

    file_list = os.listdir(path)
    now = datetime.datetime.now()

    for file in file_list:
        sec_to_now = 0
        with open(path + '/' + file, 'rb') as f:
            pcap = dpkt.pcap.Reader(f)
            for ts, buf in pcap:
                packet_time_stamp = datetime.datetime.fromtimestamp(ts)
                sec_to_now = (now - packet_time_stamp).total_seconds()
                break
        name = file.split('.')[0]
        cmd = 'bittwiste -I ' + path + '/' + file + ' -O ' + path + '/' + name + '-ip-changed.pcap' + ' -T ip -s 10.0.0.' + str(host) + ' -d 10.0.0.' + name
        os.system(cmd)
        change_time_cmd = 'editcap -t ' + str(sec_to_now) + ' ' + path + '/' + name + '-ip-changed.pcap' + ' ' + path + '/' + name + '-time-changed.pcap'
        os.system(change_time_cmd)
        change_mac_cmd = 'tcprewrite --infile=' + path + '/' + name + '-time-changed.pcap ' + ' --outfile=' + path + '/' + name + '-final.pcap' + ' --enet-smac=00:00:00:00:01:0' + str(host) + ' --enet-dmac=00:00:00:00:01:0' + name
        os.system(change_mac_cmd)

    command = 'mergecap -w ' + str(host) + '.pcap '
    for file in file_list:
        name = file.split('.')[0]
        command += path + '/' + name + '-final.pcap '

    os.system(command)

    for file in file_list:
        name = file.split('.')[0]
        os.remove(path + '/' + name + '-final.pcap')
        os.remove(path + '/' + name + '-ip-changed.pcap')
        os.remove(path + '/' + name + '-time-changed.pcap')
