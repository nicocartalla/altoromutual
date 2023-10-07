#!/bin/bash

/usr/local/tomcat/bin/catalina.sh run > /dev/null 2>&1 &

COUNTER=0
TIMEOUT=10

while ! cat $(ls -t /usr/local/tomcat/logs/catalina.*) | grep -qm 1 "Server startup in"; do
    sleep 1
    let COUNTER=COUNTER+1
    if [[ $COUNTER -ge $TIMEOUT ]]; then
        echo "Tomcat startup timed out."
        exit 1
    fi
done

#run dast scan
python3 /dast/main.py
