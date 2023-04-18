#!/bin/bash
sleep 60s
sudo mdadm --readwrite /dev/md0 /dev/md1
sudo mount /dev/md0 /media/md0
sudo mount /dev/md1 /media/md1
sudo exportfs -ra