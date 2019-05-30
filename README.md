Nginx
=========

[![Build Status](https://travis-ci.org/lesfurets/ansible-role-nginx.svg?branch=master)](https://travis-ci.org/lesfurets/ansible-role-nginx)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ansible Galaxy: lesfurets.nginx](https://img.shields.io/badge/galaxy-lesfurets.nginx-blueviolet.svg)](https://galaxy.ansible.com/lesfurets/nginx)

Ansible role to install nginx from system package

## Dependencies

Role **lesfurets.epel** is used for RedHat/CentOS.

## Role Variables

Variables are available to configure nginx and to define the varios virtual hosts.

Please have a look at the `defaults/main` for default values and examples.

Examples of setup are also available in the section below.

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
