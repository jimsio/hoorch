#!/bin/sh
#
# OnOff SHIM exposed by cyperghost for retropie.org.uk
# This is mandatory for proper shutdown with SHIM!

#this script goes here /lib/systemd/system-shutdown/
#and need to be executeable

#gpio nr
poweroff_pin="5"
led_pin="23"

if [ "$1" = "poweroff" ]; then
  /bin/echo $led_pin > /sys/class/gpio/export
  /bin/echo out > /sys/class/gpio/gpio$led_pin/direction

  for iteration in 1 2 3; do
    /bin/echo 0 > /sys/class/gpio/gpio$led_pin/value
    /bin/sleep 0.2
    /bin/echo 1 > /sys/class/gpio/gpio$led_pin/value
    /bin/sleep 0.2
  done

  /bin/echo $poweroff_pin > /sys/class/gpio/export
  /bin/echo out > /sys/class/gpio/gpio$poweroff_pin/direction
  /bin/echo 0 > /sys/class/gpio/gpio$poweroff_pin/value
fi