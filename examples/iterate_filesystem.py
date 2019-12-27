from selenium import webdriver
from selenium.webdriver.remote.file_detector import UselessFileDetector

# Only ~ and absult paths seem to work here
files = ['~/notes.txt', '/etc/passwd', '/does/not/exist', '/bin/ls']

driver = webdriver.Remote(
   command_executor="http://selenium:4444/wd/hub",
   desired_capabilities={"browserName": "firefox"}
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
