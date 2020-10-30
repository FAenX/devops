from string import Template

docker = Template(r'''
    #stop and start the pm2 app
    cd $GIT_DIR || exit
    docker build --tag $APP_NAME:1.0 .
    docker run --publish $port:8080 --detach --name $APP_NAME $APP_NAME:1.0
''')



