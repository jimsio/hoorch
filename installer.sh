#!/bin/sh
# installer.sh will install the necessary packages and config files for HOORCH

# Install packages
echo "apt updating system. this may take some time..."
apt update -y
apt upgrade -y

echo "installing packages"
apt install -y python3-pip
apt install -y sox
apt install -y libsox-fmt-mp3
apt install -y espeak
apt install -y libsdl2-mixer-2.0-0
apt install -y git

pip3 install --upgrade setuptools
pip3 install RPI.GPIO adafruit-circuitpython-pn532 board pygame rpi_ws281x adafruit-circuitpython-neopixel adafruit-circuitpython-debouncer
python3 -m pip install --force-reinstall adafruit-blinka
pip3 install --upgrade adafruit-python-shell

#enable SPI
sed -i "s/#dtparam=spi=on/dtparam=spi=on/g" "/boot/config.txt"

# i2s microphone
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
python3 i2smic.py

# i2s microphone - add volume control
mv asoundrc ~/.asoundrc

# i2s amplifier
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash

#disable hdmi (enable: -p) - to safe power - i need hdmi connection 
#/opt/vc/bin/tvservice -o

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
#systemctl enable hoorch*.service
#systemctl start hoorch*.service 

#will be started manually by user, see installation manual


#install log2ram
echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
apt update
apt install log2ram

#disable swapping
systemctl disable dphys-swapfile.service

#change SIZE=40M to SIZE=100M /etc/log2ram.conf
sed -i 's/SIZE=40M/SIZE=100M/g' /etc/log2ram.conf

#start/restart networking service (NetworkManager)
systemctl restart networking

#install comitup - wifi:
#1 install package .deb
wget https://davesteele.github.io/comitup/latest/davesteele-comitup-apt-source_latest.deb
dpkg -i --force-all davesteele-comitup-apt-source_latest.deb
rm davesteele-comitup-apt-source_latest.deb
apt update
apt install comitup comitup-watch -y

#2: Allow NetworkManager to manage the wifi interfaces by removing references to them from /etc/network/interfaces.
mv /etc/network/interfaces /etc/network/interfaces.bak

#3: Rename  /etc/wpa_supplicant/wpa_supplicant.conf.
mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.confbak

#4: The systemd.resolved service should be disabled and masked to avoid contention for providing DNS service.
systemctl mask dnsmasq.service
systemctl mask systemd-resolved.service
systemctl mask dhcpd.service
systemctl mask dhcpcd.service
systemctl mask wpa-supplicant.service
systemctl enable NetworkManager.service

#5: #rename the comitup-wifi-name to hoorch-<nn> - https://davesteele.github.io/comitup/man/comitup-conf.5.html
sed -i "s/# ap_name: comitup-<nnn>/ap_name: hoorch-<nnn>/g" "/etc/comitup.conf"

echo "Installation complete, rebooting now"
reboot
