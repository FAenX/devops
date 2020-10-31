from string import Template

common = Template(r'''
    # create a post-receive file
    #!/bin/bash
    
    # Deploy the content to the temporary directory
    git --work-tree=$TMP --git-dir=$GIT checkout -f || exit
    # Do stuffs, like npm install
    $REACT

    # Replace the content of the production directory
    rm -r $WWW/* || exit
    mv $TMP $WWW || exit

    #insert lines here for the app version 
    $NGINX
    $DOCKER
''')