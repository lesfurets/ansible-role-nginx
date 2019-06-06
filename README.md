Nginx
=========

[![Build Status](https://travis-ci.org/lesfurets/ansible-role-nginx.svg?branch=master)](https://travis-ci.org/lesfurets/ansible-role-nginx)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ansible Galaxy: lesfurets.nginx](https://img.shields.io/badge/galaxy-lesfurets.nginx-blueviolet.svg)](https://galaxy.ansible.com/lesfurets/nginx)

Ansible role to install nginx from system package

## Dependencies

Role **lesfurets.epel** is used for RedHat/CentOS.

## Role Variables

Variables are available to configure nginx and to define the various virtual hosts and upstreams.
You can also provide a list of nginx capable users. This will add these users to the nginx group.


### Nginx configuration variables

Configuration paths variables:
- **nginx_conf_path**: sets the config path. Default is `/etc/nginx/conf.d`.
- **nginx_conf_file_path**: sets the main configuration file path. Default is `/etc/nginx/nginx.conf`.
- **nginx_mime_file_path**: sets the path the the mime file. Default is `/etc/nginx/mime.types`.

Log configuration variables:
- **nginx_error_log**: sets the path for the error log file and log options. Default is `/var/log/nginx/error.log warn`.
- **nginx_access_log**: sets the path for the access log file and log options. Default is `/var/log/nginx/access.log main buffer=16k flush=2m`

Worker processes configuration variables:
- **nginx_worker_processes**: sets the worker processes configuration. Default depends on the fact `ansible_processor_vcpus` or `ansible_processor_count`.
- **nginx_worker_connections**: sets the max number of connection per worker. Default is `1024`.
- **nginx_multi_accept**: sets the multi_accept parameter for nginx conf [(source)](http://nginx.org/en/docs/ngx_core_module.html#multi_accept). Default is `off`.

TCP connection options variables [(doc)](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/#optimizing-performance-for-serving-content):
- **nginx_sendfile**: sets the sendfile parameter. Default is `on`.
- **nginx_tcp_nopush**: sets the tcp_nopush parameter. Default is `on`.
- **nginx_tcp_nodelay**: sets the tcp_nodelay parameter. Default is `on`.

Nginx keepalive settings:
- **nginx_keepalive_timeout**: sets the keepalive_timeout parameter (in seconds). Default is `65`.
- **nginx_keepalive_requests**: sets the keepalive_requests parameter. Default is `100`.

Nginx behaviour settings:
- **nginx_server_tokens**: sets the server_tokens parameter (whether nginx version is present in responses headers). Default is `on`.
- **nginx_client_max_body_size**: sets the client_max_body_size parameter (max file upload size). Default is `64m`.
- **nginx_server_names_hash_bucket_size**: sets the server_names_hash_bucket_size parameter. Default value is `64`.
- **nginx_proxy_cache_path**: sets the proxy_cache_path parameter : path and settings (e.g. `/var/cache/nginx keys_zone=cache:32m`). Not configured by default.


- **nginx_extra_conf_options**: is an optional set of parameters (plain nginx conf) to be inserted at the top of the main configuration file. Default is empty.
- **nginx_extra_http_options**: is an optional set of parameters (plain nginx conf) to be inserted in the top-level http block of the main configuration file. Default is empty.

- **nginx_capable_users**: is a list of users that will be added to the nginx group. This is useful for example when you setup a webservice and you want to proxy_pass on a socket owned by said user.

### Virtual host variables

- **nginx_remove_default_vhost**: can be set to true to remove the default nginx virtual host. Default value is false

**nginx_vhosts**: is a list of variables to setup nginx virtualhosts :
- vhost server block variables:
  - **listen**: sets the port number to listen on. Default is `80`.
  - **server_name**: sets the server name for the virtualhost. Is used as a fallback for the vhost filename.
  - **root**: *Optional*, sets the webserver root directory. Default is unset.
  - **index**: *Optional*, sets the index parameter. (e.g. `index.html index.htm`).
  - **filename**: *Optional*, sets the vhost filename.
  - **error_page**: *Optional*, sets the error page parameter.
  - **access_log**: *Optional*, sets the access log parameter
  - **error_log**: *Optional*, sets the error log parameter
  - **extra_parameters**: *Optional*, cant be used to add plain nginx conf in the vhost server block.
- SSL related variables:
  - **use_ssl**: *Optional*, when set to true, adds the `ssl on;` directive to the vhost server block.
  - **redirect_http_https**: *Optional*, when set to true, adds a server block that listen on port 80 and redirect to `https://$host$request_uri;`
  - **ssl_params**: *Optional*, a list of SSL parameters to add: [] # list of ssl parameters to apply. Default is 
  ```ssl_certificate: '/etc/nginx/cert.crt'
  ssl_certificate_key: '/etc/nginx/cert.key'
  ssl_session_cache: 'builtin:1000  shared:SSL:10m'
  ssl_protocols: 'TLSv1 TLSv1.1 TLSv1.2'
  ssl_ciphers: 'HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4'
  ssl_prefer_server_ciphers 'on'
  ```
  - **locations**
    - vhost locations block variables:
    - **location**: sets the resource location (e.g. `/` or `/static`). Also accept a list of key/value parameters to configure the location block for the defined resource.
  - **state**: is used to decide whether vhost should be present or absent. Default is `present`.


Examples of setup are available in the section below.

## Example Playbook

### Example for webserver

```
- hosts: webservers
  vars:
    - nginx_vhosts:
      - server_name: "mywebsite.com"
        listen: "80"
        root: "/srv/www/mywebsite"
		index index.html;
		locations:
		  - location: "/"
		    try_files: "$uri $uri/ =404"
  roles:
    - lesfurets.nginx
```

### Example for reverse proxy with https

```
- hosts: reverse_proxy
  vars:
    - nginx_vhosts:
      - listen: "443"
        use_ssl: true
        redirect_http_https: true
        ssl_params:
          - ssl_certificate: "/srv/ssl/cert.pem"
          - ssl_certificate_key: "/srv/ssl/cert.key"
        locations:
          - location: "/"
            proxy_pass: "http://127.0.0.1:8080"
            proxy_set_header:
              - "Host $host"
              - "X-Real-IP $remote_addr"
              - "X-Forwarded-For $proxy_add_x_forwarded_for"
              - "X-Forwarded-Proto $scheme"
  roles:
    - lesfurets.nginx
```

## License

Licensed unter the GPLv3 License. See LICENSE file for details.
