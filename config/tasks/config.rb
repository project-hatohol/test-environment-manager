@containers.each do |container_name, container|
  namespace container_name do
    desc "Configure Container:#{container_name}"
    task 'config' do
      puts "Apply settings to container: #{container_name}"

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
        config_redmine(container_name, container)
      end

      if container.has_key?('ipaddress')
        puts "IP Address Setting"
        config_ipaddress(container)
        puts "IP Address:#{container['ip_address']}"
      end
    end
  end
end

namespace 'all' do
  desc 'Configure All Containers'
  task 'config' do

    @containers.each do |container_name, container|

      puts "Apply settings to container: #{container_name}"

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
        config_redmine(container_name, container)
      end

      if container.has_key?('ipaddress')
        puts "IP Address Setting"
        config_ipaddress(container)
        puts "IP Address:#{container['ip_address']}"
      end
    end
  end
end

def config_ipaddress(container)
  container_config_path = File.join(container['container_path'],'config')
  open(container_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    config = f.read

    unless config.sub!(/^(?!.*#)\s*lxc.network.ipv4\s*=.*/, "lxc.network.ipv4=#{container['ipaddress']}")
      config << "#Added by test-environment-manager\n"
      config << "lxc.network.ipv4=#{container['ipaddress']}"
    end

    f.rewind
    f.puts config
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{container_config_path}"

  ipaddress_config_path = File.join(container['container_path'],'rootfs/etc/sysconfig/network-scripts/ifcfg-eth0')
  open(ipaddress_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    config = f.read

    unless config.sub!(/^(\s*)BOOTPROTO\s*=.*/, "BOOTPROTO=static")
      config << "BOOTPROTO=static"
    end

    f.rewind
    f.puts config
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{ipaddress_config_path}"

end

def config_zabbix_server(container)
  zabbix_server_config_path = File.join(container['container_path'],'rootfs/etc/zabbix/zabbix_server.conf')
  open(zabbix_server_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    unless body.sub!(/^(?!.*#)\s*DBHost\s*=.*/,"\nDBHost=localhost")
      body << "\n#Added by test-environment-manager\n"
      body << "DBHost=localhost\n"
    end

    unless body.sub!(/^(?!.*#)\s*DBName\s*=.*/,"\nDBName=#{container['zabbix-server']['database_name']}")
      body << "\n#Added by test-environment-manager\n"
      body << "DBName=#{container['zabbix-server']['database_name']}\n"
    end

    unless body.sub!(/^(?!.*#)\s*DBUser\s*=.*/,"\nDBUser=#{container['zabbix-server']['database_username']}")
      body << "\n#Added by test-environment-manager\n"
      body << "DBUser=#{container['zabbix-server']['database_username']}"
    end

    unless body.sub!(/^(?!.*#)\s*DBPassword\s*=.*/,"\nDBPassword=#{container['zabbix-server']['database_password']}")
      body << "\n#Added by test-environment-manager\n"
      body << "DBPassword=#{container['zabbix-server']['database_password']}"
    end

    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{zabbix_server_config_path}"

  httpd_zabbix_config_path = File.join(container['container_path'],'rootfs/etc/httpd/conf.d/zabbix.conf')
  open(httpd_zabbix_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    unless body.sub!(/^(?!.*#)\s*php_value\s*date.timezone.*/,"\nphp_value date.timezone Asia/Tokyo")
      body << "\n#Added by test-environment-manager\n"
      body << "php_value date.timezone Asia/Tokyo"
    end

    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{httpd_zabbix_config_path}"

end

def config_zabbix_agent(container)
  zabbix_agent_config_path = File.join(container['container_path'],'rootfs/etc/zabbix/zabbix_agentd.conf')
  open(zabbix_agent_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    unless body.sub!(/^(?!.*#)\s*Server\s*=.*/,"\nServer=#{container['zabbix-agent']['server_ipaddress']}")
      body << "\n#Added by test-environment-manager\n"
      body << "Server=#{container['zabbix-agent']['server_ipaddress']}"
    end

    unless body.sub!(/^(?!.*#)\s*ListenIP\s*=.*/,"\nListenIP=#{container['ipaddress']}")
      body << "\n#Added by test-environment-manager\n"
      body << "ListenIP=#{container['ipaddress']}"
    end

    unless body.sub!(/^(?!.*#)\s*Hostname\s*=.*/,"\nHostname=#{container['zabbix-agent']['host_name']}")
      body << "\n#Added by test-environment-manager\n"
      body << "Hostname=#{container['zabbix-agent']['host_name']}"
    end

    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{zabbix_agent_config_path}"

end

def config_nagios(container)
  nagios_config_path = File.join(container['container_path'],'rootfs/etc/nagios/nagios.cfg')
  open(nagios_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    unless body.sub!(/^(?!.*#)\s*broker_module\s*=.*/,"\nbroker_module=/usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg")
      body << "\n#Added by test-environment-manager\n"
      body << "broker_module=/usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg\n"
    end

    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{nagios_config_path}"

  ndo2db_config_path = File.join(container['container_path'],'rootfs/etc/nagios/ndo2db.cfg')
  open(ndo2db_config_path,"r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read

    unless body.sub!(/^(?!.*#)\s*db_name\s*=.*/,"\ndb_name=#{container['nagios']['database_name']}")
      body << "\n#Added by test-environment-manager\n"
      body << "db_name=#{container['nagios']['database_name']}"
    end

    unless body.sub!(/^(?!.*#)\s*db_user\s*=.*/,"\ndb_user=#{container['nagios']['database_username']}")
      body << "\n#Added by test-environment-manager\n"
      body << "db_user=#{container['nagios']['database_username']}"
    end

    unless body.sub!(/^(?!.*#)\s*db_pass\s*=.*/,"\ndb_pass=#{container['nagios']['database_password']}")
      body << "\n#Added by test-environment-manager\n"
      body << "db_user=#{container['nagios']['database_username']}"
    end

    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  puts "Settings saved as #{ndo2db_config_path}"

end

def config_hatohol(container)
end

def config_redmine(container_name, container)

  # Config /var/lib/redmine/config/database.yml
  database_config_path = File.join(container['container_path'],'rootfs/var/lib/redmine/config/database.yml')
  database_config_example_path = database_config_path + '.example'

  database_config = YAML::load_file(database_config_example_path)

  database_config['production']['database'] = container['redmine']['database_name']
  database_config['production']['username'] = container['redmine']['database_username']
  database_config['production']['password'] = container['redmine']['database_password']

  open(database_config_path,'w') do |f|
    YAML::dump(database_config,f)
  end

  puts "Settings saved as #{database_config_path}"

  # Database Setting
  c = LXC::Container.new(container_name)
  c.start

  puts "Container Starting"
  while true
    break unless c.ip_addresses.empty?
  end

  puts "Redmine Internal Setting Start"
  tmp_path = File.join(container['container_path'], 'rootfs/tmp')
  FileUtils.copy('assets/redmine_setup.sh', tmp_path)

  c.attach do
    LXC.run_command('bash /tmp/redmine_setup.sh')
  end
end
