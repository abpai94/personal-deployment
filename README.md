# Raspbery Pi Configuration
This repository should contain the instructions and configuration files to set up the raspberry pi's named Franklin and Eleanor. The instructions should help configure them with the following utilities.

## Franklin
* Recursive DNS
* Pi-Hole
* Pi-VPN
* Mount NFS
* Deluge
* Jellyfin
* Radarr
* Sonarr
* Jackett

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

### Enable Hardware Encoding
* Add ```dtoverlay=rpivid-v4l2``` to ```/boot/config.txt```

#### GPIO Fan
* Add ```dtoverlay=gpio-fan,gpiopin=3,temp=60000``` to ```/boot/config.txt```
* Copy ```fancontrol.py``` to ```/home/pi/fancontrol```
* Copy ```fancontrol.service``` to ```/lib/systemd/system/fancontrol.service```
* Execute the following commands:
    * ```sudo systemctl daemon-reload```
    * ```sudo systemctl enable fancontrol.service```
    * ```sudo systemctl start fancontrol.service```

#### NFS Client
* Execute ```sudo apt-get install nfs-common -y```
* Copy NFS FSTAB configuration to ```/etc/fstab```
* Execute ```sudo mount -a```

#### Deluge (http://hostname:8112)
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

#### Pi-Hole (http://hostname:80) & PiVPN
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
* Run the following script ```curl -L https://install.pivpn.io | bash``` and follow the instructions choosing WireGuard

#### Jellyfin (http://hostname:8096)
* Execute ```sudo apt install apt-transport-https lsb-release```
* Execute ```curl https://repo.jellyfin.org/debian/jellyfin_team.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/jellyfin-archive-keyring.gpg >/dev/null```
* Execute ```echo "deb [signed-by=/usr/share/keyrings/jellyfin-archive-keyring.gpg arch=$( dpkg --print-architecture )] https://repo.jellyfin.org/debian $( lsb_release -c -s ) main" | sudo tee /etc/apt/sources.list.d/jellyfin.list```
* Execute ```sudo apt-get update```
* Execute ```sudo apt install jellyfin```
* Set-up Jellyfin

#### Radarr (http://hostname:7878)
* Execute ```wget --content-disposition 'http://radarr.servarr.com/v1/update/master/updatefile?os=linux&runtime=netcore&arch=arm'```
* Extract tarball ```tar -xvzf Radarr*.linux*.tar.gz```
* Move extracted contents ```sudo mv Radarr /opt/```
* Change Permission ```sudo mv Radarr /opt/```
* Copy ```radarr.service``` to ```/etc/systemd/system/radarr.service```
* Reload systemd ```sudo systemctl daemon-reload```
* Enable Radarr service ```sudo systemctl enable radarr.service```
* Start Radarr service ```sudo systemctl start radarr.service```
* Delete Radarr tarball ```rm Radarr*.linux*.tar.gz```

#### Sonarr (http://hostname:8989)
* Retrieve apt repository key ```sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 2009837CBFFD68F45BC180471F4F90DE2A9B4BF8```
* Add apt source list ```echo "deb https://apt.sonarr.tv/debian buster main" | sudo tee /etc/apt/sources.list.d/sonarr.list```
* Update local package list ```sudo apt update```
* Install Sonarr ```sudo apt install sonarr```

#### Jackett (http://hostname:9117)
* Retrieve Jackett Binaries ```wget https://github.com/Jackett/Jackett/releases/download/<version>/Jackett.Binaries.LinuxARM32.tar.gz```
* Extract tarball ```tar xvf Jackett.Binaries.LinuxARM32.tar.gz```
* Execute ```sudo Jackett/./install_service_systemd.sh```

### Setting up Eleanor

#### Rock-Pi SATA
* Execute the script ```curl -sL https://rock.sh/get-rockpi-sata | sudo -H -E bash -```
* Copy ```fan.py``` to ```/usr/bin/rockpi-sata/```
* Copy ```rockpi-sata.conf``` to ```/etc/```

#### Delete filesystem, RAID configuration and mount md0/1
* Execute ```sudo fdisk /dev/disk/<hdd uuid>``` and choose ```d``` and ```w``` for all the following drives
    * ```ata-ST1000LM024_HN-M101MBB_S30CJAEF433469```
    * ```ata-HGST_HTS721010A9E630_JR10004M22L7UF```
    * ```ata-TOSHIBA_MQ01ABD100_96G7C6MLT```
    * ```ata-ST1000LM048-2E7172_ZKP2QKJJ```
* Create a RAID 1 instance with 2 HDDs
    * ```sudo mdadm --verbose --create --level=1 /dev/md0 --raid-devices=2 /dev/disk/by-id/ata-ST1000LM024_HN-M101MBB_S30CJAEF433469 /dev/disk/by-id/ata-HGST_HTS721010A9E630_JR10004M22L7UF```
    * ```sudo mdadm --verbose --create --level=1 /dev/md1 --raid-devices=2 /dev/disk/by-id/ata-ST1000LM048-2E7172_ZKP2QKJJ /dev/disk/by-id/ata-TOSHIBA_MQ01ABD100_96G7C6MLT```
* Detect existing RAID configuration
   * ```sudo mdadm --verbose --assemble /dev/md0 /dev/disk/by-id/ata-ST1000LM024_HN-M101MBB_S30CJAEF433469 /dev/disk/by-id/ata-HGST_HTS721010A9E630_JR10004M22L7UF```
   * ```sudo mdadm --verbose --assemble /dev/md1 /dev/disk/by-id/ata-ST1000LM048-2E7172_ZKP2QKJJ /dev/disk/by-id/ata-TOSHIBA_MQ01ABD100_96G7C6MLT```
* Enable Read-Write on RAID
    * ```sudo mdadm --readwrite /dev/md0```
    * ```sudo mdadm --readwrite /dev/md1```
* Add ext4 filesystem and partition
    * ```sudo mkfs -t ext4 /dev/disk/by-id/md-uuid-4b99e74b:24828ab4:56bf833a:75473490```
    * ```sudo mkfs -t ext4 /dev/disk/by-id/md-uuid-11435132:302ccabd:aa2b0572:b8ed9f50```
* Mount all partitions from ```fstab``` file to ```/etc/fstab```
* Copy ```mdadm.conf``` to ```/etc/mdadm/mdadm.conf```
* Execute ```update-initramfs -u```

#### NFS Server
* Execute ```sudo apt-get install nfs-kernel-server```
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
* ```sudo watch "cat /proc/mdstat"```
* ```sudo watch "mdadm --detail /dev/md0"```

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
* https://pimylifeup.com/raspberry-pi-jellyfin/ - Jellyfin server installation instructions
* https://wiki.servarr.com/radarr/installation#linux - Radarr configuration instructions
* https://sonarr.tv/#downloads-v3-linux-debian - Sonarr installation instructions
* https://github.com/Jackett/Jackett - Jackett installation instructions