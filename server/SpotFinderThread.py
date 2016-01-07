import thread
import threading
import time
import re
from subprocess import Popen, PIPE
import socket
import sys

ips = []
re_ip = None
ownIP = ""

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

def getOwnIP():
    return ownIP
    #import urllib2
    #ret = urllib2.urlopen('https://enabledns.com/ip')
    #return ret.read()

def keepAvahiBrowsing(thread_name, ips):
    print("start keepAvahiBrowsing: threadname=" + thread_name)
    while( True ):
        lock.acquire()
        #ips = [] # Only keep active IPs
        (output, err) = runShellCommand("avahi-browse -rtp _coap._udp")
        if( (err == None or len(err) > 0) or (output == None or len(output) == 0) ):
            print("SpotFinderThread: error avahi-browse err=" + str(err) + ",out=" + output)
        else:
            lines = output.splitlines()
            for line in lines:
                #print("Processing line line=" + line)
                arr = line.split(";")
                if( len(arr) >= 8 ):
                    ip = arr[7]
                    if( isValidIpv4(ip) and ips.count(ip) == 0 ):
                        print("SpotFinderThread: client-ip found ip=" + ip)
                        thread.start_new_thread(sendServerIPtoParkingSpot, ("sendServerIPtoParkingSpot", ip, getOwnIP()))
                        ips.append(ip)
        lock.release()

        time.sleep(10)

def sendServerIPtoParkingSpot(thread_name, ip, ownIP):
    # sends the server IP to the parking spot s.t. it can start lwm2mclient
    print("start sendServerIPtoParkingSpot: threadname=" + thread_name + " ,ip=" + ip)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 0;
    while( i < 10 ):
        try:
            s.connect((ip, 4000))
            s.send(ownIP)
            print("sendServerIPtoParkingSpot ip has been sent! threadname=" + thread_name + " ,ip=" + ip)
            i = 10
        except Exception:
            time.sleep(2)
            i += 1


def init(p_ownIP):
    global ips
    global re_ip
    global ownIP

    ownIP = p_ownIP
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    ips = [];
    thread.start_new_thread(keepAvahiBrowsing, ("SpotFinderThread", ips))