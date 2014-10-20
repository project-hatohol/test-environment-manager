#!/bin/sh

bundle install --without development test
bundle exec rake generate_secret_token
RAILS_ENV=production bundle exec rake db:migrate
passenger-install-apache2-module --snippet > /etc/httpd/conf.d/passenger.conf
mysql -uroot db_redmine < my_setting
chown -R apache /var/lib/redmine
chgrp -R apache /var/lib/redmine
