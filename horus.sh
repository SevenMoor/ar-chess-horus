#!/bin/bash

if [[ "$1" == "uninstall" ]]; then
    sudo rm -rf /usr/bin/ar-horus
    sudo rm -rf /opt/ar-chess-horus
    echo -e "\e[33mDésinstallation terminée!\e[0m"
elif [[ "$1" == "update" ]]; then
    DIR=$(pwd)
    cd /opt/ar-chess-horus
    sudo git pull
    cd "$DIR"
    echo -e "\e[36mMise à jour terminée!\e[0m"
else
    DIR=$(pwd)
    cd /opt/ar-chess-horus
    python /opt/ar-chess-horus/main.py ${@:1}
    cd "$DIR"
fi
