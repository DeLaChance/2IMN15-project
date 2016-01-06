import thread
import threading
import time
import re
from subprocess import Popen, PIPE

ips = []
re_ip = None

lock = threading.Lock()

def runShellCommand(cmd):
    # assumes the server is run on Linux or Mac OS
    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return (out, err)

def isValidIpv4(s):
    return re_ip.match(s);

def getIPs():
    global lock
    lock.acquire()
    ips2 = list(ips)
    lock.release()
    return ips2

def keepAvahiBrowsing(thread_name, ips):
    while( True ):
        lock.acquire()
        ips = [] # Only keep active IPs
        (output, err) = runShellCommand("avahi-browse -rtp _coap._udp")
        if( err != 0 or (output == None or len(output) == 0) ):
            print("SpotFinderThread: error avahi-browse err=" + str(err) + ",out=" + output)
        else:
            lines = output.splitlines()
            for line in lines:
                print("Processing line line=" + line)
                arr = line.split(";")
                if( len(arr) >= 6 ):
                    ip = arr[5]
                    if( isValidIpv4(ip) and ips.count(ip) == 0 ):
                        print("SpotFinderThread: ip found ip=" + ip)
                        ips.append(ip)
        lock.release()

        time.sleep(10)

def init():
    global ips
    global re_ip
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    ips = [];
    thread.start_new_thread(keepAvahiBrowsing, ("SpotFinderThread", ips))