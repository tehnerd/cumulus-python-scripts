#!/usr/bin/python
import subprocess
import re
import sys
import time
from string import join

def get_intf_rates(interface):
    re_rxtx_rates = re.compile(".*?RX bytes:(\d+) .*?TX bytes:(\d+) .*?")
    IFCONFIG = '/sbin/ifconfig'
    pipe = subprocess.Popen([IFCONFIG,interface],stdout=subprocess.PIPE)
    for line in pipe.stdout.readlines():
        if re_rxtx_rates.match(line):
            return re_rxtx_rates.findall(line)[0][0], re_rxtx_rates.findall(line)[0][1]


def main():
    INTF = sys.argv[1]
    rx1,tx1 = get_intf_rates(INTF)
    time.sleep(10)
    rx2,tx2 = get_intf_rates(INTF)
    print("rx_rate: %s bps\t tx_rate:%s bps"
      %((int(rx2)-int(rx1))/10*8,(int(tx2)-int(tx1))/10*8,))


if __name__ == '__main__':
    main()

