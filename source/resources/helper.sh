#!/bin/sh

if [ "$2" = "0" ]
then
  pgrep xbmc.bin | xargs kill -SIGSTOP
  (echo "***** `date +"%d.%m.%Y %T"` *****" && $1) > $3 2>&1
  pgrep xbmc.bin | xargs kill -SIGCONT  
  exit 0
elif [ "$2" = "1" ]
then
  systemctl stop xbmc.service
  (echo "***** `date +"%d.%m.%Y %T"` *****" && $1) > $3 2>&1
  systemctl start xbmc.service
  exit 0
else
  exit 1
fi
