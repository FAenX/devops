from string import Template

common = Template(r'''
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
    $DOCKER_BUILD_RUN_LINES
''')