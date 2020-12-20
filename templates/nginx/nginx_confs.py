from string import Template

cache_directive = Template('''
    proxy_cache_path /var/nginx/$APP_NAME levels=1:2 
    keys_zone=$APP_NAME:10m max_size=10g inactive=24h use_temp_path=off;
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
        try_files $uri $uri/ /index.html;
        proxy_set_header       Host $host;
        proxy_buffering        on;
        proxy_cache            $APP_NAME;
        proxy_cache_valid      200  1d;
        proxy_cache_use_stale  error timeout invalid_header updating
                                   http_500 http_502 http_503 http_504;
    }

    location ~* .(svg|css|rss|atom|js|jpg|jpeg|gif|png|ico)$ {
        expires max;
        log_not_found off;
        access_log off;
    }
}
''')

# nginx proxy pass to localhost configuration
reverse_proxy = Template('''
$CACHE_DIRECTIVE
# server
server{
    # SSL Configuration
    server_name $SERVER_NAME;
    client_max_body_size 50M;

    access_log  /var/log/nginx/$SERVER_NAME.access.log;
    error_log   /var/log/nginx/$SERVER_NAME.error.log;

    location / {
        proxy_cache $APP_NAME;
        proxy_cache_revalidate on;
        proxy_cache_min_uses 3;
        proxy_cache_use_stale error timeout updating http_500 http_502
                              http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;
        proxy_pass http://127.0.0.1:$PORT/;
        
    }
}
''')


dir_react=Template('''/srv/www/$SITE_NAME/build/''')
dir_jekyll=Template('''/srv/www/$SITE_NAME/_site/''')
dir_static=Template('''/srv/www/$SITE_NAME/''')
dir_svelte=Template('''/srv/www/$SITE_NAME/__sapper__/export/''')



    

