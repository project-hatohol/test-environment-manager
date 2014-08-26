desc 'Show Container Status and IPs'
task 'status' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Status of #{container_name}: #{c.state}"
    puts "\tIP Address: #{c.ip_addresses}"
  end
end

desc 'Start All Containers'
task 'start' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    c.start
    while true
      sleep 1
      break unless c.ip_addresses.empty?
    end
    puts "Start:#{container_name}(#{c.ip_addresses})"
  end
end

desc 'Shutdwon All Containers'
task 'shutdown' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Shutdown:#{container_name}(#{c.ip_addresses})"
    c.shutdown
  end
end

desc 'Reboot All Containers'
task 'reboot' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Reboot:#{container_name}(#{c.ip_addresses})"
    c.reboot
  end
end

desc 'Clone Container as base_container'
task 'build' do
  @containers.each do |container_name, container|
    if container.has_key?('base_container')
      base_container = LXC::Container.new(container['base_container'])
      base_container.shutdown

      puts "Clone from #{container['base_container']} to #{container_name}"
      base_container.clone(container_name)

      puts "Done."
    end
  end
end

desc 'Destroy All Containers'
task 'destroy' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Destroy:#{container_name}"
    c.stop
    c.destroy
  end
end

desc 'Call Destroy and Build tasks'
task 'rebuild' => ['destroy', 'build']
