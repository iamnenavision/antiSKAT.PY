#!/bin/bash
echo -e "Введите API-KEY-TG!"
read KEY
echo -e $KEY
docker build -t bot --build-arg KEY_TG=$KEY .
docker run --rm -e KEY_TG=$KEY bot