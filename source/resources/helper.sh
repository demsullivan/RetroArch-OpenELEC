#!/bin/sh

DATE=$(date +"%d.%m.%Y %T")

if [ "$1" = "0" ]
then
  pgrep xbmc.bin | xargs kill -SIGSTOP
  (echo $DATE && $2) > $3 2>&1
  pgrep xbmc.bin | xargs kill -SIGCONT  
  exit 0
elif [ "$1" = "1" ]
then
  systemctl stop xbmc.service
  (echo $DATE && $2) > $3 2>&1
  systemctl start xbmc.service
  exit 0
else
  exit 1
fi
