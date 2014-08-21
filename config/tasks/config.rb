task 'config' => 'load_containers' do

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
      config_redmine(container)
    end
  end
end

def config_zabbix_server(container)
  open("#{container['container_path']}/rootfs/etc/zabbix/zabbix_server.conf","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    body.sub!(/#\s*DBHost/ , "DBHost");
    body.sub!(/^(?!.*#\s*)DBName=[[:print:]]*/,"DBName=#{container['zabbix-server']['database_name']}");
    body.sub!(/^(?!.*#\s*)DBUser=[[:print:]]*/,"DBUser=#{container['zabbix-server']['database_username']}");
    body.sub!(/#\s*DBPassword=[[:print:]]*/,"DBPassword=#{container['zabbix-server']['database_name']}");
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end

  open("#{container['container_path']}/rootfs/etc/httpd/conf.d/zabbix.conf","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    body.sub!(/#\s*php_value\s*date.timezone\s*Europe\/Riga/,"php_value date.timezone Asia/Tokyo");
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
    body.sub!(/^(?!.*#\s*)Server=[[:print:]]*/,"Server=#{container['zabbix-agent']['server_ipaddress']}");
    body.sub!(/#\s*ListenIP=[[:print:]]*/,"ListenIP=#{container['ipaddress']}");
    body.sub!(/^(?!.*#\s*)Hostname=[[:print:]]*/,"Hostname=#{container['zabbix-agent']['host_name']}");
    f.rewind
    f.puts body
    f.truncate(f.tell)
    f.close
  end
end

def config_nagios(container)
  open("#{container['container_path']}/rootfs/","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    p body.class
    if body.match(/^(?!.*#\s*)broker_module=[[:print]]*/)
      body.sub!(/^(?!.*#\s*)broker_module=[[:print]]*/,"broker_module=/usr/lib64/nagios/brokers/ndomod.so config_file=/etc/nagios/ndomod.cfg");
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

  open("#{container['container_path']}/rootfs/","r+") do |f|
    f.flock(File::LOCK_EX)
    body = f.read
    body.sub!(/db_name=[[:print:]]*/,"db_name=#{container['nagios']['database_name']}");
    body.sub!(/(?<!ndo2)db_user=[[:print:]]*/,"db_user=#{container['nagios']['database_username']}");
    body.sub!(/db_pass=[[:print:]]*/,"db_pass=#{container['nagios']['database_password']}");
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
