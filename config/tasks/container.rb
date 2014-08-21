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

task 'build' => 'load_containers' do
  @containers.each do |container_name, container|
    if container.has_key?('base_container')
      puts "Clone from #{container['base_container']} to #{container_name}"

      base_container = LXC::Container.new(container['base_container'])
      base_container.clone(container_name)

      puts "Done."
    end
  end
end

task 'destroy' => 'load_containers' do
  container_names = @containers.keys

  container_names.each do |container_name|
    c = LXC::Container.new(container_name)
    puts "Destroy:#{container_name}"
    c.stop
    c.destroy
  end
end