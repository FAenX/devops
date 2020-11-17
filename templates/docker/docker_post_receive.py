from string import Template

docker = Template(r'''
    #stop and start the pm2 app
    cd $WWW || exit
    docker build --tag $APP_NAME:1.0 .
    docker stop $APP_NAME
    docker rm $APP_NAME
    docker run --publish $PORT:3000 --restart always --detach --name $APP_NAME $APP_NAME:1.0
''')



