import SpotFinderThread
import time
import sys

# just a temporary main-class to test the set-up of the whole
# process using mDNS and lwm2m

def main():
    print("Starting initProcess...")
    SpotFinderThread.init(sys.argv[1])
    while( True ):
        time.sleep(1)

if __name__ == '__main__':
    main()