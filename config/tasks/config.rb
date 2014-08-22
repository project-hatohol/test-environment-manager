task 'config' => 'load_containers' do

  @containers.each do |container_name, container|

    puts "Apply settings to container: #{container_name}"

    if container.has_key?('ipaddress')
      puts "IP Address Setting"
      config_ipaddress(container)
      puts "IP Address:#{container['ip_address']}"
    end

    if container.has_key?('zabbix-server')
      puts "Zabbix Server Setting"
      config_zabbix_server(container)
    end

    if container.has_key?('zabbix-agent')
      puts "Zabbix Agent Setting"
      config_zabbix_agent(container)
    end

    if container.has_key?('nagios')
      puts "Nagios Setting"
      config_nagios(container)
    end

    if container.has_key?('hatohol')
      puts "Hatohol Setting"
      config_hatohol(container)
    end

    if container.has_key?('redmine')
      puts "Redmine Setting"
      config_redmine(container)
    end
  end
end

def config_ipaddress(container)

  open("#{container['container_path']}/config","r+") do |f|
    f.flock(File::LOCK_EX)
    config = f.read

    if config.match(/^(?!.*#)\s*lxc.network.ipv4\s*=.*/)
      config.sub!(/^(?!.*#)\s*lxc.network.ipv4\s*=.*/, "lxc.network.ipv4=#{container['ipaddress']}")
    elsif
      config.concat("#Added by test-environment-manager\n")
      config.concat("lxc.network.ipv4=#{container['ipaddress']}")
    end

    f.rewind
    f.puts config
    f.truncate(f.tell)
    f.close
  end

  open("#{container['container_path']}/rootfs/etc/sysconfig/network-scripts/ifcfg-eth0","r+") do |f|
    f.flock(File::LOCK_EX)
    config = f.read

    if config.match(/^(\s*)BOOTPROTO\s*=.*/)
      config.sub!(/^(\s*)BOOTPROTO\s*=.*/, "BOOTPROTO=static")
    elsif
      config.concat("BOOTPROTO=static")
    end

    f.rewind
    f.puts config
    f.truncate(f.tell)
    f.close
  end
end

def config_zabbix_server(container)
  open("#{container['container_path']}/rootfs/etc/zabbix/zabbix_server.conf","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    if
      body.match(/^(?!.*#)\s*DBHost\s*=.*/)
      body.sub!(/^(?!.*#)\s*DBHost\s*=.*/,"\nDBHost=localhost")
    elsif
      body.concat("\n#Added by test-environment-manager\n")
      body.concat("DBHost=localhost\n")
    end

    if
      body.match(/^(?!.*#)\s*DBName\s*=.*/)
      body.sub!(/^(?!.*#)\s*DBName\s*=.*/,"\nDBName=#{container['zabbix-server']['database_name']}")
    elsif
      body.concat("\n#Added by test-environment-manager\n")
      body.concat("DBName=#{container['zabbix-server']['database_name']}\n")
    end
    
    if
      body.match(/^(?!.*#)\s*DBUser\s*=.*/)
      body.sub!(/^(?!.*#)\s*DBUser\s*=.*/,"\nDBUser=#{container['zabbix-server']['database_username']}")
    elsif
      body.concat("\n#Added by test-environment-manager\n")
      body.concat("DBUser=#{container['zabbix-server']['database_username']}")
    end
    
    if
      body.match(/^(?!.*#)\s*DBPassword\s*=.*/)
      body.sub!(/^(?!.*#)\s*DBPassword\s*=.*/,"\nDBPassword=#{container['zabbix-server']['database_password']}")
    elsif
      body.concat("\n#Added by test-environment-manager\n")
      body.concat("DBPassword=#{container['zabbix-server']['database_password']}")
    end
    
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  open("#{container['container_path']}/rootfs/etc/httpd/conf.d/zabbix.conf","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    if
      body.match(/^(?!.*#)\s*php_value\s*date.timezone.*/)
      body.sub!(/^(?!.*#)\s*php_value\s*date.timezone.*/,"php_value date.timezone Asia/Tokyo")
    elsif
      body.concat("\n#Added by test-environment-manager\n")
      body.concat("php_value date.timezone Asia/Tokyo")
    end
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end
end

def config_zabbix_agent(container)
  open("#{container['container_path']}/rootfs/etc/zabbix/zabbix_agentd.conf","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    body.sub!(/^(?!.*#)\s*Server\s*=.*/,"Server=#{container['zabbix-agent']['server_ipaddress']}");
    body.sub!(/#\s*ListenIP\s*=.*/,"ListenIP=#{container['ipaddress']}");
    body.sub!(/^(?!.*#)\s*Hostname\s*=.*/,"Hostname=#{container['zabbix-agent']['host_name']}");
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end
end

def config_nagios(container)
  open("#{container['container_path']}/rootfs/etc/nagios/nagios.cfg","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    p body.class
    if body.match(/^(?!.*#)\s*broker_module\s*=.*/)
      body.sub!(/^(?!.*#)\s*broker_module\s*=.*/,"broker_module=/usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg");
    elsif
      body.concat("#Added a broker_module\n");
      body.concat("broker_module=/usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg\n");
    end
    #print body
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  open("#{container['container_path']}/rootfs/etc/nagios/ndo2db.cfg","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    body.sub!(/db_name\s*=.*/,"db_name=#{container['nagios']['database_name']}");
    body.sub!(/(?<!ndo2)db_user\s*=.*/,"db_user=#{container['nagios']['database_username']}");
    body.sub!(/db_pass\s*=.*/,"db_pass=#{container['nagios']['database_password']}");
    #print body
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end
end

def config_hatohol(container)
end

def config_redmine(container)

  database_config_path = File.join(container['container_path'],'rootfs/var/lib/redmine/config/database.yml');
  database_config_example_path = database_config_path + '.example'

  database_config = YAML::load_file(database_config_path);

  database_config['production']['database'] = container['redmine']['database_name']
  database_config['production']['username'] = container['redmine']['database_username']
  database_config['production']['password'] = container['redmine']['database_password']

  open(database_config_path,'w') do |f|
    YAML::dump(database_config,f);
  end

  puts "Settings saved as #{database_config_path}"
end
