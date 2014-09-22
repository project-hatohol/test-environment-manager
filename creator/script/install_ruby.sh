#!/bin/sh

RUBY_DIR=ruby-2.0.0-p481

cd $RUBY_DIR
./configure --disable-install-doc
make
make install
cd ../
