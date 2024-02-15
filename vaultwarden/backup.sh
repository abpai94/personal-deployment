#!/bin/bash

sudo docker stop vaultwarden
sudo chown pi.pi {{ home_directory }}/docker_config/vaultwarden/
sudo -u pi rsync -a --delete-after {{ home_directory }}/docker_config/vaultwarden /mnt/md0/docker_config/
sudo docker start vaultwarden