from string import Template

docker = Template(r'''
    docker build --tag $APP_NAME:1.0 .
    docker stop $APP_NAME
    docker rm $APP_NAME
    docker run --publish $PORT:3000 --restart always --detach --name $APP_NAME $APP_NAME:1.0
''')

restart_nginx = r'''
    sudo systemctl restart nginx.service
'''

react = Template(r'''
    npm install
    npm run build
''')

jekyll = Template(r'''
    bundle
    jekyll build
''')

svelte = Template(r'''
    npm install
    npm run export
''')






