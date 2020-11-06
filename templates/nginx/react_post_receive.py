from string import Template

react = Template(r'''
    #stop and start the pm2 app
    cd $TMP || exit
    npm install
    npm run build
''')



