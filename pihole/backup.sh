#!/bin/bash

docker exec -it pihole pihole -a -t /etc/pihole/backup.tar.gz
sudo chown pi.pi {{ home_directory }}/docker_config/pihole/
sudo -u pi rsync -a --delete-after {{ home_directory }}/docker_config/pihole/etc-pihole/backup.tar.gz /mnt/md0/docker_config/pihole/backup.tar.gz