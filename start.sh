#!/bin/bash
echo -e "Введите API-KEY-TG!"
read KEY
echo -e $KEY
sudo docker build -t bot --build-arg KEY_TG=$KEY .
sudo docker run --name=bot --rm -e KEY_TG=$KEY bot