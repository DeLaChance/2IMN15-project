#!/bin/sh
# just to be sure
BASEDIR=$(dirname $0)
export MODELS_FOLDER=$BASEDIR
OWN_IP=$1

# clean-up
rm -rf jsUpdate-*
ps ax | grep LWM2M | awk '{ print $1 }' | xargs kill -9

# start Java leshan-standalone (lwm2m)
java -jar LWM2MServer.jar &

sleep 5 # wait for the LWM2mServer to be started

# start python process
#python2.7 server/InitProcess.py 192.168.1.103
python2.7 server/server.py $OWN_IP "skip"
