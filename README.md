# Raspbery Pi Configuration
This repository should contain the instructions and configuration files to set up the raspberry pi's named Franklin and Eleanor. The instructions should help configure them with the following utilities.

## Franklin
* Recursive DNS
* Pi-Hole
* Pi-VPN
* Deluge
* Plex Media Server

## Eleanor
* Mount HDDs
* RAID

## Instructions

### General

#### Disable Swap file
* Execute the following commands:
    * ```sudo dphys-swapfile swapoff```
    * ```sudo dphys-swapfile uninstall```
    * ```sudo systemctl stop dphys-swapfile.service```
    * ```sudo systemctl disable dphys-swapfile.service```

### Setting up Franklin

#### GPIO Fan
* Add ```dtoverlay=gpio-fan,gpiopin=3,temp=60000``` to ```/boot/config.txt```
* Copy ```fancontrol.py``` to ```/home/pi/fancontrol```
* Copy ```fancontrol.service``` to ```/lib/systemd/system/fancontrol.service```
* Execute the following commands:
    * ```sudo systemctl daemon-reload```
    * ```sudo systemctl enable fancontrol.service```
    * ```sudo systemctl start fancontrol.service```

#### NFS Client
* Execute ``sudo apt-get install nfs-common -y```
* Copy NFS FSTAB configuration to ```/etc/fstab```
* Execute ```sudo mount -a```

#### Deluge
* Execute ```sudo apt-get install deluged deluge-web```
* Copy ```deluge``` script to ```/etc/init.d/```
* Delete existing ```deluged-daemon``` script
* Execute ```sudo systemtctl daemon-reload```
* Add the line from ```web.conf``` to ```/home/<user>/.config/deluge/web.conf```
* Modify and copy ```deluged-config``` to ```/etc/defaults/deluged```
* Configure deluge

#### DuckDNS
* Copy ```duck.sh``` to ```~/duckdns/```
* Execute ```chmod 700 duck.sh```
* Execute ```crontab -e```
* Add ```*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1``` to the cron config
* Start cron service ```sudo service cron start```
* Test ```./duck.sh``` and check logs ```cat duck.log```

#### Pi-Hole & PiVPN
* Execute ```curl -sSL https://install.pi-hole.net | bash``` and follow the instructions to configure Pi-hole
* Add static IP address to ```static domain_name_servers=[IP Address]``` in ```/etc/dhcpcd.conf```
* Set a static IP address for Raspberry Pi on the router
* Configure the primary DNS server on the router to point to the Raspberry Pi static IP address
* Install unbound ```sudo apt-get install unbound```
* Copy ```root.hints``` to ```/var/lib/unbound/```
* Copy ```pi-hole.conf``` to ```/etc/unbound/unbound.conf.d/```
* Restart unbound service ```sudo systemctl restart unbound```
* Test recursive DNS using ```dig pi-hole.net @127.0.0.1 -p 5335```
* Copy ```99-edns.conf``` to ```/etc/dnsmasq.d/```
* Add ```127.0.0.1#5335``` as a custom DNS IPv4 provider to use local unbound DNS queries
* Run the following script ```curl -L https://install.pivpn.io | bash``` and follow the instructions choosing WireGuard

#### Plex Media Server
* Execute ```sudo apt-get install apt-transport-https```
* Execute ```curl https://downloads.plex.tv/plex-keys/PlexSign.key | gpg --dearmor | sudo tee /usr/share/keyrings/plex-archive-keyring.gpg >/dev/null```
* Execute ```echo deb [signed-by=/usr/share/keyrings/plex-archive-keyring.gpg] https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list```
* Execute ```sudo apt-get update```
* Execute ```sudo apt install plexmediaserver```
* Set-up Plex Media Server

### Setting up Eleanor

#### Rock-Pi SATA
* Execute the script ```curl -sL https://rock.sh/get-rockpi-sata | sudo -H -E bash -```
* Copy ```fan.py``` to ```/usr/bin/rockpi-sata/```
* Copy ```rockpi-sata.conf``` to ```/etc/```

#### Sector error check, EXT4 formatting, mount HDD and RAID configuration
* Execute ```sudo mkfs -t ext4 -c /dev/<sda/sdb/sdc/sdd> -v```
* Execute ```sudo blkid``` and take a note of the UUID of the storage drive
* Add ```UUID=<Storage UUID> /media/hdd ntfs defaults,auto,users,rw,nofail,umask=000 0 0``` with custom modifications to ```/etc/fstab``` file
* Execute ```sudo reboot```

#### NFS Server
* Execute ```sudo apt-get install nfs-kernel-server -y```
* Copy ```exports``` to ```/etc/exports```
* Execute ```sudo exportfs -ra```

#### HDD Maintainance
* Install hdparm by executing ```sudo apt-get hdparm```
* Check HDD UUID with ```sudo blkid```
* Add the UUID to ```hdparm.service```
* Copy ```hdparm.service``` to ```/lib/systemd/system/multi-user.target.wants/```
* Execute the following commands:
    * ```sudo systemctl daemon-reload```
    * ```sudo systemctl status hdparm.service```
    * ```sudo systemctl enable hdparm.service```
    * ```sudo systemctl start hdparm.service```
    * ```sudo hdparm -I /dev/sda1 /dev/sdb1```

## Helpful commands
### Updating and installing required packages
* ```sudo apt-get update```
* ```sudo apt-get upgrade```
* ```sudo blkid```
* ```sudo systemctl restart smbd```
* ```sudo systemctl daemon-reload```
* ```sudo systemctl restart deluged```
* ```sudo watch "vcgencmd measure_temp && hdparm -C /dev/sda1 && vcgencmd pm_get_status"```

## Useful links
* https://dev.deluge-torrent.org/wiki/UserGuide/Service/DebianUbuntuInitd - Init script for deluged and deluge-web application to launch simultaneously at launch with the configuration to connect the deluge-daemon to each other automatically without requiring configuration at startup.
* https://github.com/pi-hole/pi-hole/#one-step-automated-install - Repository for Pi-hole containing more detailed instructions.
* https://docs.pi-hole.net/guides/dns/unbound/ - Instructions to configure a reverse DNS server using unbound.
* https://www.pivpn.io/ && https://hndrk.blog/tutorial-pihole-pivpn/ - Instructions to create a OVPN or WireGuard VPN that uses Pi-Hole to filter traffic.
* https://www.htpcguides.com/spin-down-and-manage-hard-drive-power-on-raspberry-pi/ - Guide to spin down, rest the actuator arm and manage hdd usage to increase longevity.
* https://manpages.ubuntu.com/manpages/bionic/man5/hdparm.conf.5.html - hdparm configuration
* https://man7.org/linux/man-pages/man8/hdparm.8.html - hdparm man page
* https://pimylifeup.com/headless-raspberry-pi-setup/ - Guide to creating a headless raspberry pi.
* https://pimylifeup.com/raspberry-pi-nfs/ - Setting up NFS server
* https://pimylifeup.com/raspberry-pi-nfs-client/ - Setting up NFS Client
* https://pimylifeup.com/raspberry-pi-plex-server/ - Setting up Plex Server
