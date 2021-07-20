#!/bin/bash

git config pull.rebase false
git config user.name "p1ratrulezzz"
git config user.email "git@p1ratrulezzz.me"
KEY_PATH=$(pwd -P)"/deployment-private.key"
KEY_PATH_PUB=$(pwd -P)"/deployment-public.key"
echo "${SSH_PUBKEY}" > "${KEY_PATH_PUB}"
echo "Adding an SSH key to agent"
eval $(ssh-agent -s)
touch "${KEY_PATH}"
chmod 0600 "${KEY_PATH}"
echo "${SSH_PRIVATEKEY}" > "${KEY_PATH}"
ssh-add -t 3600 "${KEY_PATH}"

echo "Installing python3 and dependencies"
sudo apt install -y python3-venv git
echo "Creating venv"
python3 -m venv venv

echo "Checkout master"
git fetch origin
git checkout -b master origin/master
git pull origin master

#echo "Initializing spotify.yml"
#echo "${SPOTIFY_YML}" > spotify.yml

echo "Activating venv"
source venv/bin/activate || exit 1
pip3 install -r requirements.txt

echo "Parsing data and rebuild readme..."
python3 rebuild_readme.py

echo "Add to git"
git add README.md resources
git commit -m"[skip-ci] CI update"
git push -f origin master
rm -f "${KEY_PATH_PUB}"
rm -f "${KEY_PATH_PUB}"
