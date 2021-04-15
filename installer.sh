#!/bin/sh
# installer.sh will install the necessary packages and config files for HOORCH

CONFIG="/boot/config.txt"
COMITUP_CONF="/etc/comitup.conf"

# Install packages
#echo "updating system. this may take some time..."
apt update
#apt upgrade -y

echo "installing packages"
apt install -y python3-pip
apt install -y sox
apt install -y libsox-fmt-mp3
apt install -y espeak
apt install -y libsdl2-mixer-2.0-0
apt install -y git

pip3 install --upgrade setuptools
pip3 install RPI.GPIO adafruit-circuitpython-pn532 board pygame
python3 -m pip install --force-reinstall adafruit-blinka

#enable SPI
sed -i "s/#dtparam=spi=on/dtparam=spi=on/g" $CONFIG

#create asound.conf
#https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage

# cat > ~/asound.conf << 'EOL'
# pcm.speakerbonnet {
#    type hw card 0
# }
#
# pcm.dmixer {
#    type dmix
#    ipc_key 1024
#    ipc_perm 0666
#    slave {
#      pcm "speakerbonnet"
#      period_time 0
#      period_size 1024
#      buffer_size 8192
#      rate 44100
#      channels 2
#    }
# }
#
# ctl.dmixer {
#     type hw card 0
# }
#
# pcm.softvol {
#     type softvol
#     slave.pcm "dmixer"
#     control.name "PCM"
#     control.card 0
# }
#
# ctl.softvol {
#     type hw card 0
# }
#
# pcm.!default {
#     type             plug
#     slave.pcm       "softvol"
# }
# EOL
#
# mv ~/asound.conf /etc/asound.conf

#disable audio / for i2s speaker
#sed -i "s/dtparam=audio=on/#dtparam=audio=on/g" $CONFIG

#add the two lines for i2s speaker
#sh -c "echo 'dtparam=act_led_trigger=none' >> /boot/config.txt"
#dtoverlay=hifiberry-dac
#dtoverlay=i2s-mmap

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
sh -c "echo 'disable_splash=1' >> /boot/config.txt"

# Set the bootloader delay to 0 seconds. The default is 1s if not specified.
#sh -c "echo 'boot_delay=0' >> /boot/config.txt"


#disable interfering SPI chip select/slave select pin
#problem was flickering led 6 at (Pin 24, GPIO8, SPI_CE0_N)
#more information https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README
sh -c "echo 'dtoverlay=spi0-2cs,cs0_pin=0' >> /boot/config.txt"

echo "copying HOORCH files"

#copy service-files to /etc/systemd/system
cp *.service /etc/systemd/system

#copy gpio shutoff script for OnOff Shim and make it executeable
cp gpio-shutoff.sh /lib/systemd/system-shutdown/
chmod +x /lib/systemd/system-shutdown/gpio-shutoff.sh

#enable and start the services
systemctl enable hoorch*.service
systemctl start hoorch*.service


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
#sed -i "s/# ap_name: comitup-<nn>/ap_name: hoorch-<nn>/g" $COMITUP_CONF
sed -i "s/# ap_name: comitup-<nnn>/ap_name: hoorch-<nnn>/g" "/etc/comitup.conf"

#comment out references to /etc/network/interfaces - https://github.com/davesteele/comitup/wiki/Installing-Comitup
sed -i "s/source-directory/#source-directory/g" "/etc/network/interfaces"

#if connected to pi via remote, network connection will break here making screen freeze at at 88%.

echo "Installation complete, rebooting now"
reboot
