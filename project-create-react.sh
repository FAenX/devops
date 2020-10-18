#!/bin/bash


# When you push your code to the git repo,
# the `post-receive` hook will deploy the code
# in the $TMP directory, then copy it to $WWW.

DIR_TMP="/srv/tmp/"
DIR_WWW="/srv/www/"
DIR_GIT="/srv/git/"

if [ $# -eq 0 ]; then
	echo 'No project name provided (mandatory)'
	exit 1
else
	echo "- Project name:" "$1"
fi


GIT=$DIR_GIT$1.git
TMP=$DIR_TMP$1
WWW=$DIR_WWW$1

echo "- git:" "$GIT"
echo "- tmp:" "$TMP"
echo "- www:" "$WWW"

export GIT
export TMP
export WWW

function dir_create() {
	sudo mkdir -p "$1"
	sudo chgrp -R users "$1" # set the group
	sudo chmod -R g+rwX  "$1" # allow the group to read/write
	sudo chmod g+s `find "$1" -type d` # new files get group id of directory
}

dir_create "$TMP" 
dir_create "$WWW" 
dir_create "$GIT" 

# install node
sudo apt update 
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt --assume-yes -y install nodejs
sudo apt --assume-yes -y install npm

# Create a directory for the git repository
cd "$GIT" || exit

# Init the repo as an empty git repository
sudo git init --bare --shared=all 

cd hooks || exit

sudo touch post-receive

# create a post-receive file
sudo tee post-receive <<EOF
#!/bin/bash
# The production directory
WWW="${WWW}"
# A temporary directory for deployment
TMP="${TMP}"
# The Git repo
GIT="${GIT}"
# Deploy the content to the temporary directory
git --work-tree=\$TMP --git-dir=\$GIT checkout -f
# Do stuffs, like npm install
cd $TMP || exit

npm install

# Replace the content of the production directory
# with the temporary directory
cd $WWW || exit
sudo rm -r .\/*

cd $TMP || exit
sudo mv .\/* $WWW || exit

#enter the production directory
cd $WWW || exit
npm run build

sudo systemctl restart nginx.service
EOF

# make it executable
sudo chmod +x post-receive

echo "$GIT"
