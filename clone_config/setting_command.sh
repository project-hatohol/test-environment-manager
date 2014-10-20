#!/bin/sh

bundle install --without development test
bundle exec rake generate_secret_token
echo sakamoto
RAILS_ENV=production bundle exec rake db:migrate
passenger-install-apache2-module --snippet > /etc/httpd/conf.d/passenger.conf
echo masayuki
mysql -uroot db_redmine < my_setting
chown -R apache /var/lib/redmine
echo takashi
chgrp -R apache /var/lib/redmine
echo finish

