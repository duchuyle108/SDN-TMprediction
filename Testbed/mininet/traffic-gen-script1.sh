#!bin/bash
pingall

h1 for file in prepared-pcaps/h1/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h1-eth0 --pps=10 $file & done

h2 for file in prepared-pcaps/h2/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h2-eth0 --pps=8 $file & done

h3 for file in prepared-pcaps/h3/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h3-eth0 --pps=5 $file & done

h4 for file in prepared-pcaps/h4/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h4-eth0 --pps=12 $file & done

h5 for file in prepared-pcaps/h5/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h5-eth0 --pps=11 $file & done

h6 for file in prepared-pcaps/h6/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h6-eth0 --pps=15 $file & done

h7 for file in prepared-pcaps/h7/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h7-eth0 --pps=6 $file & done

h8 for file in prepared-pcaps/h8/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h8-eth0 --pps=9 $file & done

h9 for file in prepared-pcaps/h9/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h9-eth0 --pps=13 $file & done

h10 for file in prepared-pcaps/h10/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h10-eth0 --pps=14 $file & done

h11 for file in prepared-pcaps/h11/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h11-eth0 --pps=14 $file & done

h12 for file in prepared-pcaps/h12/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h12-eth0 --pps=16 $file & done

h13 for file in prepared-pcaps/h13/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h13-eth0 --pps=8 $file & done

h14 for file in prepared-pcaps/h14/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=1000 -i h14-eth0 --pps=7 $file & done
