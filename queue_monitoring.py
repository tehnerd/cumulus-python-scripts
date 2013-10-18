#!/usr/bin/python

import subprocess
import socket
import re
import sys
import time
from string import join

HOSTNAME=socket.gethostname().split('.')[0]
BCM_SHELL = '/usr/lib/cumulus/bcmcmd'
CMD = 'show counters changed'
SRC_ADDR = ('0.0.0.0',1165)
STATSD_SERVER_IP = sys.argv[1]
STATSD_PORT = 8125
STATSD_SERVER = (STATSD_SERVER_IP,STATSD_PORT)

statsd_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
statsd_socket.bind(SRC_ADDR)

egress_queue_pkt_re = re.compile('UC_PERQ_PKT\((\d{1})\)\.(.+?)\t:.*')
egress_queue_byte_re = re.compile('UC_PERQ_BYTE\((\d{1})\)\.(.+?)\t:.*')

def send_queue_info(port,queue,object,action,counter):
    #statsd gauge
    msg = (HOSTNAME,'.',port,'-queue',queue,'-',action,'-',object,':',counter,'|g')
    msg = join(msg,sep='')
    statsd_socket.sendto(msg,STATSD_SERVER)


def main():
    while True:
        pipe = subprocess.Popen([BCM_SHELL,CMD],stdout=subprocess.PIPE)
        for line in pipe.stdout.readlines():
            if egress_queue_pkt_re.match(line):
                int_name = egress_queue_pkt_re.findall(line)[0][1]
                queue_num = egress_queue_pkt_re.findall(line)[0][0]
                value = join(line.strip().split()[2].strip('+').split(','),sep='')
                send_queue_info(int_name,queue_num,'pkt','pass',value)
            if egress_queue_byte_re.match(line):
                int_name = egress_queue_byte_re.findall(line)[0][1]
                queue_num = egress_queue_byte_re.findall(line)[0][0]
                value = join(line.strip().split()[2].strip('+').split(','),sep='')
                send_queue_info(int_name,queue_num,'byte','pass',value)
        time.sleep(9)


if __name__ == '__main__':
    main()
