#!/bin/bash

sudo chown pi.pi {{ home_directory }}/docker_config/wireguard/
sudo -u pi rsync -a --delete-after {{ home_directory }}/docker_config/wireguard /mnt/md0/docker_config/