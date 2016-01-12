import thread
import threading
import time
import re
from subprocess import Popen, PIPE
import socket
import os
import RequestUtils

re_ip = None
ownIP = ""
ipaddresses = []

lock = threading.Lock()

def runShellCommand(cmd):
    # assumes the server is run on Linux or Mac OS
    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return (out, err)

def isValidIpv4(s):
    return re_ip.match(s) != None;

def getOwnIP():
    return ownIP

def keepAvahiBrowsing(thread_name, ipaddresses, lock):
    print("start keepAvahiBrowsing: threadname=" + thread_name)
    while( True ):
        (output, err) = runShellCommand("avahi-browse -rtp _coap._udp")
        if( (err == None) or (output == None or len(output) == 0) ):
            print("SpotFinderThread: error avahi-browse err=" + str(err) + ",out=" + output)
        else:
            lines = output.splitlines()
            for line in lines:
                arr = line.split(";")
                if( len(arr) >= 8 ):
                    ip = arr[7]
                    #print("SpotFinderThread: testing ip=" + ip + ",isValidIp=" + str(isValidIpv4(ip)) + ",in=" + str(ip in ipaddresses))
                    lock.acquire()
                    if( isValidIpv4(ip) and (ip in ipaddresses) == False ):
                        print("SpotFinderThread: client-ip found ip=" + ip)
                        thread.start_new_thread(sendServerIPtoParkingSpot, ("sendServerIPtoParkingSpot", ip, getOwnIP()))
                        RequestUtils.createParkingSpot(ip)
                        ipaddresses.append(ip)
                    lock.release()
        time.sleep(5)

def keepReadingJoystickFiles(thread_name, ipaddresses, lock):
    # reads the joystickfiles jsUpdate-<end_point>.txt that are output by Java
    # assumes these are in the directory below
    print("start keepReadingJoystickFiles thread_name=" + thread_name);
    path = os.path.realpath(__file__)
    path = path[0:path.rindex("/")]
    path = path[0:path.rindex("/")+1] # get parent directory
    prefix = "jsUpdate-"
    suffix = ".txt"
    print("keepReadingJoystickFiles path=" + path)

    while( True ):
        fileNames = os.listdir(path)
        for fileName in fileNames:
            if prefix in fileName:
                endpoint = fileName[len(prefix):len(fileName)-len(suffix)]
                print("keepReadingJoystickFiles fileName=" + fileName, "endpoint=" + endpoint)
                RequestUtils.enterOrLeaveVehicle(endpoint)
                # delete file
                os.remove(fileName)
        time.sleep(1)


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
            print("sendServerIPtoParkingSpot retry i=" + str(i) +"! threadname=" + thread_name + " ,ip=" + ip)


def init(p_ownIP):
    global re_ip
    global ownIP
    global ipaddresses

    ownIP = p_ownIP
    ipaddresses = []
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    thread.start_new_thread(keepAvahiBrowsing, ("SpotFinderThread,keepAvahiBrowsing", ipaddresses, lock))
    thread.start_new_thread(keepReadingJoystickFiles, ("SpotFinderThread,keepReadingJoystickFiles", ipaddresses, lock))