#!/bin/bash

cp . /opt/ar-chess-horus -R
chmod +x /opt/ar-chess-horus/horus.sh
rm -f /opt/ar-chess-horus/install.sh

FILE=/usr/bin/ar-horus
if [[ -f "$FILE" ]]; then
    sudo rm -f "$FILE"
fi

sudo pip install /opt/ar-chess-horus
sudo ln -s /opt/ar-chess-horus/horus.sh /usr/bin/ar-horus
