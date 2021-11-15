#!/bin/bash

apt-get update
apt-get install -y pipenv git python3 python3-pip default-libmysqlclient-dev
git clone https://github.com/Ebenolt/access-pc
cd access-pc
pipenv install