from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
from pox.lib.recoco import Timer
from pox.lib.packet.packet_utils import *
from pox.lib.addresses import IPAddr, parse_cidr

import numpy as np
import os.path
import time
import csv
from copy import deepcopy
from datetime import datetime

log = core.getLogger()

node_num = 14

latest_traffic = np.zeros((node_num, node_num), dtype=object)

class TrackedSwitch(object):
    def __init__ (self, connection):
        # Switch we'll be adding L2 learning switch capabilities to
        self.connection = connection
        connection.addListeners(self)
    
    def _handle_FlowStatsReceived (self, event):
        dpid = event.connection.dpid
        stats = event.stats
        traffic = np.zeros(node_num, dtype=object)
        for flow in stats:
            match = flow.match
            if match.nw_src == IPAddr("10.0.0.%d" %dpid):
                traffic[int(match.nw_dst.toStr().split('.')[3]) - 1] += flow.byte_count
        latest_traffic[int(dpid) - 1] = traffic
        
class traffic_observation(object):
    def __init__ (self, output, interval):
        self.output = output
        self.interval = interval
        self.switches = []
        self.previous_traffic = []
        self.start_time = time.time()
        self.tm_flag = 0
        core.openflow.addListeners(self)
    
    def tm_cal(self):
        self.query_all_switches()
        time.sleep(1)
        if self.tm_flag == 0:
            log.info("Calculating Traffic Matrix!")
            self.start_time = time.time()
            self.previous_traffic = deepcopy(latest_traffic)
            self.tm_flag = 1
            Timer(2,self.tm_cal)
        else:
            duration = time.time() - self.start_time
            dif_matrix = latest_traffic - self.previous_traffic
            traffic_matrix = dif_matrix / int(duration)
            log.info("Traffic Matrix: \n" + str(traffic_matrix))
            if self.output is not None:
                with open(self.output, 'a') as f:
                    f.write(datetime.now().strftime(format = '%Y-%m-%d %H:%M:%S,'))
                    np.savetxt(f, traffic_matrix.ravel()[None], delimiter=',', fmt = '%s')
            self.tm_flag = 0
            Timer(float(self.interval),self.tm_cal)

    def _handle_ConnectionUp (self, event):
        self.connection = event.connection
        self.switches.append(event.connection)
        TrackedSwitch(event.connection)

    def query_all_switches(self):
        if self.switches:
            for i in range(len(self.switches)):
                self.stats_request(self.switches[i])
        
    def stats_request(self, switch):
        switch.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def launch(output=None, interval = 60):
    log.info('Collecting data from flow')
    if output is not None:
        if not os.path.isfile(output):
            with open(output, 'w') as f:
                pass
    ob = core.registerNew(traffic_observation, output, interval)
    core.traffic_observation.tm_cal()
    



# python pox.py openflow.spanning_tree --no-flood --hold-down openflow.discovery basic_forwarding traffic_observation --output=.... --interval=...