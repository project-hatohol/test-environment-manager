@containers.each do |container_name, container|
  namespace container_name do

    desc "#{container_name}:Show Container Status and IPs"
    task "status" do
      c = LXC::Container.new(container_name)
      puts "Status of #{container_name}: #{c.state}"
      puts "\tIP Address: #{c.ip_addresses}"
    end

    desc "Start Container:#{container_name}"
    task "start" do
      c = LXC::Container.new(container_name)
      c.start
      while true
        sleep 1
        break unless c.ip_addresses.empty?
      end
      puts "Start:#{container_name}(#{c.ip_addresses})"
    end

    desc "Shutdwon Container:#{container_name}"
    task "shutdown" do
      c = LXC::Container.new(container_name)
      puts "Shutdown:#{container_name}(#{c.ip_addresses})"
      c.shutdown
    end

    desc "Reboot Container:#{container_name}"
    task "reboot" do
      c = LXC::Container.new(container_name)
      puts "Reboot:#{container_name}(#{c.ip_addresses})"
      c.reboot
    end

    desc "Clone Container #{container_name} as base_container"
    task 'build' do
      if container.has_key?('base_container')
        base_container = LXC::Container.new(container['base_container'])
        base_container.shutdown

        puts "Clone from #{container['base_container']} to #{container_name}"
        base_container.clone(container_name)

        puts "Done."
      end
    end

    desc "Destroy Container:#{container_name}"
    task "destroy" do
      c = LXC::Container.new(container_name)
      puts "Destroy:#{container_name}"
      c.stop
      c.destroy
    end

    desc "Call Destroy and Build tasks for #{container_name}"
    task "rebuild" => ["destroy-#{container_name}", "build-#{container_name}"]
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
  task 'build' do |task|
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
end

def run_containers_task(task_name, containers)
  container_names = containers.keys
  container_names.each do |container_name|
    task = container_name + ':' + task_name
    Rake::Task[task].invoke
  end
end

def get_task_name(task)
  task_string = task.name.split(':')
  return task_string[1]
end
