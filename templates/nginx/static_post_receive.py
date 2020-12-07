from string import Template

react = Template(r'''
    #stop and start the pm2 app
    cd $WWW || exit
    npm install
    npm run build
''')

jekyll = Template(r'''
#stop and start the pm2 app
    cd $WWW || exit
    bundle
    jekyll build
''')

svelte = Template(r'''
#stop and start the pm2 app
    cd $WWW || exit
    npm install
    npm run export
''')



