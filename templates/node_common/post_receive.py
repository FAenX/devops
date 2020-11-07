from string import Template

common = Template(r'''
    # create a post-receive file
    #!/bin/bash
    
    # Deploy the content to the temporary directory
    git --work-tree=$TMP --git-dir=$GIT checkout -f || exit

    # Replace the content of the production directory
    cd $WWW || exit
    pwd
    rm -rf .\/* || exit
    mv $TMP\/* $WWW || exit

     # Do stuffs, like npm install
    $REACT
    $JEKYLL

    #insert lines here for the app version 
    $NGINX
    $DOCKER
''')