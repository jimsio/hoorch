#!/bin/sh
# installer.sh will install the necessary packages and config files for HOORCH
# https://core-electronics.com.au/tutorials/create-an-installer-script-for-raspberry-pi.html
# Kernel 4.19.97-v8+

CONFIG="/boot/config.txt"
COMITUP_CONF="/etc/comitup.conf"

# Install packages
echo "installing packages"
apt update
apt upgrade -y
pip3 install --upgrade setuptools
pip3 install RPI.GPIO adafruit-circuitpython-pn532 adafruit-blinka pygame
apt install sox libsox-fmt-mp3 espeak
#not needed:
#apt install xrdp

#enable SPI
sed -i "s/#dtparam=spi=on/dtparam=spi=on/g" $CONFIG 

#disable hdmi (enable: -p) - to safe power
/opt/vc/bin/tvservice -o

# Disable the ACT LED.
sh -c "echo 'dtparam=act_led_trigger=none' >> /boot/config.txt"
sh -c "echo 'dtparam=act_led_activelow=off' >> /boot/config.txt"

# Disable the PWR LED.
sh -c "echo 'dtparam=pwr_led_trigger=none' >> /boot/config.txt"
sh -c "echo 'dtparam=pwr_led_activelow=off' >> /boot/config.txt"

#disable bluetooth - to safe power
sh -c "echo 'dtoverlay=pi3-disable-bt' >> /boot/config.txt"
systemctl disable bluetooth.service

# Disable the rainbow splash screen
sh -c "echo 'disabble_splash=1' >> /boot/config.txt"

# Set the bootloader delay to 0 seconds. The default is 1s if not specified.
sh -c "echo 'boot_delay=0' >> /boot/config.txt"


#disable interfering SPI chip select/slave select pin
#problem was flickering led 6 at (Pin 24, GPIO8, SPI_CE0_N)
#more information https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README
sh -c "echo 'dtoverlay=spi0-cs,cs0_pin=0,cs1_pin=0' >> /boot/config.txt"

#deprecated: change owner of wpa_supplicant.conf for editing
#chown pi /etc/wpa_supplicant/wpa_supplicant.conf

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
# or: sudo apt-get install comitup
mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.confbak
#systemctl disable systemd.resolved

#rename the comitup-wifi-name to hoorch-<nn> - https://davesteele.github.io/comitup/man/comitup-conf.5.html
sed -i "s/# ap_name: comitup-<nn>/ap_name: hoorch-<nn>/g" $COMITUP_CONF

#comment out references to /etc/network/interfaces - https://github.com/davesteele/comitup/wiki/Installing-Comitup
sed -i "s/source-directory/#source-directory/g" "/etc/network/interfaces"

echo "copying hoorch files"

#copy service-files to /etc/systemd/system
cp *.service /etc/systemd/system

#enable and start the services
systemctl enable hoorch*.service
systemctl start hoorch*.service

#copy gpio shutoff script for OnOff Shim and make it executeable
cp gpio-shutoff.sh /lib/systemd/system-shutdown/
chmod +x /lib/systemd/system-shutdown/gpio-shutoff.sh

#install OnOff Shim library
#curl https://get.pimoroni.com/cleanshutdown | bash
#What BCM pin would you like to use as trigger for the shutdown? 13
#What BCM pin would you like to pull low on shutdown? ('off' for none) 5
#Would you like to reboot now? [y/N] N
#to change the pin numbers manually: sudo nano /etc/cleanshutd.conf

#set hold time for shutdown button to 3 seconds
#sed -i "s/#hold_time=1/hold_time=3/g" "/etc/cleanshutd.conf" 

#set led to blink at shutdown to the led at reader 1 (gpio23)
#sed -i "s/#led_pin=off/led_pin=23/g" "/etc/cleanshutd.conf" 

echo "Installation complete, rebooting now"
reboot
