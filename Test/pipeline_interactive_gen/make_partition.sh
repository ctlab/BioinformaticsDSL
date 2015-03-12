#!/bin/bash

if [ -d "workdir" ]; then
	rm -rf workdir
fi

mkdir workdir
fallocate -l 500M workdir/ext4part.img
yes | mkfs -t ext4 workdir/ext4part.img

mkdir workdir/mntpoint
sudo mount workdir/ext4part.img workdir/mntpoint
echo $res
