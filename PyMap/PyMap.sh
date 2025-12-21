#!/bin/sh

BAND="10m"
FILTER="LU7DZ"
LOGIN="LU2EIC"
LOCAL=9000
REMOTE=7000
HOST="telnet.reversebeacon.net"
python PyMap.py --remote-host $HOST --remote-port $REMOTE -r $LOGIN --listen-port $LOCAL  -f $FILTER --keyword "LU7DZ" --band $BAND --persist 5 --graph "MARBLE"
