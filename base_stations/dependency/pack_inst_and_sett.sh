#!/bin/bash
# Packages

apt-get update;
apt-get remove --purge triggerhappy logrotate dphys-swapfile  xserver-common lightdm avahi-daemon -y

apt-get autoremove --purge -y

sudo apt-get install cubian-nandinstall lighttpd python-pip  php5-cgi php5 php-pear ppp python-matplotlib python-numpy python-scipy ffmpeg ffmpeg sox curl usb-modeswitch python-twisted usbutils wvdial busybox-syslogd -y

dpkg --purge rsyslog

sudo pip install pydub
pip install pyA10_CB

# Save alsa settings
alsactl store 0

insserv -r bootlogs
insserv -r sudo
insserv -r alsa-utils
insserv -r console-setup
insserv -r fake-hwclock

# links
rm -rf /var/lib/dhcp/
ln -s /tmp /var/lib/dhcp

rm /.matplotlib/ -rf
ln -s  /tmp /.matplotlib

rm -rf /root/.matplotlib
ln -s /tmp /root/.matplotlib

sudo update-rc.d atd disable 2
sudo update-rc.d atd disable 3
sudo update-rc.d atd disable 4
