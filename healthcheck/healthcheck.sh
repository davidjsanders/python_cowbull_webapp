#!/bin/sh
set -o pipefail
curl -sI http://localhost:8080 &> /dev/null
ret_stat=$?
if [ "$ret_stat" == "0" ]; then printf "Healthy"; else printf "Unhealthy"; fi
exit $ret_stat