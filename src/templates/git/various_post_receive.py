from string import Template

docker = Template('''
    docker build --tag $APP_NAME:1.0 .
    docker stop $APP_NAME
    docker rm $APP_NAME
    docker run --publish $PORT:3000 --restart always --detach --name $APP_NAME $APP_NAME:1.0
''')

react = '''
    npm install
    npm run build
    sudo systemctl restart nginx.service
'''

jekyll = '''
    npm install
    npm run build
    bundle
    bundle exec jekyll build
    sudo systemctl restart nginx.service
'''

svelte = '''
    npm install
    npm run export
    sudo systemctl restart nginx.service
'''

minikube = Template('''
    $MINIKUBE_DIR/kubectl apply -f $MANIFEST_PATH
''')





