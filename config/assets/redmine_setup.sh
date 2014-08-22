#!/bin/bash

service mysqld start
cd /var/lib/redmine
bundle install --without development test
bundle exec rake generate_secret_token
bundle exec rake --trace db:migrate RAILS_ENV=production
