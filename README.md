# Personal Deployment
This repository tracks the journey of deploying services on my raspberry pi's named Franklin and Eleanor. I use Ansible to configure each of them and deploy docker containers in order to self-host services that I wish to use for my personal use. 

## Franklin
* Dashboard (https://dashboard.abhishekpai.co.uk)
* Pi-Hole (https://pihole.abhishekpai.co.uk/admin)
* Wireguard (https://wireguard.abhishekpai.co.uk)
* Traefik (https://traefik.abhishekpai.co.uk)
* DDClient
* Portainer (https://portainer.abhishekpai.co.uk)
* Vaultwarden (https://vault.abhishekpai.co.uk)
* Authelia (https://auth.abhishekpai.co.uk)
* Personal Website (https://www.abhishekpai.co.uk)

## Eleanor
* RAID 0
* Deluge (https://deluge.abhishekpai.co.uk)
* Jellyfin (https://jellyfin.abhishekpai.co.uk)
* Radarr (https://radarr.abhishekpai.co.uk)
* Sonarr (https://sonarr.abhishekpai.co.uk)
* Prowlarr (https://prowlarr.abhishekpai.co.uk)
* Nextcloud (https://cloud.abhishekpai.co.uk)

## Setup
* Configure a password for ansible vault in `~/.secrets/ansible-password` file or change the location in `ansible.cfg`
* `main.yml` contains all the playbooks which will be executed
* Execute playbooks with the following command: `ansible-playbook -i inventory.yml -i vault.yml main.yml`