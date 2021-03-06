#!/bin/bash

sudo cp . /opt/ar-chess-horus -R
sudo chmod +x /opt/ar-chess-horus/horus.sh
sudo rm -f /opt/ar-chess-horus/install.sh

FILE=/usr/bin/ar-horus
if [[ -f "$FILE" ]]; then
    sudo rm -f "$FILE"
fi

sudo chmod 777 /opt/ar-chess-horus -R

sudo pip install /opt/ar-chess-horus
sudo ln -s /opt/ar-chess-horus/horus.sh /usr/bin/ar-horus
echo -e "\033[32mInstallation terminée!\033[0m"
