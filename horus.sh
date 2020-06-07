#!/bin/bash

if [[ "$1" == "uninstall" ]]; then
    sudo rm -rf /usr/bin/ar-horus
    rm -rf /opt/ar-chess-horus
elif [[ "$1" == "update" ]]; then
    DIR=$(pwd)
    cd /opt/ar-chess-horus
    git pull
    cd "$DIR"
else
    python main.py ${@:1}
fi
