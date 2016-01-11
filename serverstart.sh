#!/bin/sh
# just to be sure
BASEDIR=$(dirname $0)
export MODELS_FOLDER=$BASEDIR

# start Java leshan-standalone (lwm2m)
java -jar LWM2MServer.jar &

# start python process
python2.7 server/server.py