from string import Template

cache_directive = Template('''
proxy_cache_path /var/nginx/$SITE_NAME levels=1:2 
keys_zone=$SITE_NAME:10m max_size=10g inactive=1w use_temp_path=off;
''')

cache = Template('''
        proxy_cache $SITE_NAME;
        proxy_cache_revalidate on;
        proxy_cache_min_uses 3;
        proxy_cache_use_stale error timeout updating http_500 http_502
                              http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;
''')

static_common = Template('''
$CACHE_DIRECTIVE
#server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 50M;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    root $DIRECTORY;
    index index.html index.htm;

    location / {
        $CACHE
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        $CACHE
        proxy_pass https://$PROXY/;    
    }

}
''')

# nginx proxy pass to localhost configuration
reverse_proxy = Template('''
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 50M;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
        proxy_pass http://127.0.0.1:$PORT/;
        
    }
}
''')

# nginx proxy pass to a socket configuration
socket_proxy = Template('''
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 50M;
     access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/$ROOT_DIR/$SOCKET;
        uwsgi_buffering off;  # <-- this line is new
        
    }
}
''')



dir_react=Template('''/srv/www/$SITE_NAME/build/''')
dir_jekyll=Template('''/srv/www/$SITE_NAME/_site/''')
dir_static=Template('''/srv/www/$SITE_NAME/''')
dir_svelte=Template('''/srv/www/$SITE_NAME/__sapper__/export/''')



    

