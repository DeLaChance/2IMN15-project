#!/bin/sh
rm -rf reserveParkingSpotOutput.txt
date | awk '{print $4}' > reserveParkingSpotOutput.txt
echo "python2.7 server/reserveParkingSpot.py $1 $2 >> reserveParkingSpotOutput.txt" | at -t $3