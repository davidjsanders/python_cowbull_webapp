#!/bin/bash
set -o pipefail
curl http://localhost:8080 | grep "CowBull Version"
exit $?