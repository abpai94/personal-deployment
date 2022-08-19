# Raspbery Pi Configuration
This repository should contain the instructions and configuration files to set up the raspberry pi as a media server and recursive DNS.

## Instructions
### Deluge
* Execute ```sudo apt-get install deluged deluge-web```
* Copy ```deluge``` script to ```/etc/init.d/```
* Delete existing ```deluged-daemon``` script
* Execute ```sudo systemtctl daemon-reload```
* Add the line from ```web.conf``` to ```/home/<user>/.config/deluge/web.conf```
* Modify and copy ```deluged-config``` to ```/etc/defaults/deluged```
* Configure deluge

### HDD mount
* Execute ```sudo blkid``` and take a note of the UUID of the storage drive
* Add ```UUID=<Storage UUID> /media/hdd ntfs defaults,auto,users,rw,nofail,umask=000 0 0``` with custom modifications to ```/etc/fstab``` file
* Execute ```sudo reboot```

### Pi-Hole
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

### HDD Maintainance
* Install hdparm by executing ```sudo apt-get hdparm```
* Check HDD ID with ```sudo blkid```
* Add the configuration in ```hdparm.conf``` to ```/etc/hdparm.conf```
* Restart Raspberry Pi

### DuckDNS
* Copy ```duck.sh``` to ```~/duckdns/```
* Execute ```chmod 700 duck.sh```
* Execute ```crontab -e```
* Add ```*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1``` to the cron config
* Start cron service ```sudo service cron start```
* Test ```./duck.sh``` and check logs ```cat duck.log```

### OpenVPN
* Download the following script ```wget https://github.com/Nyr/openvpn-install/raw/master/openvpn-install.sh```
* Change permissions ```chmod 755 openvpn-install.sh```
* Run the script as admin ```sudo ./openvpn-install.sh```
* Script configuration use ```UDP``` with ```443```
* Restart OVPN services ```sudo systemctl restart openvpn-iptables.service openvpn-server@server.service```
* Add the configuration ```interface=tun0``` && ```interface=eth0``` to ```/etc/dnsmasq.d/01-pihole.conf```
* Add the configuration ```PIHOLE_INTERFACE=tun0``` to ```/etc/pihole/setupVars.conf```

## Helpful commands
### Updating and installing required packages
* ```sudo apt-get update```
* ```sudo apt-get upgrade```
* ```sudo blkid```
* ```sudo systemctl restart smbd```
* ```sudo systemctl daemon-reload```
* ```sudo systemctl restart deluged```
* ```sudo watch "vcgencmd measure_temp && hdparm -C /dev/sda1 && vcgencmd pm_get_status"```

### Headless Raspberry Pi installation (Complete steps after writing Raspbian image to microSD)
* Create empty file called ```ssh```
* Configure and copy ```wpa_supplicant.conf```

## Useful links
* https://dev.deluge-torrent.org/wiki/UserGuide/Service/DebianUbuntuInitd - Init script for deluged and deluge-web application to launch simultaneously at launch with the configuration to connect the deluge-daemon to each other automatically without requiring configuration at startup.
* https://github.com/pi-hole/pi-hole/#one-step-automated-install - Repository for Pi-hole containing more detailed instructions.
* https://www.htpcguides.com/spin-down-and-manage-hard-drive-power-on-raspberry-pi/ - Guide to spin down, rest the actuator arm and manage hdd usage to increase longevity.
* https://pimylifeup.com/headless-raspberry-pi-setup/ - Guide to creating a headless raspberry pi.
* https://docs.pi-hole.net/guides/dns/unbound/ - Instructions to configure a reverse DNS server using unbound.
* https://discourse.pi-hole.net/t/see-my-pihole-enabled-openvpn-server/111/3 - Forum instructions regarding enabling external VPN traffic to use Pi-Hole to manage the DNS queries and filtering of traffice.
* https://pimylifeup.com/raspberry-pi-nfs/ - Setting up NFS server
* https://pimylifeup.com/raspberry-pi-nfs-client/ - Setting up NFS Client
* https://pimylifeup.com/raspberry-pi-plex-server/ - Setting up Plex Server