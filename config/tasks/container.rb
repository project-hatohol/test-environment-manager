@containers.each do |container_name, container_config|
  namespace container_name do

    desc "#{container_name}:Show Container Status and IPs"
    task "status" do
      container = LXC::Container.new(container_name)
      puts "Status of #{container_name}: #{container.state}"
      puts "\tIP Address: #{container.ip_addresses}"
    end

    desc "Start Container:#{container_name}"
    task "start" do
      container = LXC::Container.new(container_name)
      container.start
      while true
        sleep 1
        break unless container.ip_addresses.empty?
      end
      puts "Start:#{container_name}(#{container.ip_addresses})"
    end

    desc "Shutdwon Container:#{container_name}"
    task "shutdown" do
      container = LXC::Container.new(container_name)
      puts "Shutdown:#{container_name}(#{container.ip_addresses})"
      container.shutdown
    end

    desc "Reboot Container:#{container_name}"
    task "reboot" do
      container = LXC::Container.new(container_name)
      puts "Reboot:#{container_name}(#{container.ip_addresses})"
      container.reboot
    end

    desc "Clone Container #{container_name} as base_container"
    task 'clone' do
      if container_config.has_key?('base_container')
        base_container = LXC::Container.new(container_config['base_container'])
        base_container.shutdown

        puts "Clone from #{container_config['base_container']} to #{container_name}"
        base_container.clone(container_name)

        puts "Done."
      end
    end

    desc "Destroy Container:#{container_name}"
    task "destroy" do
      container = LXC::Container.new(container_name)
      puts "Destroy:#{container_name}"
      container.stop
      container.destroy
    end

    desc "Call Destroy and Build tasks for #{container_name}"
    task "rebuild" => ["destroy", "build"]
    
    desc "Call Clone and Config tasks for #{container_name}"
    task "build" => ["clone", "config","shutdown","start"]
  end
end

namespace 'all' do

  desc 'Show All Containers Status and IPs'
  task 'status' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Start All Containers'
  task 'start' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Shutdwon All Containers'
  task 'shutdown' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Reboot All Containers'
  task 'reboot' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Clone Container as base_container'
  task 'clone' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Destroy All Containers'
  task 'destroy' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

  desc 'Call Destroy and Build tasks'
  task 'rebuild' do |task|
    run_containers_task(get_task_name(task), @containers)
  end
  
  desc 'Call Clone and Config tasks'
  task 'build' do |task|
    run_containers_task(get_task_name(task), @containers)
  end

end

