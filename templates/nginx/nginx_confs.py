from string import Template

# nginx proxy pass to localhost configuration
proxy_conf = Template(r'''

# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 5M;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
        proxy_pass http://127.0.0.1:$PORT/;
        proxy_read_timeout 1800;
        proxy_connect_timeout 1800;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
    }
}
''')

# nginx proxy pass to localhost configuration
react_conf = Template(r'''
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 5M;


    root $DIRECTORY;
    index index.html index.htm;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
                try_files $uri $uri/ /index.html;
    }
    error_page 500 502 503 505 /500.html;

    location /api/ {
        proxy_pass https://$PROXY/;
    }

    error_page 500 502 503 505 /500.html;
}

''')

# nginx proxy pass to localhost configuration
jekyll_conf = Template(r'''
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 5M;


    root $DIRECTORY;
    index index.html index.htm;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
                try_files $uri $uri/ /index.html;
    }
    error_page 500 502 503 505 /500.html;

    error_page 500 502 503 505 /500.html;
}

''')

# nginx proxy pass to localhost configuration
static_conf = Template(r'''
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 5M;

    root $DIRECTORY;
    index index.html index.htm;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
                try_files $uri $uri/ /index.html;
    }
    error_page 500 502 503 505 /500.html;

    error_page 500 502 503 505 /500.html;
}

''')

dir_react=Template(r'''/srv/www/$SITE_NAME/build/''')
dir_jekyll=Template(r'''/srv/www/$SITE_NAME/_site/''')
dir_static=Template(r'''/srv/www/$SITE_NAME/''')
dir_svelte=Template(r'''/srv/www/$SITE_NAME/__sapper__/export/''')



