import base64, os
from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

local_file = '/bin/ls'
remote_file = '/tmp/ls_bin'

# Read in local file and base64 encode
file_data = ''
with open(local_file, 'rb') as file:
    file_data = base64.b64encode(file.read())

# Break remote file into path and basename
remote_path = os.path.dirname(remote_file)
remote_basename = os.path.basename(remote_file)

data_url = 'data:text/html;charset=utf-8,<html><a id=f href="data:application/octet-stream;charset=utf-16le;base64,%s" download="%s">f</a></html>' % ( file_data.decode('utf-8'), remote_basename )
print(data_url)

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', remote_path)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

driver = webdriver.Remote(
   command_executor="http://selenium:4444/wd/hub",
   desired_capabilities={"browserName": "firefox"},
   browser_profile=profile
   )
driver.file_detector = UselessFileDetector()

try:
    driver.get(data_url)
    driver.find_element_by_id('f').click()
finally:
    driver.quit()
