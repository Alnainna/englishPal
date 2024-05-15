#!/bin/sh

DEPLOYMENT_DIR=/home/lanhui/englishpal2/EnglishPal
cd $DEPLOYMENT_DIR
pwd

# Stop service
sudo docker stop EnglishPal
sudo docker rm EnglishPal

# Rebuild container. Run this after modifying the source code.
sudo docker build -t englishpal .

# Run the application
sudo docker run --restart=always -d --name EnglishPal -p 90:80  -v ${DEPLOYMENT_DIR}/app/static/frequency:/app/static/frequency --mount type=volume,src=englishpal-db,target=/app/db -t englishpal # for permanently saving data

# Save space.  Run it after sudo docker run
sudo docker system prune -a -f
