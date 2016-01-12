#!/bin/sh
# just to be sure
BASEDIR=$(dirname $0)
export MODELS_FOLDER=$BASEDIR
OWN_IP=""

# clean-up
rm -rf jsUpdate-*

# start Java leshan-standalone (lwm2m)
#java -jar LWM2MServer.jar &

# start python process
#python2.7 server/InitProcess.py 192.168.1.103
python2.7 server/server.py $OWN_IP
