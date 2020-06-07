#!/bin/bash

if [[ "$1" == "uninstall" ]]; then
    sudo rm -rf /usr/bin/ar-horus
    rm -rf /opt/ar-chess-horus
    echo "\e[36mDésinstallation terminée\e[0m!"
elif [[ "$1" == "update" ]]; then
    DIR=$(pwd)
    cd /opt/ar-chess-horus
    git pull
    cd "$DIR"
    echo "\e[36mMise à jour terminée\e[0m!"
else
    python main.py ${@:1}
fi
