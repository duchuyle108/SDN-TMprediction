
# This is a basic forwarding component used in the article:
#  "An AI-based Traffic Matrix Prediction Solution for Software-Defined Network" 
#  Authors: Duc-Huy LE, Hai Anh TRAN, Sami SOUIHI, Abdelhamid MELLOUK
#  Conference: ICC2021

# The component is derived from l2_forwarding component of pox with simpler flow rule
# with the only three matching field: protocol, Source IP Address, Destination IP Address.


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
from pox.lib.addresses import IPAddr
import time

log = core.getLogger()

class LearningSwitch (object):
  
  def __init__ (self, connection):
    self.connection = connection

    self.macToPort = {}
    # Listen for connection
    connection.addListeners(self)

  def _handle_PacketIn (self, event):

    packet = event.parsed

    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.macToPort[packet.src] = event.port

    if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
      drop()
      return

    if packet.dst.is_multicast:
      flood()
    else:
      if packet.dst not in self.macToPort: 
        flood("Port for %s unknown -- flooding" % (packet.dst,))
      else:
        port = self.macToPort[packet.dst]
        if port == event.port:
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.match.tp_dst = None
        msg.match.tp_src = None
        msg.match.dl_src = None
        msg.match.dl_dst = None
        msg.match.nw_proto = None
        msg.actions.append(of.ofp_action_output(port = port))
        msg.data = event.ofp
        self.connection.send(msg)
        
class basic_forwarding (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self):
    """
    Initialize
    """
    core.openflow.addListeners(self)

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection)


def launch ():
  core.registerNew(basic_forwarding)
