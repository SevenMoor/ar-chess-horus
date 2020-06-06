#!/bin/bash

if [[ "$1" == "uninstall" ]]; then
    sudo rm -rf /usr/bin/ar-horus
    rm -rf /opt/ar-chess-horus
else
    python main.py ${@:1}
fi
