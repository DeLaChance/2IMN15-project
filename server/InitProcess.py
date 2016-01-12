import SpotFinderThread
import time
import sys

# just a temporary main-class to test the set-up of the whole
# process using mDNS and lwm2m

def run(ip):
    print("Starting initProcess...")
    SpotFinderThread.init(ip)
    while( True ):
        time.sleep(1)
