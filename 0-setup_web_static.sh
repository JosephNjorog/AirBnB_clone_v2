#!/usr/bin/env bash
# sets up web servers for the deployment of web_static
apt-get update -y > /dev/null 2>&1
apt-get install nginx -y > /dev/null 2>&1
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "Hello from web_static" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '/^\tserver_name.*/a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
service nginx restart > /dev/null 2>&1
