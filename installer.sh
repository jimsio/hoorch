#!/bin/sh
# installer.sh will install the necessary packages and config files for HOORCH

CONFIG="/boot/config.txt"
COMITUP_CONF="/etc/comitup.conf"

# Install packages
#echo "updating system. this may take some time..."
apt update
#apt upgrade -y

#remove GUI - for faster start:
apt remove --purge x11-common
apt autoremove

echo "installing packages"
apt install -y python3-pip
apt install -y sox
apt install -y libsox-fmt-mp3
apt install -y espeak
apt install -y libsdl2-mixer-2.0-0
apt install -y git

pip3 install --upgrade setuptools
pip3 install RPI.GPIO adafruit-circuitpython-pn532 board pygame rpi_ws281x adafruit-circuitpython-neopixel
python3 -m pip install --force-reinstall adafruit-blinka
pip3 install --upgrade adafruit-python-shell

#enable SPI
sed -i "s/#dtparam=spi=on/dtparam=spi=on/g" $CONFIG

# i2s microphone
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
python3 i2smic.py

# i2s microphone - add volume control
mv ./.asoundrc ~/.asoundrc

# i2s amplifier
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash

#disable hdmi (enable: -p) - to safe power
/opt/vc/bin/tvservice -o

# Disable the ACT LED.
#sh -c "echo 'dtparam=act_led_trigger=none' >> /boot/config.txt"
#sh -c "echo 'dtparam=act_led_activelow=off' >> /boot/config.txt"

# Disable the PWR LED.
#sh -c "echo 'dtparam=pwr_led_trigger=none' >> /boot/config.txt"
#sh -c "echo 'dtparam=pwr_led_activelow=off' >> /boot/config.txt"

#disable bluetooth - to safe power
sh -c "echo 'dtoverlay=pi3-disable-bt' >> /boot/config.txt"
systemctl disable bluetooth.service

# Disable the rainbow splash screen
sh -c "echo 'disable_splash=1' >> /boot/config.txt"

# Set the bootloader delay to 0 seconds. The default is 1s if not specified.
#sh -c "echo 'boot_delay=0' >> /boot/config.txt"

echo "copying HOORCH files"

#copy service-files to /etc/systemd/system
cp *.service /etc/systemd/system

#copy gpio shutoff script for OnOff Shim and make it executeable
cp gpio-shutoff.sh /lib/systemd/system-shutdown/
chmod +x /lib/systemd/system-shutdown/gpio-shutoff.sh

#enable and start the services
systemctl enable hoorch*.service
#systemctl start hoorch*.service #will be started manually by user, see installation manual


#install log2ram
echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
apt update
apt install log2ram

#disable swapping
systemctl disable dphys-swapfile.service

#install comitup - wifi
echo "deb http://davesteele.github.io/comitup/repo comitup main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://davesteele.github.io/key-366150CE.pub.txt | sudo apt-key add -
apt update
apt install comitup

mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.confbak
#systemctl disable systemd.resolved

#rename the comitup-wifi-name to hoorch-<nn> - https://davesteele.github.io/comitup/man/comitup-conf.5.html
sed -i "s/# ap_name: comitup-<nnn>/ap_name: hoorch-<nnn>/g" "/etc/comitup.conf"

#comment out references to /etc/network/interfaces - https://github.com/davesteele/comitup/wiki/Installing-Comitup
sed -i "s/source-directory/#source-directory/g" "/etc/network/interfaces"

#if connected to pi via remote, network connection will break here making screen freeze at 88%.

echo "Installation complete, rebooting now"
reboot
