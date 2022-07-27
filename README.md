# Raspbery Pi Configuration
This repository should contain the instructions and configuration files to set up the raspberry pi as a media server.

## Feature Backlog
* VPN functionality
* RAID capabilities
* Opening port securely to the internet

## Instructions
* Execute ```sudo apt-get update```
* Execute ```sudo apt-get upgrade```
* Execute ```sudo apt-get install deluged deluge-web samba samba-common-bin```
* Execute ```sudo blkid``` and take a note of the UUID of the storage drive
* Add ```UUID=<Storage UUID> /media/hdd ntfs defaults,auto,users,rw,nofail,umask=000 0 0``` with custom modifications to ```/etc/fstab``` file
* Copy ```deluge``` script to ```/etc/init.d/```
* Delete existing ```deluged-daemon``` script
* Execute ```sudo systemtctl daemon-reload```
* Add the line from ```web.conf``` to ```/home/<user>/.config/deluge/web.conf```
* Modify and copy ```deluged-config``` to ```/etc/defaults/deluged```
* Add the contents of ```smb.conf``` to ```/etc/samba/smb.conf```
* Execute ```sudo reboot```
* Configure deluge
* Execute ```curl -sSL https://install.pi-hole.net | bash``` and follow the instructions to configure Pi-hole
* Set a static IP address for Raspberry Pi
* Configure the primary DNS server to point to the Raspberry Pi static IP address

## Helpful commands
### Updating and installing required packages
* ```sudo apt-get update```
* ```sudo apt-get upgrade```
* ```sudo apt-get install deluged deluge-web samba samba-common-bin```

### HDD UUID command
* ```sudo blkid```

### Restart and reload system services
* ```sudo systemctl restart smbd```
* ```sudo systemctl daemon-reload```
* ```sudo systemctl deluged```

## Useful links
https://dev.deluge-torrent.org/wiki/UserGuide/Service/DebianUbuntuInitd - Init script for deluged and deluge-web application to launch simultaneously at launch with the configuration to connect the deluge-daemon to each other automatically without requiring configuration at startup.
https://github.com/pi-hole/pi-hole/#one-step-automated-install - Repository for Pi-hole containing more detailed instructions.
