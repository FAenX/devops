# devops

#### generate nginx confs 
example --react with proxy_pass conf

```bash
python3 nginx_conf.py --react example.com --proxy example.net
```

output

```bash
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

#### create project directories git repos and post-receive for various platforms
example --docker

```bash
python3 deploy_prep.py --docker --port 4000 app_name
```

output
```bash 
message: created folder /srv/git/app_name.git
message: created folder /srv/www/app_name
message: created folder /srv/tmp/app_name
message: successfully created git bare repo /srv/git/app_name.git
```

post-receive
```bash
    # create a post-receive file
    #!/bin/bash
    
    # Deploy the content to the temporary directory
    git --work-tree=/srv/tmp/app_name --git-dir=/srv/git/app_name.git checkout -f || exit

    # Replace the content of the production directory
    cd /srv/www/app_name || exit
    pwd
    rm -rf .\/* || exit
    mv /srv/tmp/app_name\/* /srv/www/app_name || exit
    
    docker build --tag app_name:1.0 .
    docker stop app_name
    docker rm app_name
    docker run --publish 4000:3000 --restart always --detach --name app_name app_name:1.0

```


