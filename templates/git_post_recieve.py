from string import Template

post_recieve_common = Template(r'''
    # create a post-receive file
    #!/bin/bash
    
    # Deploy the content to the temporary directory
    git --work-tree=$TMP --git-dir=$GIT checkout -f || exit
    # Do stuffs, like npm install
    cd $TMP || exit

    npm install

    # Replace the content of the production directory
    # with the temporary directory
    cd $WWW || exit
    rm -r .\/*

    cd $TMP || exit
    mv .\/* $WWW || exit

    #enter the production directory
    cd $WWW || exit
    npm run build

    #insert lines here for the app version 
    $START_SERVER
''')

pm2_dist_index_js = Template(r'''
    #stop and start the pm2 app
    pm2 stop $APP_NAME
    pm2 start dist/index.js --name $APP_NAME
''')

pm2_server_server_js = Template(r'''
    #stop and start the pm2 app
    pm2 stop $APP_NAME
    pm2 start server/server.js --name $APP_NAME
''')

restart_nginx = Template(r'''
    restart nginx
    sudo systemctl restart nginx.service
''')