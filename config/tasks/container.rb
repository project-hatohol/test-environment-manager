task 'status' => 'load_containers' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Status of #{container_name}: #{c.state}"
  end
end

task 'start' => 'load_containers' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    c.start
    puts "Start:#{container_name}"
  end
end

task 'shutdown' => 'load_containers' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Shutdown:#{container_name}(#{c.ip_addresses})"
    c.shutdown
  end
end

task 'reboot' => 'load_containers' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Reboot:#{container_name}(#{c.ip_addresses})"
    c.reboot
  end
end