# devops

#### generate nginx confs 

```sh
python3 nginx_conf.py --react example.com --proxy example.net
```

output

```sh
proxy_cache_path /var/nginx/example levels=1:2 
keys_zone=example:10m max_size=10g inactive=1w use_temp_path=off;

#server
server{
    # SSL Configuration
    server_name example.com;
    client_max_body_size 50M;

    access_log  /var/log/nginx/example.com.access.log;
    error_log   /var/log/nginx/example.com.error.log;

    root /srv/www/example/build/;
    index index.html index.htm;

    location / {
        
        proxy_cache example;
        proxy_cache_revalidate on;
        proxy_cache_min_uses 3;
        proxy_cache_use_stale error timeout updating http_500 http_502
                              http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        
        proxy_cache example;
        proxy_cache_revalidate on;
        proxy_cache_min_uses 3;
        proxy_cache_use_stale error timeout updating http_500 http_502
                              http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        proxy_pass https://example.net/;    
    }

}

```

#### create project directories and git repo plus post-receive script to build the application

