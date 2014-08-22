#!/bin/bash -x

service mysqld start
cd /var/lib/redmine
bundle install --without development test
bundle exec rake generate_secret_token
bundle exec rake rake db:migrate RAILS_ENV=production
