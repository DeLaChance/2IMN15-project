#!/bin/bash
# just to be sure
export MODELS_FOLDER=/home/pi/

# kill avahi-publish and java processes
ps ax | grep avahi-publish | awk '{ print $1 }' | xargs kill -9
ps ax | grep java | awk '{ print $1 }' | xargs kill -9
ps ax | grep python | awk '{ print $1 }' | xargs kill -9
rm -rf /home/pi/events/serverip.txt /home/pi/events/displaylock.txt /home/pi/events/jslock.txt /home/pi/events/js.txt
netstat -peanut | awk '{ print $9 }' | grep python | sed 's:/python::g' | xargs kill -9

SERVICE_NAME="PARKING_SPOT";
PORT=5683;
NAME="/myparking";
SUBP="_floor1._sub._coap._udp";
SERVER_IP=$1
SERVER_PORT=5683

avahi-publish-service $SERVICE_NAME _coap._udp $PORT $NAME --sub $SUBP &
python ~/2IMN15-project/client/SensingActuating.py $SERVER_IP &

# after /home/pi/events/serverip.txt exists we can start java -jar
while [ ! -f "/home/pi/events/serverip.txt" ]
do
    sleep 1
done

echo "starting LWM2M server SERVER_PORT="$SERVER_PORT", SERVER_IP="$SERVER_IP;

java -jar /home/pi/RaspberryLWM2M.jar $SERVER_IP $SERVER_PORT
