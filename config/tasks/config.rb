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
end

def config_zabbix_agent(container)
end

def config_nagios(container)
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
