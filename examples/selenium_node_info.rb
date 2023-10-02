#!/usr/bin/env ruby
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_info.rb
# 
# A quick script to get node OS, arch, selenium version, and available browsers. 

require 'optparse'
require 'net/http'
require 'json'
require 'uri'

options = {}
OptionParser.new do |opts|
  opts.banner = 'Usage: example.rb [options]'
  opts.on('-hURL', '--hubURL', 'Selenium Hub URL') do |h|
    options[:hub] = h
  end
  opts.on('--help', 'Prints this help') do
    puts opts
    exit
  end
end.parse!

hub_url = options[:hub]

# Start session with encoded_profile and save session id for cleanup.
uri = URI.parse("%s/graphql" % [hub_url])
http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'application/json')
request.body = "{\"operationName\":\"GetNodes\",\"variables\":{},\"query\":\"query GetNodes {\\n  nodesInfo {\\n    nodes {\\n      id\\n      uri\\n      status\\n      maxSession\\n      slotCount\\n      stereotypes\\n      version\\n      sessionCount\\n      osInfo {\\n        version\\n        name\\n        arch\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\"}"
response = http.request(request)
#puts response.body

# Output
for node in JSON.parse(response.body)["data"]["nodesInfo"]["nodes"]
  puts node["version"] + ", " + node["osInfo"]["name"] + ", " + node["osInfo"]["arch"]
  for stereotype in JSON.parse(node["stereotypes"])
    #puts stereotype
    puts "\t" + stereotype["stereotype"]["browserName"]
    #puts stereotype["stereotype"]["platformName"]
  end
  puts "\n"
end

exit
