from string import Template


installThis=Template('''
    # install node
    sudo apt update 
    curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
    sudo apt --assume-yes -y install nodejs
    sudo apt --assume-yes -y install npm
    sudo npm install -g pm2
''')