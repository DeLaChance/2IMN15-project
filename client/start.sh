#!/bin/bash
SERVICE_NAME="PARKING_SPOT";
PORT=5683;
NAME="/myparking";
SUBP="_floor1._sub._coap._udp";

avahi-publish-service $SERVICE_NAME _coap._udp $PORT $NAME --sub $SUBP &
python ~/2IMN15-project/client/ParkingClient.py 
