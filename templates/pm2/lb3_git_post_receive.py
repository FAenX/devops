from string import Template

pm2 = Template(r'''
    #stop and start the pm2 app
    pm2 stop $APP_NAME
    pm2 start server/server.js --name $APP_NAME
''')