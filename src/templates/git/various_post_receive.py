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
#!/bin/bash

SITE_NAME=$APP_NAME
SITE_PATH=$APP_DIR

echo "**** $SITE_NAME [post-receive] hook received."

while read oldrev newrev ref
do
  branch_received=`echo $ref | cut -d/ -f3`

  echo "**** Received [$branch_received] branch."
 
  # Making sure we received the branch we want.
 
  # checkout the new version
  echo "**** Checking out branch."
  GIT_WORK_TREE=$APP_DIR git checkout -f $branch_received 
 
done

cd $APP_DIR
docker build --tag $APP_NAME:latest .
docker image tag $APP_NAME:latest $DOCKER_REGISTRY/devops/$APP_NAME:$branch_received
docker push $DOCKER_REGISTRY/devops/$APP_NAME:$branch_received
$MINIKUBE_DIR/kubectl apply -f $MANIFEST_PATH

echo "**** Done."


''')





